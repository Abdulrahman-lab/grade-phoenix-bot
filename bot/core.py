"""
🎓 Telegram Bot Core - Main Bot Implementation
"""
import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    TypeHandler,
)

# Absolute imports
from config import CONFIG
from storage.users import UserStorage
from storage.grades import GradeStorage
from university.api import UniversityAPI
from admin.dashboard import AdminDashboard
from admin.broadcast import BroadcastSystem
from utils.keyboards import get_main_keyboard, get_admin_keyboard
from utils.messages import get_welcome_message, get_help_message

logger = logging.getLogger(__name__)

# Conversation states
ASK_USERNAME, ASK_PASSWORD = range(2)

class TelegramBot:
    """Main Telegram Bot Class"""
    
    def __init__(self):
        self.app = None
        self.user_storage = UserStorage()
        self.grade_storage = GradeStorage()
        self.university_api = UniversityAPI()
        self.admin_dashboard = AdminDashboard()
        self.broadcast_system = BroadcastSystem()
        self.grade_check_task = None
        self.running = False
        
    async def start(self):
        """Start the bot"""
        import os
        try:
            # Initialize bot application
            self.app = Application.builder().token(CONFIG["TELEGRAM_TOKEN"]).build()
            
            # Add handlers
            self._add_handlers()
            
            # Start grade checking task
            if CONFIG["ENABLE_NOTIFICATIONS"]:
                self.grade_check_task = asyncio.create_task(self._grade_checking_loop())
            
            # Start webhook (for Railway)
            await self.app.initialize()
            await self.app.start()
            port = int(os.environ.get("PORT", 8443))
            webhook_url = f"https://shamunibot-production.up.railway.app/{CONFIG['TELEGRAM_TOKEN']}"
            
            logger.info(f"DEBUG: Setting up webhook on port {port}")
            logger.info(f"DEBUG: Webhook URL: {webhook_url}")
            
            await self.app.updater.start_webhook(
                listen="0.0.0.0",
                port=port,
                url_path=CONFIG["TELEGRAM_TOKEN"],
                webhook_url=webhook_url
            )
            
            logger.info("DEBUG: Webhook started successfully")
            
            self.running = True
            logger.info("🤖 Bot started successfully with webhook!")
            logger.info(f"🌐 Webhook URL: {webhook_url}")
            
        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            raise
    
    async def stop(self):
        """Stop the bot"""
        try:
            self.running = False
            
            if self.grade_check_task:
                self.grade_check_task.cancel()
            
            if self.app:
                await self.app.updater.stop()
                await self.app.stop()
                await self.app.shutdown()
            
            logger.info("🛑 Bot stopped successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error stopping bot: {e}")
    
    def _add_handlers(self):
        """Add all bot handlers"""
        logger.info("DEBUG: Adding bot handlers...")
        
        # Basic commands
        self.app.add_handler(CommandHandler("start", self._start_command))
        self.app.add_handler(CommandHandler("help", self._help_command))
        self.app.add_handler(CommandHandler("register", self._register_start))
        logger.info("DEBUG: Basic command handlers added")
        
        # User commands
        self.app.add_handler(CommandHandler("grades", self._grades_command))
        self.app.add_handler(CommandHandler("profile", self._profile_command))
        self.app.add_handler(CommandHandler("settings", self._settings_command))
        self.app.add_handler(CommandHandler("support", self._support_command))
        logger.info("DEBUG: User command handlers added")
        
        # Admin commands
        self.app.add_handler(CommandHandler("stats", self._stats_command))
        self.app.add_handler(CommandHandler("list_users", self._list_users_command))
        self.app.add_handler(CommandHandler("restart", self._restart_command))
        logger.info("DEBUG: Admin command handlers added")
        
        # Conversation handlers (registration and broadcast) - these must come BEFORE the generic message handler
        self.app.add_handler(self._get_registration_handler())
        self.app.add_handler(self._get_broadcast_handler())
        logger.info("DEBUG: Conversation handlers added")
        
        # Callback query handler
        self.app.add_handler(CallbackQueryHandler(self._handle_callback))
        logger.info("DEBUG: Callback query handler added")
        
        # Message handler for buttons (should be last)
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))
        logger.info("DEBUG: Message handler added")
        
        # Add catch-all update logger
        self.app.add_handler(TypeHandler(Update, self._log_any_update))
        logger.info("DEBUG: TypeHandler for logging added")
        
        logger.info("DEBUG: All handlers added successfully!")
    
    def _get_registration_handler(self):
        """Get registration conversation handler"""
        logger.info("DEBUG: Creating registration conversation handler")
        handler = ConversationHandler(
            entry_points=[
                CommandHandler("register", self._register_start),
                MessageHandler(filters.Regex("^🚀 تسجيل الدخول$"), self._register_start)
            ],
            states={
                ASK_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self._register_username)],
                ASK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, self._register_password)],
            },
            fallbacks=[CommandHandler("cancel", self._cancel_registration)],
        )
        logger.info("DEBUG: Registration conversation handler created successfully")
        return handler
    
    def _get_broadcast_handler(self):
        """Get broadcast conversation handler"""
        return self.broadcast_system.get_conversation_handler()
    
    # Command handlers
    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        welcome_msg = get_welcome_message(user.first_name)
        
        await update.message.reply_text(
            welcome_msg,
            reply_markup=get_main_keyboard()
        )
    
    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_msg = get_help_message()
        
        await update.message.reply_text(
            help_msg,
            reply_markup=get_main_keyboard()
        )
    
    async def _register_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start registration process"""
        logger.info("DEBUG: _register_start called")
        telegram_id = update.effective_user.id
        
        # Check if user already registered
        if self.user_storage.get_user(telegram_id):
            await update.message.reply_text(
                "✅ أنت مسجل بالفعل! يمكنك استخدام '📊 فحص الدرجات' لعرض درجاتك.",
                reply_markup=get_main_keyboard()
            )
            return ConversationHandler.END
        
        await update.message.reply_text(
            "🚀 **تسجيل الدخول للجامعة**\n\n"
            "يرجى إرسال اسم المستخدم الجامعي الخاص بك:\n"
            "(مثال: ENG2324901)",
            reply_markup=ReplyKeyboardMarkup([["❌ إلغاء"]], resize_keyboard=True)
        )
        logger.info(f"DEBUG: Registration started for user {telegram_id}")
        logger.info(f"DEBUG: Returning conversation state: {ASK_USERNAME}")
        return ASK_USERNAME
    
    async def _register_username(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info("DEBUG: _register_username called")
        username = update.message.text.strip()
        logger.info(f"DEBUG: Username received: {username}")
        
        if not username:
            await update.message.reply_text("اسم المستخدم غير صالح، حاول مرة أخرى:")
            return ASK_USERNAME
        
        context.user_data["username"] = username
        logger.info(f"DEBUG: Username stored in context: {username}")
        await update.message.reply_text("الآن، أرسل كلمة المرور الخاصة بك:")
        return ASK_PASSWORD
    
    async def _register_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle password input and complete registration"""
        logger.info("DEBUG: _register_password called")
        password = update.message.text.strip()
        logger.info(f"DEBUG: Password received (length: {len(password)})")
        
        if not password:
            await update.message.reply_text("❌ كلمة المرور غير صالحة، حاول مرة أخرى:")
            return ASK_PASSWORD
        
        username = context.user_data.get("username")
        telegram_id = update.effective_user.id
        logger.info(f"DEBUG: Attempting login for user {username} (ID: {telegram_id})")
        
        await update.message.reply_text("🔄 جاري تسجيل الدخول...")
        
        # Login to university
        token = await self.university_api.login(username, password)
        if not token:
            logger.warning(f"DEBUG: Login failed for user {username}")
            await update.message.reply_text(
                "❌ **فشل تسجيل الدخول**\n\n"
                "تأكد من صحة اسم المستخدم وكلمة المرور وحاول مرة أخرى.",
                reply_markup=get_main_keyboard()
            )
            return ConversationHandler.END
        
        logger.info(f"DEBUG: Login successful for user {username}, token received")
        await update.message.reply_text("📊 جاري جلب بياناتك...")
        
        # Fetch user data
        user_data = await self.university_api.get_user_data(token)
        if not user_data:
            logger.warning(f"DEBUG: Failed to fetch user data for {username}")
            await update.message.reply_text(
                "❌ **فشل جلب بيانات الطالب**\n\n"
                "حاول لاحقاً أو تواصل مع الدعم الفني.",
                reply_markup=get_main_keyboard()
            )
            return ConversationHandler.END
        
        logger.info(f"DEBUG: User data fetched successfully for {username}")
        
        # Save user
        self.user_storage.save_user(telegram_id, username, password, token, user_data)
        
        # Save grades
        grades = user_data.get("grades", [])
        self.grade_storage.save_grades(telegram_id, grades)
        
        logger.info(f"DEBUG: Registration completed successfully for user {username}")
        
        success_message = f"""
✅ **تم تسجيل الدخول بنجاح!**

👤 **مرحباً:** {user_data.get('fullname', username)}
📧 **البريد:** {user_data.get('email', 'غير محدد')}
📚 **عدد المواد:** {len(grades)}

🔔 **ستتلقى إشعارات عند تحديث درجاتك تلقائياً!**

💡 **يمكنك الآن:**
• 📊 فحص الدرجات الحالية
• 👤 عرض معلوماتك
• ⚙️ تعديل الإعدادات
"""
        
        await update.message.reply_text(
            success_message,
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END
    
    async def _cancel_registration(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel registration"""
        await update.message.reply_text(
            "❌ **تم إلغاء التسجيل**\n\n"
            "يمكنك المحاولة مرة أخرى في أي وقت.",
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END
    
    async def _grades_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /grades command"""
        telegram_id = update.effective_user.id
        user = self.user_storage.get_user(telegram_id)
        
        if not user:
            await update.message.reply_text(
                "❌ لم يتم تسجيلك بعد. اضغط على '🚀 تسجيل الدخول' أولاً.",
                reply_markup=get_main_keyboard()
            )
            return
        
        await update.message.reply_text("🔄 جاري فحص الدرجات...")
        
        # Get fresh grades
        token = user.get("token")
        if not token or not await self.university_api.test_token(token):
            token = await self.university_api.login(user.get("username"), user.get("password"))
            if token:
                user["token"] = token
                self.user_storage.update_user(telegram_id, user)
        
        if token:
            fresh_data = await self.university_api.get_user_data(token)
            if fresh_data:
                grades = fresh_data.get("grades", [])
                self.grade_storage.save_grades(telegram_id, grades)
                
                if grades:
                    message = "📊 **درجاتك الحالية:**\n\n"
                    for grade in grades:
                        # Safely extract all fields with proper validation
                        course_name = grade.get('المقرر', 'غير محدد')
                        course_code = grade.get('كود المادة', '')
                        ects_credits = grade.get('رصيد ECTS', '')
                        practical_grade = grade.get('درجة الأعمال', 'لم يتم النشر')
                        theoretical_grade = grade.get('درجة النظري', 'لم يتم النشر')
                        final_grade = grade.get('الدرجة', 'لم يتم النشر')
                        
                        # Validate and clean the data
                        course_name = course_name.strip() if course_name else 'غير محدد'
                        course_code = course_code.strip() if course_code else ''
                        ects_credits = ects_credits.strip() if ects_credits else ''
                        practical_grade = practical_grade.strip() if practical_grade else 'لم يتم النشر'
                        theoretical_grade = theoretical_grade.strip() if theoretical_grade else 'لم يتم النشر'
                        final_grade = final_grade.strip() if final_grade else 'لم يتم النشر'
                        
                        message += f"📚 **{course_name}**\n"
                        if course_code and course_code != '':
                            message += f"   🏷️ الكود: {course_code}\n"
                        if ects_credits and ects_credits != '':
                            message += f"   📊 الرصيد: {ects_credits} ECTS\n"
                        message += f"   🔬 درجة الأعمال: {practical_grade}\n"
                        message += f"   ✍️ درجة النظري: {theoretical_grade}\n"
                        message += f"   🎯 الدرجة النهائية: {final_grade}\n\n"
                else:
                    message = "📭 لا توجد درجات متاحة حالياً."
            else:
                message = "❌ فشل في جلب الدرجات. حاول مرة أخرى لاحقاً."
        else:
            message = "❌ فشل في تسجيل الدخول. حاول مرة أخرى."
        
        await update.message.reply_text(message, reply_markup=get_main_keyboard())
    
    async def _profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command"""
        telegram_id = update.effective_user.id
        user = self.user_storage.get_user(telegram_id)
        
        if not user:
            await update.message.reply_text(
                "❌ لم يتم تسجيلك بعد. اضغط على '🚀 تسجيل الدخول' أولاً.",
                reply_markup=get_main_keyboard()
            )
            return
        
        grades = self.grade_storage.get_grades(telegram_id)
        
        message = f"""
👤 **معلوماتك الشخصية:**

🆔 **معرف التلجرام:** {telegram_id}
👨‍🎓 **اسم المستخدم:** {user.get('username', 'غير محدد')}
📧 **البريد الإلكتروني:** {user.get('email', 'غير محدد')}
👤 **الاسم الكامل:** {user.get('fullname', 'غير محدد')}

📊 **عدد المواد:** {len(grades)}
🕒 **آخر تحديث:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        await update.message.reply_text(message, reply_markup=get_main_keyboard())
    
    async def _settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /settings command"""
        telegram_id = update.effective_user.id
        users_count = len(self.user_storage.get_all_users())
        grades_count = len(self.grade_storage.get_grades(telegram_id)) if telegram_id else 0
        
        settings_message = f"""
⚙️ **إعدادات البوت**

🔧 **الإعدادات الحالية:**
• 🔔 الإشعارات: {'مفعلة' if CONFIG["ENABLE_NOTIFICATIONS"] else 'معطلة'}
• ⚠️ إشعارات الأخطاء: {'مفعلة' if CONFIG["ENABLE_ERROR_NOTIFICATIONS"] else 'معطلة'}
• 🔄 فترة الفحص: كل {CONFIG["GRADE_CHECK_INTERVAL"]} دقائق
• 🔁 عدد المحاولات: {CONFIG["MAX_RETRY_ATTEMPTS"]}

📊 **إحصائيات البوت:**
• 👥 عدد المستخدمين: {users_count}
• 📈 عدد المواد: {grades_count}

🔗 **معلومات الاتصال:**
• 👨‍💻 المطور: {CONFIG["ADMIN_USERNAME"]}
• 📧 البريد الإلكتروني: {CONFIG["ADMIN_EMAIL"]}
• 🌐 موقع الجامعة: {CONFIG["UNIVERSITY_WEBSITE"]}

هل تريد تغيير أي إعداد؟ ⚙️
"""
        
        await update.message.reply_text(settings_message, reply_markup=get_main_keyboard())
    
    async def _support_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /support command"""
        support_text = """
📞 **الدعم الفني:**

Developed by Abdulrahman Abdulkader
Email: abdulrahmanabdulkader59@gmail.com
username on other platforms: @sisp_t

🔧 **في حالة وجود مشاكل:**
1. تأكد من صحة بياناتك الجامعية
2. تحقق من اتصال الإنترنت
3. تواصل مع المطور

💬 **ساعات الدعم:** 24/7
"""
        
        await update.message.reply_text(support_text, reply_markup=get_main_keyboard())
    
    async def _stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command (admin only)"""
        if update.effective_user.id != CONFIG["ADMIN_ID"]:
            return
        
        stats = await self.admin_dashboard.get_stats()
        await update.message.reply_text(stats, reply_markup=get_admin_keyboard())
    
    async def _list_users_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /list_users command (admin only)"""
        if update.effective_user.id != CONFIG["ADMIN_ID"]:
            return
        
        users_list = await self.admin_dashboard.get_users_list()
        await update.message.reply_text(users_list, reply_markup=get_admin_keyboard())
    
    async def _restart_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /restart command (admin only)"""
        if update.effective_user.id != CONFIG["ADMIN_ID"]:
            return
        
        await update.message.reply_text("🔄 جاري إعادة تشغيل البوت...")
        await update.message.reply_text("✅ تم إعادة تشغيل البوت بنجاح!", reply_markup=get_admin_keyboard())
    
    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages and button clicks"""
        text = update.message.text
        
        if text == "🚀 تسجيل الدخول":
            await self._register_start(update, context)
        elif text == "📊 فحص الدرجات":
            await self._grades_command(update, context)
        elif text == "👤 معلوماتي":
            await self._profile_command(update, context)
        elif text == "⚙️ الإعدادات":
            await self._settings_command(update, context)
        elif text == "❓ المساعدة":
            await self._help_command(update, context)
        elif text == "📞 الدعم":
            await self._support_command(update, context)
        elif text == "🎛️ لوحة التحكم" and update.effective_user.id == CONFIG["ADMIN_ID"]:
            await self.admin_dashboard.show_dashboard(update, context)
        elif text == "🔙 العودة":
            await self._start_command(update, context)
        else:
            await update.message.reply_text(
                "❓ لم أفهم طلبك. استخدم الأزرار أدناه أو اكتب /help للمساعدة.",
                reply_markup=get_main_keyboard()
            )
    
    async def _handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != CONFIG["ADMIN_ID"]:
            return
        
        await self.admin_dashboard.handle_callback(update, context)
    
    async def _grade_checking_loop(self):
        """Main loop for checking grades"""
        while self.running:
            try:
                logger.info("🔄 Starting grade check cycle...")
                
                users = self.user_storage.get_all_users()
                for user in users:
                    await self._check_user_grades(user)
                
                logger.info(f"✅ Grade check completed. Next check in {CONFIG['GRADE_CHECK_INTERVAL']} minutes")
                
                # Wait for next check
                await asyncio.sleep(CONFIG["GRADE_CHECK_INTERVAL"] * 60)
                
            except asyncio.CancelledError:
                logger.info("🛑 Grade checking task cancelled")
                break
            except Exception as e:
                logger.error(f"❌ Error in grade checking: {e}")
                await asyncio.sleep(300)  # 5 minutes
    
    async def _check_user_grades(self, user):
        """Check grades for a specific user"""
        try:
            telegram_id = user.get("telegram_id")
            username = user.get("username")
            password = user.get("password")
            
            # Try to use stored token first
            token = user.get("token")
            if not token or not await self.university_api.test_token(token):
                logger.info(f"Token expired for user {username}, re-authenticating...")
                token = await self.university_api.login(username, password)
                if token:
                    user["token"] = token
                    self.user_storage.update_user(telegram_id, user)
                else:
                    logger.warning(f"Failed to re-authenticate user {username}")
                    return
            
            # Get fresh data
            user_data = await self.university_api.get_user_data(token)
            if not user_data:
                logger.warning(f"Failed to fetch data for user {username}")
                return
            
            # Compare grades
            old_grades = self.grade_storage.get_grades(telegram_id)
            new_grades = user_data.get("grades", [])
            
            if old_grades != new_grades:
                # Grades changed, notify user
                changes = []
                for new_grade in new_grades:
                    course_name = new_grade.get("المقرر", "")
                    old_grade = next((g for g in old_grades if g.get("المقرر") == course_name), None)
                    
                    if not old_grade or old_grade != new_grade:
                        changes.append(new_grade)
                
                if changes:
                    message = "🎓 تم تحديث درجاتك:\n\n"
                    for grade in changes:
                        # Safely extract all fields with proper validation
                        course_name = grade.get('المقرر', 'غير محدد')
                        course_code = grade.get('كود المادة', '')
                        practical_grade = grade.get('درجة الأعمال', 'لم يتم النشر')
                        theoretical_grade = grade.get('درجة النظري', 'لم يتم النشر')
                        final_grade = grade.get('الدرجة', 'لم يتم النشر')
                        
                        # Validate and clean the data
                        course_name = course_name.strip() if course_name else 'غير محدد'
                        course_code = course_code.strip() if course_code else ''
                        practical_grade = practical_grade.strip() if practical_grade else 'لم يتم النشر'
                        theoretical_grade = theoretical_grade.strip() if theoretical_grade else 'لم يتم النشر'
                        final_grade = final_grade.strip() if final_grade else 'لم يتم النشر'
                        
                        message += f"📚 **{course_name}**\n"
                        if course_code and course_code != '':
                            message += f"   🏷️ الكود: {course_code}\n"
                        message += f"   🔬 درجة الأعمال: {practical_grade}\n"
                        message += f"   ✍️ درجة النظري: {theoretical_grade}\n"
                        message += f"   🎯 الدرجة النهائية: {final_grade}\n\n"
                    
                    try:
                        await self.app.bot.send_message(chat_id=telegram_id, text=message)
                        logger.info(f"Sent grade update to user {username}")
                    except Exception as e:
                        logger.error(f"Failed to send message to user {username}: {e}")
                
                # Save new grades
                self.grade_storage.save_grades(telegram_id, new_grades)
            else:
                logger.info(f"No grade changes for user {username}")
                
        except Exception as e:
            logger.error(f"Error checking grades for user {user.get('username', 'unknown')}: {e}")
    
    async def _log_any_update(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Log any incoming update for debugging"""
        try:
            update_type = "Unknown"
            user_info = "Unknown"
            
            if update.message:
                update_type = "Message"
                user_info = f"ID: {update.effective_user.id}, Username: {update.effective_user.username}, Text: {update.message.text[:50]}..."
            elif update.callback_query:
                update_type = "Callback Query"
                user_info = f"ID: {update.effective_user.id}, Username: {update.effective_user.username}, Data: {update.callback_query.data}"
            elif update.edited_message:
                update_type = "Edited Message"
                user_info = f"ID: {update.effective_user.id}, Username: {update.effective_user.username}"
            
            logger.info(f"DEBUG: Received {update_type} update - {user_info}")
            
        except Exception as e:
            logger.error(f"DEBUG: Error logging update: {e}")
            logger.info(f"DEBUG: Raw update: {update}") 