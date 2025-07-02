"""
📝 Message Templates
"""
from config import CONFIG
from storage.models import Base, DatabaseManager

def get_welcome_message(fullname: str | None = None) -> str:
    """Returns a simple, user-friendly welcome message explaining what the bot does."""
    name_line = f"أهلاً {fullname}!\n\n" if fullname else "مرحباً بك! 👋\n\n"
    
    return (
        name_line
        + "🎓 **ما هو هذا البوت؟**\n"
        + "هذا البوت يساعدك في متابعة درجاتك الجامعية بسهولة!\n\n"
        + "✨ **ماذا يمكنك أن تفعل؟**\n"
        + "• 📊 عرض درجاتك الحالية\n"
        + "• 🔔 الحصول على إشعارات عند تحديث الدرجات\n"
        + "• 📱 استخدام واجهة سهلة وبسيطة\n\n"
        + "🚀 **للبدء:**\n"
        + "اضغط على '🚀 تسجيل الدخول' وأدخل بياناتك الجامعية\n\n"
        + "🔐 **الأمان:**\n"
        + "بياناتك محمية ومشفرة بالكامل\n\n"
        + f"👨‍💻 المطور: {CONFIG['ADMIN_USERNAME']}\n"
        + f"📱 الإصدار: {CONFIG['BOT_VERSION']}"
    )

def get_simple_welcome_message() -> str:
    """Returns a very simple welcome message for new users."""
    return (
        "مرحباً! 👋\n\n"
        + "🎓 **بوت متابعة الدرجات الجامعية**\n\n"
        + "**ماذا يفعل البوت؟**\n"
        + "• يعرض درجاتك الجامعية\n"
        + "• يخبرك عند تحديث الدرجات\n"
        + "• سهل الاستخدام\n\n"
        + "**كيف تبدأ؟**\n"
        + "اضغط '🚀 تسجيل الدخول' وأدخل بياناتك الجامعية\n\n"
        + "🔐 بياناتك آمنة ومشفرة\n"
        + f"👨‍💻 للمساعدة: {CONFIG['ADMIN_USERNAME']}"
    )

def get_security_welcome_message() -> str:
    """Returns a security-focused welcome message for returning users."""
    return (
        "مرحباً بعودتك! 🔐\n\n"
        + "✅ **حالة الأمان:** ممتازة\n"
        + "🔒 **حماية البيانات:** مشفرة\n"
        + "🛡️ **معايير الأمان:** OWASP + NIST\n\n"
        + "**الأوامر الأمنية:**\n"
        + "🔍 `/security_info` - معلومات الأمان\n"
        + "📋 `/security_audit` - تقرير الأمان\n"
        + "🔒 `/privacy_policy` - سياسة الخصوصية\n\n"
        + "💡 استخدم الأزرار أدناه للوصول للميزات"
    )

def get_help_message() -> str:
    """دالة ترجع رسالة المساعدة."""
    return (
        "استخدم القائمة الرئيسية للتنقل بين الميزات.\n\n"
        "• تسجيل الدخول: لإدخال بياناتك الجامعية\n"
        "• عرض الدرجات: للاطلاع على نتائجك\n"
        "• الإعدادات: لتخصيص تجربتك\n\n"
        f"للمساعدة: {CONFIG['ADMIN_USERNAME']}\n"
        f"الإصدار: {CONFIG['BOT_VERSION']}\n"
        "THE DIE IS CAST"
    )

def get_error_message(error_type: str = "عام") -> str:
    """دالة ترجع رسالة الخطأ."""
    error_messages = {
        "login_failed": "تعذّر تسجيل الدخول. يرجى التأكد من صحة البيانات.",
        "network_error": "حدث خطأ في الاتصال. يرجى المحاولة لاحقًا.",
        "api_error": "النظام غير متاح حاليًا. حاول لاحقًا.",
        "token_expired": "انتهت الجلسة. يرجى تسجيل الدخول مجددًا.",
        "no_grades": "لا توجد درجات متاحة حاليًا.",
        "general": "حدث خطأ غير متوقع. يرجى المحاولة لاحقًا."
    }
    return error_messages.get(error_type, error_messages["general"])

def get_success_message(action: str) -> str:
    """دالة ترجع رسالة النجاح."""
    success_messages = {
        "login": "✅ تم تسجيل الدخول بنجاح!\n\nيمكنك الآن فحص درجاتك واستلام الإشعارات.",
        "grades_updated": "📊 تم تحديث الدرجات بنجاح!\n\nتم فحص درجاتك وتحديثها.",
        "settings_saved": "⚙️ تم حفظ الإعدادات بنجاح!\n\nتم تحديث إعداداتك.",
        "profile_updated": "👤 تم تحديث الملف الشخصي بنجاح!\n\nتم تحديث معلوماتك الشخصية."
    }
    
    return success_messages.get(action, "✅ تم تنفيذ العملية بنجاح!")

def get_info_message(info_type: str) -> str:
    """دالة ترجع رسالة المعلومات."""
    info_messages = {
        "not_registered": "❌ لم يتم تسجيلك بعد.\n\nاضغط على '🚀 تسجيل الدخول' أولاً لإدخال بياناتك الجامعية.",
        "no_permission": "🚫 ليس لديك صلاحية الوصول لهذه الميزة.",
        "maintenance": "🔧 البوت في الصيانة حاليًا. يرجى المحاولة لاحقًا أو التواصل مع الدعم.",
        "coming_soon": "🚧 قريبًا: هذه الميزة ستتوفر لاحقًا."
    }
    
    return info_messages.get(info_type, "ℹ️ معلومات") 

def get_registration_success_message(username: str) -> str:
    """دالة ترجع رسالة نجاح تسجيل الدخول."""
    return (
        f"تم تسجيل الدخول بنجاح.\n\n"
        f"مرحباً {username}.\n\n"
        f"يمكنك الآن متابعة درجاتك في نظام الإشعارات الجامعية.\n\n"
        f"THE DIE IS CAST"
    ) 

def get_credentials_security_info_message() -> str:
    """Returns a security info message shown when asking for credentials."""
    return (
        "🔒 لماذا نطلب بياناتك الجامعية؟\n"
        "نحتاج إلى اسم المستخدم وكلمة المرور فقط لتسجيل الدخول إلى نظام الجامعة وجلب درجاتك. "
        "لا نقوم بتخزين كلمة المرور، ويتم حذفها فوراً بعد تسجيل الدخول. بياناتك مشفرة وآمنة، ويمكنك تغيير كلمة المرور في أي وقت من بوابة الجامعة.\n\n"
        "للأمان الكامل، ننصح باستخدام كلمة مرور خاصة لهذا الحساب وعدم مشاركتها مع أي خدمة أخرى."
    )

db_manager = DatabaseManager(CONFIG["DATABASE_URL"])
Base.metadata.create_all(bind=db_manager.engine) 