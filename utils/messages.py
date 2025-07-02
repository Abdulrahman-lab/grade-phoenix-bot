"""
📝 Message Templates
"""
from config import CONFIG
from storage.models import Base, DatabaseManager

def get_welcome_message(fullname: str = None) -> str:
    """Returns the welcome message for the user, mentioning their university fullname if available."""
    name_line = f"مرحباً {fullname} في نظام الإشعارات الجامعية!\n\n" if fullname else "مرحباً بك في نظام الإشعارات الجامعية!\n\n"
    return (
        name_line
        + "سجّل دخولك لمتابعة درجاتك الأكاديمية بسهولة.\n\n"
        + f"المطور: {CONFIG['ADMIN_USERNAME']}\n"
        + f"Version: {CONFIG['BOT_VERSION']}\n"
        "THE DIE IS CAST"
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

db_manager = DatabaseManager(CONFIG["DATABASE_URL"])
Base.metadata.create_all(bind=db_manager.engine) 