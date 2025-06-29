# 🚀 دليل النشر - Telegram University Bot v2.0.0

## 📋 المتطلبات الأساسية

### 1. حساب Telegram Bot
1. اذهب إلى [@BotFather](https://t.me/BotFather) على Telegram
2. اكتب `/newbot` لإنشاء بوت جديد
3. اختر اسم للبوت (مثال: "بوت إشعارات الدرجات")
4. اختر username للبوت (مثال: `university_grades_bot`)
5. احفظ التوكن الذي ستحصل عليه

### 2. معرف Telegram الخاص بك
1. اذهب إلى [@userinfobot](https://t.me/userinfobot)
2. اكتب `/start`
3. احفظ معرف Telegram الخاص بك (مثال: `123456789`)

## 🌐 النشر على Railway

### الخطوة 1: إعداد GitHub
```bash
# إنشاء مستودع جديد على GitHub
git init
git add .
git commit -m "Initial commit - Telegram University Bot v2.0.0"
git branch -M main
git remote add origin https://github.com/yourusername/telegram-university-bot.git
git push -u origin main
```

### الخطوة 2: إعداد Railway
1. اذهب إلى [Railway.app](https://railway.app)
2. سجل دخولك بحساب GitHub
3. اضغط "New Project"
4. اختر "Deploy from GitHub repo"
5. اختر المستودع الذي أنشأته

### الخطوة 3: إعداد المتغيرات البيئية
في Railway، اذهب إلى "Variables" وأضف:

```bash
# متغيرات مطلوبة
TELEGRAM_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_id_here

# متغيرات اختيارية
ADMIN_USERNAME=@your_username
ADMIN_EMAIL=your_email@example.com
DEBUG_MODE=false
LOG_LEVEL=INFO
```

### الخطوة 4: النشر
1. Railway سيقوم بالبناء تلقائياً
2. انتظر حتى يكتمل البناء
3. البوت سيعمل تلقائياً

## 🔧 إعدادات النشر

### ملف Procfile
```
web: python main.py
```

### ملف requirements.txt
```
python-telegram-bot==20.7
aiohttp==3.9.1
beautifulsoup4==4.12.2
flask==3.0.0
python-dotenv==1.0.0
```

### ملف runtime.txt
```
python-3.11.7
```

## 📊 مراقبة البوت

### فحص الصحة
- **الرابط:** `https://your-app.railway.app/health`
- **الحالة:** يجب أن تعرض `{"status": "healthy"}`

### السجلات
- في Railway، اذهب إلى "Deployments"
- اضغط على آخر deployment
- شاهد "Logs" لمراقبة البوت

### الإحصائيات
- استخدم `/stats` في البوت (للمطور فقط)
- شاهد إحصائيات Railway في لوحة التحكم

## 🛠️ استكشاف الأخطاء

### مشاكل شائعة

#### 1. البوت لا يستجيب
```bash
# تحقق من:
- صحة TELEGRAM_TOKEN
- صحة ADMIN_ID
- سجلات Railway
```

#### 2. فشل في تسجيل الدخول
```bash
# تحقق من:
- صحة بيانات الجامعة
- اتصال الإنترنت
- حالة API الجامعة
```

#### 3. فشل في النشر
```bash
# تحقق من:
- صحة requirements.txt
- صحة Python version
- سجلات البناء في Railway
```

### أوامر التشخيص
```bash
# فحص الصحة
curl https://your-app.railway.app/health

# فحص الحالة
curl https://your-app.railway.app/status

# فحص الجذر
curl https://your-app.railway.app/
```

## 🔄 التحديثات

### تحديث البوت
```bash
# في GitHub
git add .
git commit -m "Update bot"
git push origin main

# Railway سيقوم بالتحديث تلقائياً
```

### إعادة تشغيل البوت
```bash
# في Railway
- اذهب إلى "Deployments"
- اضغط "Redeploy"
```

## 📱 اختبار البوت

### 1. اختبار أساسي
```
/start - بدء البوت
/help - المساعدة
```

### 2. اختبار تسجيل الدخول
```
/register - تسجيل الدخول بالجامعة
```

### 3. اختبار فحص الدرجات
```
/grades - فحص الدرجات
```

### 4. اختبار المطور
```
/stats - إحصائيات (للمطور فقط)
/broadcast - إشعار عام (للمطور فقط)
```

## 🔒 الأمان

### نصائح أمنية
1. **لا تشارك التوكن** مع أي شخص
2. **استخدم متغيرات بيئية** للمعلومات الحساسة
3. **راقب سجلات البوت** دورياً
4. **احتفظ بنسخ احتياطية** من البيانات
5. **حدث البوت** بانتظام

### مراقبة الأمان
- راجع سجلات Railway دورياً
- تحقق من إحصائيات البوت
- راقب الأنشطة المشبوهة

## 📞 الدعم

### في حالة المشاكل
1. **تحقق من السجلات** في Railway
2. **اختبر البوت** محلياً أولاً
3. **تواصل مع المطور:**
   - البريد الإلكتروني: tox098123@gmail.com
   - Telegram: @Abdulrahman_lab

### موارد مفيدة
- [Railway Documentation](https://docs.railway.app)
- [Python Telegram Bot Documentation](https://python-telegram-bot.readthedocs.io)
- [GitHub Repository](https://github.com/yourusername/telegram-university-bot)

---

🔔 **بوت الإشعارات الجامعية** - نظام متقدم لإشعارات الدرجات الجامعية
👨‍💻 المطور: عبدالرحمن عبدالقادر 