# قائمة بالرسائل المترجمة للغات الثلاث

error_messages = {
    "invalid_number": {
        "العربية": "يرجى إدخال أرقام صحيحة! ❗️",
        "English": "Please enter valid numbers! ❗️",
        "Română": "Vă rugăm să introduceți numere valide! ❗️"
    },
    "missing_values": {
        "العربية": "يرجى إدخال جميع القيم المطلوبة! ❗️",
        "English": "Please enter all required values! ❗️",
        "Română": "Vă rugăm să introduceți toate valorile necesare! ❗️"
    },
    "eggs_exceed": {
        "العربية": "عدد البيض يجب ألا يتجاوز 580! ❗️",
        "English": "Number of eggs should not exceed 580! ❗️",
        "Română": "Numărul de ouă nu trebuie să depășească 580! ❗️"
    },
    "days_exceed": {
        "العربية": "عدد الأيام يجب ألا يتجاوز 730! ❗️",
        "English": "Number of days should not exceed 730! ❗️",
        "Română": "Numărul de zile nu trebuie să depășească 730! ❗️"
    },
    "reset_success": {
        "العربية": "تم إعادة التعيين بنجاح! ✅",
        "English": "Reset successful! ✅",
        "Română": "Resetare reușită! ✅"
    },
    "no_chicken_data": {
        "العربية": "لا توجد بيانات دجاج مدخلة حتى الآن!",
        "English": "No chicken data entered yet!",
        "Română": "Nu există date despre găini introduse încă!"
    },
    "not_first_year_chicken": {
        "العربية": "لا يمكن بيع الدجاجة لأنها في السنة الثانية (تجاوزت 320 بيضة أو 365 يوم)",
        "English": "Chicken cannot be sold as it's in the second year (exceeded 320 eggs or 365 days)",
        "Română": "Găina nu poate fi vândută deoarece este în al doilea an (a depășit 320 de ouă sau 365 de zile)"
    },
    "save_success": {
        "العربية": "تم حفظ الأسعار الجديدة بنجاح! ✅",
        "English": "New prices saved successfully! ✅",
        "Română": "Prețurile noi au fost salvate cu succes! ✅"
    },
    "chicken_added": {
        "العربية": "تمت إضافة الدجاجة رقم {chicken_id} بنجاح! ✅",
        "English": "Chicken #{chicken_id} added successfully! ✅",
        "Română": "Găina #{chicken_id} a fost adăugată cu succes! ✅"
    }
}

# رسائل المساعدة
help_messages = {
    "eggs_input": {
        "العربية": "أدخل عدد البيض (بحد أقصى 580 للسنتين، 320 للسنة الأولى)",
        "English": "Enter the number of eggs (max 580 for both years, 320 for first year)",
        "Română": "Introduceți numărul de ouă (maxim 580 pentru ambii ani, 320 pentru primul an)"
    },
    "days_input": {
        "العربية": "أدخل عدد الأيام (بحد أقصى 730 للسنتين، 365 للسنة الأولى)",
        "English": "Enter the number of days (max 730 for both years, 365 for first year)",
        "Română": "Introduceți numărul de zile (maxim 730 pentru ambii ani, 365 pentru primul an)"
    },
    "rewards_input": {
        "العربية": "أدخل عدد المكافآت",
        "English": "Enter the number of rewards",
        "Română": "Introduceți numărul de recompense"
    },
    "food_input": {
        "العربية": "أدخل عدد الطعام المطلوب",
        "English": "Enter the amount of food needed",
        "Română": "Introduceți cantitatea de hrană necesară"
    }
}

# استخدام الرسائل
def get_error_message(key, language, **kwargs):
    if key in error_messages and language in error_messages[key]:
        # تنسيق الرسالة باستخدام المتغيرات إذا تم توفيرها
        return error_messages[key][language].format(**kwargs)
    else:
        # رسالة افتراضية بالإنجليزية إذا كان المفتاح أو اللغة غير موجودين
        return "An error occurred!"

# استخدام رسائل المساعدة
def get_help_message(key, language):
    if key in help_messages and language in help_messages[key]:
        return help_messages[key][language]
    else:
        # رسالة افتراضية بالإنجليزية إذا كان المفتاح أو اللغة غير موجودين
        return ""
