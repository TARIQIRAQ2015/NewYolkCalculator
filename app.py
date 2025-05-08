import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# استيراد رسائل الخطأ المترجمة
from error_messages_fix import get_error_message, get_help_message

# تحسين الواجهة
st.set_page_config(
    page_title="New Yolk Calculator",
    page_icon="🐔",
    layout="wide"
)

# إخفاء أزرار التحكم بالمظهر
st.markdown("""
    <style>
        /* إخفاء العناصر غير الضرورية */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stToolbar"] {visibility: hidden;}
        
        /* تحسين المظهر العام والخلفية */
        .stApp {
            background: linear-gradient(135deg, 
                #1a1a2e,
                #16213e,
                #0f3460,
                #162447
            );
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            color: #e2e2e2;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* تأثير الإيموجي */
        .emoji-link {
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            cursor: pointer;
            font-size: 32px;
            margin-right: 10px;
        }
        .emoji-link:hover {
            transform: scale(1.5);
            text-shadow: 0 0 20px rgba(255,255,255,0.5);
        }
        
        /* تحسين القوائم المنسدلة */
        .stSelectbox > div > div,
        .stNumberInput > div > div {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            padding: 12px !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            height: auto !important;
            min-height: 48px !important;
            font-size: 16px !important;
            line-height: 1.5 !important;
            position: relative;
            overflow: hidden;
        }
        
        /* تأثير الموجة عند التحويم */
        .stSelectbox > div > div::before,
        .stNumberInput > div > div::before,
        div[data-baseweb="select"] ul li::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.05),
                transparent
            );
            transition: all 0.5s ease;
            z-index: 1;
        }
        
        .stSelectbox > div > div:hover::before,
        .stNumberInput > div > div:hover::before,
        div[data-baseweb="select"] ul li:hover::before {
            left: 100%;
        }
        
        /* تأثير التحويم */
        .stSelectbox > div > div:hover,
        .stNumberInput > div > div:hover {
            background: linear-gradient(135deg, #161b25 0%, #1e212b 100%) !important;
            border-color: rgba(255, 255, 255, 0.3) !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* تحسين قائمة الخيارات المنسدلة */
        div[data-baseweb="select"] > div {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            padding: 8px !important;
            transition: all 0.3s ease;
        }
        
        div[data-baseweb="select"] ul {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            padding: 4px !important;
            border-radius: 8px !important;
            backdrop-filter: blur(10px);
        }
        
        /* تحسين عناصر القائمة */
        div[data-baseweb="select"] ul li {
            background: transparent !important;
            transition: all 0.3s ease;
            border-radius: 6px;
            margin: 2px 0;
            padding: 10px 12px !important;
            position: relative;
            overflow: hidden;
            cursor: pointer;
            color: rgba(255, 255, 255, 0.8) !important;
        }
        
        div[data-baseweb="select"] ul li:hover {
            background: linear-gradient(135deg, #161b25 0%, #1e212b 100%) !important;
            transform: translateX(4px);
            color: #ffffff !important;
        }
        
        /* تحسين الأيقونات في القوائم */
        .stSelectbox svg,
        div[data-baseweb="select"] svg {
            transition: all 0.3s ease;
            fill: rgba(255, 255, 255, 0.7) !important;
        }
        
        .stSelectbox:hover svg,
        div[data-baseweb="select"]:hover svg {
            fill: rgba(255, 255, 255, 1) !important;
            transform: translateY(1px);
        }
        
        /* تحسين النص المحدد */
        div[data-baseweb="select"] [aria-selected="true"] {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        /* تحسين الخط والقراءة */
        .stMarkdown {
            font-size: 16px !important;
            line-height: 1.6 !important;
            color: #e2e2e2 !important;
        }
        
        /* تحسين المسافات بين العناصر */
        .element-container {
            margin: 1.5rem 0 !important;
        }
        
        /* إخفاء أزرار الزيادة والنقصان في حقول الإدخال العددية */
        input[type="number"]::-webkit-inner-spin-button, 
        input[type="number"]::-webkit-outer-spin-button { 
            -webkit-appearance: none; 
            margin: 0; 
        }
        
        input[type="number"] {
            -moz-appearance: textfield;
        }
        
        /* إخفاء رسالة "Press Enter to apply" وجميع رسائل المساعدة */
        .stNumberInput [data-testid="InputHelpText"],
        .stTextInput [data-testid="InputHelpText"],
        [data-testid="stForm"] [data-testid="InputHelpText"] {
            display: none !important;
        }
        
        /* إضافة تنسيق لتوافق أفضل مع جميع اللغات */
        [dir="rtl"] .stNumberInput input,
        [dir="rtl"] .stTextInput input {
            text-align: right !important;
        }
        
        [dir="ltr"] .stNumberInput input,
        [dir="ltr"] .stTextInput input {
            text-align: left !important;
        }
        
        /* تحسين النصوص والعناصر الأخرى */
        .stMarkdown {
            color: #e2e2e2;
        }
        
        /* تحسين الروابط */
        a {
            color: #4f8fba !important;
            text-decoration: none !important;
            transition: all 0.3s ease;
        }
        a:hover {
            color: #6ba5d1 !important;
            text-decoration: none !important;
        }
        
        /* تحسين تأثير الضغط على الدجاجة */
        .emoji-link {
            font-size: 24px;
            text-decoration: none;
            transition: all 0.3s ease;
            display: inline-block;
            margin-right: 8px;
            filter: drop-shadow(0 0 8px rgba(255,255,255,0.2));
        }
        
        .emoji-link:hover {
            transform: scale(1.2);
            filter: drop-shadow(0 0 12px rgba(255,255,255,0.4));
        }
        
        .emoji-link:active {
            transform: scale(0.95);
        }
        
        /* تحسين العنوان */
        .title {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 12px;
            text-align: center;
            background: linear-gradient(120deg, #ffffff, #e2e2e2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .title-text {
            text-decoration: none;
            color: inherit;
            margin-left: 8px;
        }
        
        /* تحسين القوائم المنسدلة */
        .stSelectbox > div > div {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            padding: 12px !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            height: auto !important;
            min-height: 48px !important;
            font-size: 16px !important;
            line-height: 1.5 !important;
        }
        
        /* تحسين قائمة الخيارات المنسدلة */
        div[data-baseweb="select"] > div {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            padding: 8px !important;
            min-width: 200px !important;
        }
        
        div[data-baseweb="select"] ul {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            padding: 4px !important;
        }
        
        div[data-baseweb="select"] ul li {
            color: #ffffff !important;
            font-size: 16px !important;
            padding: 12px !important;
            margin: 4px 0 !important;
            border-radius: 6px !important;
            line-height: 1.5 !important;
        }
        
        /* تحسين النصوص في القوائم */
        .stSelectbox label {
            color: #ffffff !important;
            font-size: 18px !important;
            font-weight: 500 !important;
            margin-bottom: 12px !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
            line-height: 1.5 !important;
        }
        
        /* تحسين الأيقونة في القائمة المنسدلة */
        .stSelectbox svg {
            fill: #ffffff !important;
            width: 24px !important;
            height: 24px !important;
        }
        
        /* تحسين العنوان */
        .subtitle {
            font-size: 18px;
            color: #b8b8b8;
            margin-bottom: 24px;
            text-align: center;
        }
        
        /* تحسين أزرار الحساب */
        .stButton > button {
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            color: #e2e2e2 !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.1)) !important;
            border-color: rgba(255,255,255,0.3) !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* تحسين حقول الإدخال */
        .stNumberInput > div > div > input {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 8px !important;
            color: #e2e2e2 !important;
            padding: 8px 12px !important;
            transition: all 0.3s ease;
        }
        
        .stNumberInput > div > div > input:focus {
            border-color: rgba(255, 255, 255, 0.3) !important;
            box-shadow: 0 0 0 2px rgba(255,255,255,0.1) !important;
        }
        
        /* تحسين حقوق النشر */
        .copyright {
            text-align: center;
            color: rgba(255,255,255,0.5);
            padding: 16px;
            font-size: 14px;
            margin-top: 32px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }
        
        /* تحسين الشريط العلوي */
        .stProgress > div > div {
            background: rgba(30, 37, 48, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            overflow: hidden;
            position: relative;
            height: 48px !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }
        
        .stProgress > div > div > div {
            background: linear-gradient(90deg, 
                rgba(255,255,255,0.1),
                rgba(255,255,255,0.15),
                rgba(255,255,255,0.1)
            ) !important;
            border-radius: 6px !important;
            height: 100% !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(5px);
        }
        
        .stProgress > div > div::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.05),
                transparent
            );
            transition: all 0.5s ease;
            z-index: 1;
        }
        
        .stProgress > div > div:hover::before {
            left: 100%;
        }
        
        .stProgress > div > div:hover {
            background: rgba(22, 27, 37, 0.8) !important;
            border-color: rgba(255, 255, 255, 0.3) !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* تحديث شفافية القوائم المنسدلة */
        .stSelectbox > div > div,
        .stNumberInput > div > div {
            background: rgba(30, 37, 48, 0.7) !important;
            backdrop-filter: blur(10px);
        }
        
        .stSelectbox > div > div:hover,
        .stNumberInput > div > div:hover {
            background: rgba(22, 27, 37, 0.8) !important;
        }
        
        div[data-baseweb="select"] > div,
        div[data-baseweb="popover"] > div {
            background: rgba(30, 37, 48, 0.7) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        div[data-baseweb="select"] ul,
        div[data-baseweb="menu"] ul {
            background: rgba(30, 37, 48, 0.7) !important;
            backdrop-filter: blur(10px);
        }
        
        div[data-baseweb="select"] ul li:hover,
        div[data-baseweb="menu"] ul li:hover {
            background: rgba(22, 27, 37, 0.8) !important;
        }
        
        /* تحسين ملخص النتائج */
        pre {
            background: linear-gradient(45deg, 
                #1a1a2e,
                #16213e
            ) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 15px !important;
            padding: 20px !important;
            color: #ffffff !important;
            font-family: 'Courier New', monospace !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.3s ease !important;
            animation: gradientBG 15s ease infinite !important;
            background-size: 200% 200% !important;
        }

        pre:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            border-color: rgba(255, 255, 255, 0.2) !important;
        }

        /* تأثير الخلفية المتحركة */
        @keyframes gradientBG {
            0% {
                background: linear-gradient(45deg, 
                    #1a1a2e,
                    #16213e,
                    #0f3460
                );
                background-size: 200% 200%;
                background-position: 0% 50%;
            }
            50% {
                background: linear-gradient(45deg, 
                    #16213e,
                    #0f3460,
                    #1a1a2e
                );
                background-size: 200% 200%;
                background-position: 100% 50%;
            }
            100% {
                background: linear-gradient(45deg, 
                    #1a1a2e,
                    #16213e,
                    #0f3460
                );
                background-size: 200% 200%;
                background-position: 0% 50%;
            }
        }

        /* تنسيق النص داخل ملخص النتائج */
        pre code {
            color: #e2e2e2 !important;
            font-size: 1.1em !important;
            line-height: 1.5 !important;
        }

        /* تأثير الحدود المضيئة */
        pre::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            border-radius: 16px;
            background: linear-gradient(45deg, 
                #1a1a2e,
                #0f3460,
                #1a1a2e
            );
            z-index: -1;
            animation: borderGlow 3s ease-in-out infinite;
            opacity: 0.5;
        }

        @keyframes borderGlow {
            0% {
                opacity: 0.3;
            }
            50% {
                opacity: 0.6;
            }
            100% {
                opacity: 0.3;
            }
        }
        
        /* تنسيق العنوان الرئيسي */
        .main-title {
            font-size: 2.5em !important;
            font-weight: bold !important;
            text-align: center !important;
            margin-bottom: 1em !important;
            color: #ffffff !important;
            text-shadow: 0 0 10px rgba(255,255,255,0.3);
        }
        
        /* تأثير الإيموجي المتحرك */
        .chicken-emoji {
            display: inline-block;
            font-size: 2em;
            cursor: pointer;
            transition: all 0.3s ease;
            animation: float 2s ease-in-out infinite;
        }
        
        .chicken-emoji:hover {
            transform: scale(1.3) rotate(15deg);
        }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        
        /* تنسيق قسم "كم ربحت من الدجاجة" */
        .progress-section {
            background: linear-gradient(135deg, rgba(30, 37, 48, 0.7), rgba(20, 27, 38, 0.7));
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .progress-section:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            border-color: rgba(255, 255, 255, 0.2);
        }
        
        .progress-info {
            background: rgba(30, 37, 48, 0.5);
            border-radius: 8px;
            padding: 10px 15px;
            margin-bottom: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        
        .progress-info:hover {
            background: rgba(30, 37, 48, 0.7);
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .progress-label {
            display: block;
            font-size: 0.9em;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 5px;
        }
        
        .progress-value {
            display: block;
            font-size: 1.2em;
            font-weight: bold;
            color: white;
        }
        
        .progress-extras {
            font-size: 0.9em;
            color: rgba(255, 255, 255, 0.8);
            font-style: italic;
        }
        
        /* تحسين شريط التقدم */
        .stProgress > div > div {
            position: relative;
            height: 20px !important;
            background: rgba(20, 27, 38, 0.7) !important;
            border-radius: 10px !important;
            overflow: hidden;
            box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            margin: 10px 0 !important;
        }
        
        .stProgress > div > div > div {
            background: linear-gradient(90deg, 
                rgba(102, 187, 106, 0.8),
                rgba(102, 187, 106, 1.0)
            ) !important;
            box-shadow: 0 0 10px rgba(102, 187, 106, 0.5) !important;
            border-radius: 10px !important;
            height: 100% !important;
            transition: all 0.5s ease !important;
        }
        
        /* إضافة تأثير التوهج لشريط التقدم */
        .stProgress > div > div > div::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent,
                rgba(255, 255, 255, 0.3),
                transparent
            );
            animation: progressShine 2.5s ease-in-out infinite;
        }
        
        @keyframes progressShine {
            0% {
                transform: translateX(0%);
            }
            100% {
                transform: translateX(200%);
            }
        }
    </style>
""", unsafe_allow_html=True)

# دالة لتحديد لون شريط التقدم حسب النسبة
def get_progress_color(percentage):
    if percentage < 33:
        return "#FF5252"  # أحمر
    elif percentage < 66:
        return "#FFA726"  # برتقالي
    else:
        return "#66BB6A"  # أخضر

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تعريف النصوص بجميع اللغات
texts = {
    "العربية": {
        "title": "حاسبة الدجاج - نيويولك",
        "subtitle": "نيويولك توفر لك حاسبة أرباح دقيقة ومباشرة",
        "language": "اللغة 🌍",
        "currency": "العملة 💵",
        "egg_price": "سعر البيض الحالي 🥚",
        "feed_price": "سعر العلف الحالي 🌽",
        "save_prices": "حفظ الأسعار 💾",
        "calculation_type": "نوع الحساب 📊",
        "chicken_profits": "أرباح الدجاجة",
        "daily_rewards": "المكافآت اليومية",
        "eggs_input": "عدد البيض 🥚",
        "days_input": "عدد الأيام 📅",
        "food_input": "عدد الطعام المطلوب 🌽",
        "calculate_profits": "حساب الأرباح 🧮",
        "calculate_rewards": "حساب الربح اليومي 📈",
        "reset": "إعادة تعيين 🔄",
        "value": "القيمة",
        "category": "الفئة",
        "net_profit": "الربح في السنة الاولى 📈",
        "total_first_year_profit": "إجمالي الربح في السنة الاولى 📈",
        "total_rewards": "إجمالي عدد البيض اليومي 🥚",
        "total_food_cost": "اجمالي عدد العلف اليومي 🌽",
        "first_year_rental": "الإيجار للسنة الثانية 🏠",
        "final_profit": "الربح الصافي خلال السنتين 💰",
        "calculation_time": "وقت الحساب ⏰",
        "summary": "ملخص النتائج ✨",
        "usd_results": "النتائج بالدولار الأمريكي 💵",
        "iqd_results": "النتائج بالدينار العراقي 💵",
        "daily_profit": "الربح اليومي 📈",
        "am": "صباحاً",
        "pm": "مساءً",
        "copy_results": "نسخ النتائج",
        "group_calculation": "الحساب الجماعي",
        "chicken_number": "رقم الدجاجة",
        "add_chicken": "إضافة دجاجة",
        "daily_egg_rate": "عدد البيض الحالي",
        "active_days": "عدد الأيام النشطة",
        "chicken_details": "تفاصيل الدجاج",
        "egg_count": "عدد البيض",
        "income": "الدخل",
        "feed_cost": "تكلفة العلف",
        "rent": "الإيجار للسنة الثانية",
        "net_profit_per_chicken": "الربح الصافي خلال السنتين",
        "profit_with_sale": "📊 الربح مع بيع الدجاجة في السنة الاولى 📊",
        "chicken_sale_price": "سعر بيع الدجاجة (اختياري) 💰",
        "total_summary": "الملخص الإجمالي",
        "total_eggs": "إجمالي عدد البيض",
        "total_income": "إجمالي الدخل",
        "total_feed": "إجمالي تكلفة العلف",
        "total_rent": "إجمالي الإيجار للسنة الثانية",
        "total_net_profit": "إجمالي الربح الصافي خلال السنتين",
        "total_profit_with_sale": "إجمالي الربح الصافي مع بيع الدجاج خلال السنة الاولى 🐔",
        "remove_chicken": "حذف الدجاجة",
        "calculate_group": "حساب النتائج الجماعية",
        "no_chicken_data": "لا توجد بيانات دجاج مدخلة حتى الآن!",
        "not_first_year_chicken": "لا يمكن بيع الدجاجة لأنها ليست في السنة الأولى (عدد البيض أقل من 260)",
        "summary_egg_price": "مجموع سعر البيض 🥚",
        "summary_feed_price": "مجموع سعر العلف 🌽",
        "progress_title": "كم ربحت من الدجاجة 📊",
        "progress_percentage": "نسبة الإنجاز:",
        "max_potential_profit": "الربح المحتمل عند اكتمال دورة الدجاجة:",
        "current_vs_max": "ربحك الحالي مقارنة بالحد الأقصى:",
        "remaining_eggs": "عدد البيض المتبقي للوصول للحد الأقصى:",
        "remaining_days": "عدد الأيام المتبقية للوصول للحد الأقصى:",
        "completed_cycle": "أنت وصلت للحد الأقصى من دورة حياة الدجاجة!"
    },
    "English": {
        "title": "Chicken Calculator - NewYolk",
        "subtitle": "NewYolk Provides You With Accurate And Direct Profit Calculator",
        "language": "Language 🌍",
        "currency": "Currency 💵",
        "egg_price": "Current Egg Price 🥚",
        "feed_price": "Current Feed Price 🌽",
        "save_prices": "Save Prices 💾",
        "calculation_type": "Calculation Type 📊",
        "chicken_profits": "Chicken Profit",
        "daily_rewards": "Daily Rewards",
        "eggs_input": "Number of Eggs 🥚",
        "days_input": "Number of Days 📅",
        "food_input": "Amount of Food Needed 🌽",
        "calculate_profits": "Calculate Profits 🧮",
        "calculate_rewards": "Calculate Daily Profit 📈",
        "reset": "Reset 🔄",
        "value": "Value",
        "category": "Category",
        "net_profit": "First Year Profit 📈",
        "total_first_year_profit": "Total First Year Profit 📈",
        "total_rewards": "Total Daily Eggs Count 🥚",
        "total_food_cost": "Total Daily Feed Amount 🌽",
        "first_year_rental": "Second Year Rental 🏠",
        "final_profit": "Two Years Net Profit 💰",
        "calculation_time": "Calculation Time ⏰",
        "summary": "Results Summary ✨",
        "usd_results": "Results in USD 💵",
        "iqd_results": "Results in IQD 💵",
        "daily_profit": "Daily Profit 📈",
        "am": "AM",
        "pm": "PM",
        "copy_results": "Copy Results",
        "group_calculation": "Group Calculation",
        "chicken_number": "Chicken Number",
        "add_chicken": "Add Chicken",
        "daily_egg_rate": "Current Egg Count",
        "active_days": "Active Days",
        "chicken_details": "Chicken Details",
        "egg_count": "Egg Count",
        "income": "Income",
        "feed_cost": "Feed Cost",
        "rent": "Second Year Rental",
        "net_profit_per_chicken": "Two Years Net Profit",
        "profit_with_sale": "📊 First Year Profit With Chicken Sale 📊",
        "chicken_sale_price": "Chicken Sale Price (Optional) 💰",
        "total_summary": "Total Summary",
        "total_eggs": "Total Eggs",
        "total_income": "Total Income",
        "total_feed": "Total Feed Cost",
        "total_rent": "Total Second Year Rental",
        "total_net_profit": "Total Two Years Net Profit",
        "total_profit_with_sale": "Total Net Profit With Chicken Sale During First Year 🐔",
        "remove_chicken": "Remove Chicken",
        "calculate_group": "Calculate Group Results",
        "no_chicken_data": "No chicken data entered yet!",
        "not_first_year_chicken": "Chicken cannot be sold as it's not in the first year (egg count less than 260)",
        "summary_egg_price": "Total Egg Price 🥚",
        "summary_feed_price": "Total Feed Price 🌽",
        "progress_title": "How Much You've Earned From The Chicken 📊",
        "progress_percentage": "Achievement Percentage:",
        "max_potential_profit": "Maximum Potential Profit:",
        "current_vs_max": "Your Current Profit Compared to Maximum:",
        "remaining_eggs": "Remaining Eggs to Reach Maximum:",
        "remaining_days": "Remaining Days to Reach Maximum:",
        "completed_cycle": "You've reached the maximum chicken lifecycle!"
    },
    "Română": {
        "title": "Calculator Găini - NewYolk",
        "subtitle": "NewYolk Vă Oferă Un Calculator De Profit Precis Și Direct",
        "language": "Limbă 🌍",
        "currency": "Monedă 💵",
        "egg_price": "Preț Curent Ouă 🥚",
        "feed_price": "Preț Curent Furaje 🌽",
        "save_prices": "Salvează Prețurile 💾",
        "calculation_type": "Tipul Calculului 📊",
        "chicken_profits": "Profit Găină",
        "daily_rewards": "Recompensele Zilnice",
        "eggs_input": "Număr de Ouă 🥚",
        "days_input": "Număr de Zile 📅",
        "food_input": "Cantitate de Hrană Necesară 🌽",
        "calculate_profits": "Calculați Profiturile 🧮",
        "calculate_rewards": "Calculați Profitul Zilnic 📈",
        "reset": "Resetare 🔄",
        "value": "Valoare",
        "category": "Categorie",
        "net_profit": "Profit În Primul An 📈",
        "total_first_year_profit": "Profit Total În Primul An 📈",
        "total_rewards": "Numărul Total De Ouă Zilnice 🥚",
        "total_food_cost": "Cantitatea Totală De Furaje Zilnice 🌽",
        "first_year_rental": "Chirie Pentru Al Doilea An 🏠",
        "final_profit": "Profit Net În Cei Doi Ani 💰",
        "calculation_time": "Ora Calculului ⏰",
        "summary": "Rezumatul Rezultatelor ✨",
        "usd_results": "Rezultate în USD 💵",
        "iqd_results": "Rezultate în IQD 💵",
        "daily_profit": "Profit Zilnic 📈",
        "am": "AM",
        "pm": "PM",
        "copy_results": "Copiază Rezultatele",
        "group_calculation": "Calcul de Grup",
        "chicken_number": "Numărul Găinii",
        "add_chicken": "Adaugă Găină",
        "daily_egg_rate": "Numărul Actual de Ouă",
        "active_days": "Zile Active",
        "chicken_details": "Detalii Găini",
        "egg_count": "Număr Ouă",
        "income": "Venit",
        "feed_cost": "Cost Furaje",
        "rent": "Chirie Pentru Al Doilea An",
        "net_profit_per_chicken": "Profit Net În Cei Doi Ani",
        "profit_with_sale": "📊 Profit Din Primul An Cu Vânzarea Găinii 📊",
        "chicken_sale_price": "Preț Vânzare Găină (Opțional) 💰",
        "total_summary": "Rezumat Total",
        "total_eggs": "Total Ouă",
        "total_income": "Venit Total",
        "total_feed": "Cost Total Furaje",
        "total_rent": "Chirie Totală Pentru Al Doilea An",
        "total_net_profit": "Profit Net Total În Cei Doi Ani",
        "total_profit_with_sale": "Profit Net Total Cu Vânzarea Găinilor În Primul An 🐔",
        "remove_chicken": "Elimină Găina",
        "calculate_group": "Calculează Rezultatele de Grup",
        "no_chicken_data": "Nu există date despre găini introduse încă!",
        "not_first_year_chicken": "Găina nu poate fi vândută deoarece nu este în primul an (numărul de ouă mai mic de 260)",
        "summary_egg_price": "Preț Total Ouă 🥚",
        "summary_feed_price": "Preț Total Furaje 🌽",
        "progress_title": "Cât Ați Câștigat Din Găină 📊",
        "progress_percentage": "Procentajul de Realizare:",
        "max_potential_profit": "Profitul Maxim Potențial:",
        "current_vs_max": "Profitul Dvs. Actual Comparativ cu Maximul:",
        "remaining_eggs": "Ouă Rămase Pentru a Atinge Maximul:",
        "remaining_days": "Zile Rămase Pentru a Atinge Maximul:",
        "completed_cycle": "Ați atins ciclul maxim de viață al găinii!"
    }
}

# اختيار اللغة
language = st.selectbox(
    "اللغة | Language | Limbă 🌍",
    ["العربية", "English", "Română"],
    key="language_selector"
)

# تحسين الواجهة
st.markdown(
    f"""
    <style>
        .stApp {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
        }}
        .title {{
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            padding: 20px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .subtitle {{
            font-size: 24px;
            text-align: center;
            margin-bottom: 30px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .stButton {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
            text-align: {'right' if language == 'العربية' else 'left'};
            font-size: 24px;
        }}
        .stSelectbox, .stTextInput {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
            text-align: {'right' if language == 'العربية' else 'left'};
            font-size: 24px;
        }}
        .stButton button {{
            font-size: 24px;
            padding: 10px 24px;
            border-radius: 12px;
            width: 100%;
        }}
        .stTable th, .stTable td {{
            text-align: {'right' if language == 'العربية' else 'left'} !important;
            direction: {'rtl' if language == 'العربية' else 'ltr'} !important;
        }}
        [data-testid="stMarkdownContainer"] {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
            text-align: {'right' if language == 'العربية' else 'left'};
        }}
        .element-container {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
        }}
        thead tr th:first-child {{
            text-align: {'right' if language == 'العربية' else 'left'} !important;
        }}
        tbody tr td:first-child {{
            text-align: {'right' if language == 'العربية' else 'left'} !important;
        }}
    </style>
    <div class="main-title">
        {texts[language]["title"]}
        <a href="https://newyolkcalculator.streamlit.app" target="_blank" class="chicken-emoji">🐔</a>
        <div class="subtitle">
            {texts[language]["subtitle"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        .main-title {
            font-size: 2.5em !important;
            font-weight: bold !important;
            text-align: center !important;
            margin-bottom: 0.2em !important;
            color: #ffffff !important;
            text-shadow: 0 0 10px rgba(255,255,255,0.3);
        }
        
        .subtitle {
            font-size: 0.7em;
            text-align: center;
            margin-top: 0.5em;
            color: #e2e2e2;
            opacity: 0.9;
            font-weight: normal;
        }
        
        /* تنسيق قسم "كم ربحت من الدجاجة" */
        .progress-section {
            background: linear-gradient(135deg, rgba(30, 37, 48, 0.7), rgba(20, 27, 38, 0.7));
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .progress-section:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            border-color: rgba(255, 255, 255, 0.2);
        }
        
        .progress-info {
            background: rgba(30, 37, 48, 0.5);
            border-radius: 8px;
            padding: 10px 15px;
            margin-bottom: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        
        .progress-info:hover {
            background: rgba(30, 37, 48, 0.7);
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .progress-label {
            display: block;
            font-size: 0.9em;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 5px;
        }
        
        .progress-value {
            display: block;
            font-size: 1.2em;
            font-weight: bold;
            color: white;
        }
        
        .progress-extras {
            font-size: 0.9em;
            color: rgba(255, 255, 255, 0.8);
            font-style: italic;
        }
        
        /* تحسين شريط التقدم */
        .stProgress > div > div {
            position: relative;
            height: 20px !important;
            background: rgba(20, 27, 38, 0.7) !important;
            border-radius: 10px !important;
            overflow: hidden;
            box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            margin: 10px 0 !important;
        }
        
        .stProgress > div > div > div {
            background: linear-gradient(90deg, 
                rgba(102, 187, 106, 0.8),
                rgba(102, 187, 106, 1.0)
            ) !important;
            box-shadow: 0 0 10px rgba(102, 187, 106, 0.5) !important;
            border-radius: 10px !important;
            height: 100% !important;
            transition: all 0.5s ease !important;
        }
        
        /* إضافة تأثير التوهج لشريط التقدم */
        .stProgress > div > div > div::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, 
                transparent,
                rgba(255, 255, 255, 0.3),
                transparent
            );
            animation: progressShine 2.5s ease-in-out infinite;
        }
        
        @keyframes progressShine {
            0% {
                transform: translateX(0%);
            }
            100% {
                transform: translateX(200%);
            }
        }
    </style>
""", unsafe_allow_html=True)

# دالة التحقق من المدخلات
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# قسم تعديل الأسعار
st.subheader(texts[language]["save_prices"])
col3, col4 = st.columns(2)

with col3:
    new_egg_price = st.text_input(
        texts[language]["egg_price"],
        value="0.1185"
    )

with col4:
    new_feed_price = st.text_input(
        texts[language]["feed_price"],
        value="0.0196"
    )

if st.button(texts[language]["save_prices"], type="secondary"):
    if not is_number(new_egg_price) or not is_number(new_feed_price):
        st.error(get_error_message("invalid_number", language))
    else:
        st.success(get_error_message("save_success", language))

# تحديث الأسعار بناءً على العملة
if is_number(new_egg_price) and is_number(new_feed_price):
    if currency == "IQD":
        egg_price_display = float(new_egg_price) * 1480
        feed_price_display = float(new_feed_price) * 1480
    else:
        egg_price_display = float(new_egg_price)
        feed_price_display = float(new_feed_price)

    st.write(f"{texts[language]['egg_price']}: {format_decimal(egg_price_display)} {currency}")
    st.write(f"{texts[language]['feed_price']}: {format_decimal(feed_price_display)} {currency}")

# دالة إنشاء الرسم البياني
def create_profit_chart(df, language):
    # تخصيص الألوان
    colors = {
        texts[language]["total_eggs"]: '#4CAF50',
        texts[language]["total_feed"]: '#FF9800',
        texts[language]["total_first_year_profit"]: '#2196F3',
        texts[language]["total_rent"]: '#F44336',
        texts[language]["total_net_profit"]: '#9C27B0'
    }
    
    # إنشاء الرسم البياني
    fig = px.pie(
        df,
        values=texts[language]["value"],
        names=texts[language]["category"],
        title=texts[language]["summary"],
        color_discrete_sequence=['#4CAF50', '#FF9800', '#2196F3', '#F44336', '#9C27B0']
    )
    
    # تحديث تصميم الرسم البياني
    fig.update_traces(
        textposition='outside',
        textinfo='percent+label'
    )
    
    fig.update_layout(
        title_x=0.5,
        title_font_size=24,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=60, l=0, r=0, b=0),
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

if calculation_type == texts[language]["chicken_profits"]:
    st.subheader(texts[language]["chicken_profits"] + " 📈")
    col5, col6 = st.columns(2)

    with col5:
        eggs = st.text_input(
            texts[language]["eggs_input"],
            value="",
            help=get_help_message("eggs_input", language)
        )

    with col6:
        days = st.text_input(
            texts[language]["days_input"],
            value="",
            help=get_help_message("days_input", language)
        )

    # إضافة حقل سعر بيع الدجاجة
    try:
        eggs_value = float(eggs) if eggs else 0
        is_first_year = eggs_value >= 260
    except ValueError:
        is_first_year = False  # إذا لم يكن رقماً صحيحاً
        
    if is_first_year:
        chicken_sale_price = st.text_input(
            texts[language]["chicken_sale_price"],
            value=""
        )
    else:
        if eggs: # نظهر الرسالة فقط إذا أدخل المستخدم قيمة للبيض
            st.info(texts[language]["not_first_year_chicken"])
        chicken_sale_price = "0"

    if st.button(texts[language]["calculate_profits"], type="primary"):
        try:
            # التحويل من نص إلى رقم بشكل صحيح
            try:
                eggs_value = float(eggs) if eggs else None
                days_value = float(days) if days else None
                chicken_sale_price_value = float(chicken_sale_price) if chicken_sale_price else 0
            except ValueError:
                st.error(get_error_message("invalid_number", language))
                eggs_value = None
                days_value = None
                chicken_sale_price_value = 0

            if eggs_value is None or days_value is None:
                st.error(get_error_message("missing_values", language))
            elif eggs_value > 580:
                st.error(get_error_message("eggs_exceed", language))
            elif days_value > 730:
                st.error(get_error_message("days_exceed", language))
            else:
                # حساب الأرباح
                total_egg_price = eggs_value * float(new_egg_price)  # ضرب عدد البيض في سعر البيض الحالي
                total_feed_cost = (days_value * 2) * float(new_feed_price)  # ضرب عدد الأيام في 2 ثم في سعر العلف الحالي
                
                # حساب الإيجار
                total_rent = 6 if eggs_value >= 260 else 0  # 6 دولار فقط إذا كان عدد البيض 260 أو أكثر
                
                # حساب النتائج
                net_profit_before_rent = total_egg_price - total_feed_cost
                net_profit = net_profit_before_rent - total_rent
                
                # حساب الربح مع بيع الدجاجة - فقط للدجاج التي عدد بيضها 260 أو أكثر
                profit_with_sale = 0
                if eggs_value >= 260 and chicken_sale_price_value > 0:
                    profit_with_sale = net_profit_before_rent + chicken_sale_price_value
                
                # حساب الربح الأقصى المحتمل عند اكتمال دورة حياة الدجاجة (580 بيضة و730 يوم)
                max_eggs = 580
                max_days = 730
                max_total_egg_price = max_eggs * float(new_egg_price)
                max_total_feed_cost = (max_days * 2) * float(new_feed_price)
                max_total_rent = 6  # الإيجار للسنة الثانية
                max_net_profit_before_rent = max_total_egg_price - max_total_feed_cost
                max_net_profit = max_net_profit_before_rent - max_total_rent
                
                # حساب عدد البيض والأيام المتبقية للوصول إلى الحد الأقصى
                remaining_eggs = max(0, max_eggs - eggs_value)
                remaining_days = max(0, max_days - days_value)
                
                # حساب نسبة الإنجاز بناءً على الربح الحالي مقارنة بالربح الأقصى
                progress_percentage = min(100, (net_profit / max_net_profit * 100) if max_net_profit > 0 else 0)
                
                # تحديد لون شريط التقدم بناءً على النسبة
                progress_color = get_progress_color(progress_percentage)

                # تحويل العملة
                if currency == "IQD":
                    total_egg_price = total_egg_price * 1480
                    total_feed_cost = total_feed_cost * 1480
                    net_profit_before_rent = net_profit_before_rent * 1480
                    total_rent = total_rent * 1480
                    net_profit = net_profit * 1480
                    max_net_profit = max_net_profit * 1480
                    max_total_egg_price = max_total_egg_price * 1480
                    max_total_feed_cost = max_total_feed_cost * 1480
                    max_total_rent = max_total_rent * 1480
                    if profit_with_sale > 0:
                        profit_with_sale = profit_with_sale * 1480
                    chicken_sale_price_value = chicken_sale_price_value * 1480 if chicken_sale_price_value > 0 else 0
                else:
                    # الأسعار بالدولار تبقى كما هي
                    pass

                # تنسيق التاريخ والوقت حسب توقيت بغداد
                current_time = datetime.now() + timedelta(hours=3)  # تحويل التوقيت إلى توقيت بغداد
                date_str = current_time.strftime("%Y-%m-%d")
                time_str = current_time.strftime("%I:%M %p")

                # إنشاء نص النتائج مع إضافة الربح مع البيع
                results_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                  {texts[language]['summary']}                    ║
╠══════════════════════════════════════════════════════════════════╣
║ {texts[language]['calculation_time']}: {date_str} {time_str}
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['usd_results']}:
║ {texts[language]['summary_egg_price']}: {format_decimal(total_egg_price)} USD
║ {texts[language]['summary_feed_price']}: {format_decimal(total_feed_cost)} USD
║ {texts[language]['net_profit']}: {format_decimal(net_profit_before_rent)} USD"""

                # إضافة سعر البيع والربح مع البيع إذا كانت الدجاجة في السنة الأولى وتم إدخال سعر البيع
                if eggs_value >= 260 and chicken_sale_price_value > 0:
                    results_text += f"""
║ {texts[language]['chicken_sale_price']}: {format_decimal(chicken_sale_price_value)} USD
║ {texts[language]['profit_with_sale']}: {format_decimal(profit_with_sale)} USD"""

                # إضافة الإيجار والربح الصافي
                results_text += f"""
║ {texts[language]['first_year_rental']}: {format_decimal(total_rent)} USD
║ {texts[language]['final_profit']}: {format_decimal(net_profit)} USD"""

                # استكمال النص
                results_text += f"""
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['iqd_results']}:
║ {texts[language]['summary_egg_price']}: {format_decimal(total_egg_price * 1480)} IQD
║ {texts[language]['summary_feed_price']}: {format_decimal(total_feed_cost * 1480)} IQD
║ {texts[language]['net_profit']}: {format_decimal(net_profit_before_rent * 1480)} IQD"""

                # إضافة سعر البيع والربح مع البيع بالدينار العراقي
                if eggs_value >= 260 and chicken_sale_price_value > 0:
                    results_text += f"""
║ {texts[language]['chicken_sale_price']}: {format_decimal(chicken_sale_price_value * 1480)} IQD
║ {texts[language]['profit_with_sale']}: {format_decimal(profit_with_sale * 1480)} IQD"""

                # إضافة الإيجار والربح الصافي بالدينار العراقي
                results_text += f"""
║ {texts[language]['first_year_rental']}: {format_decimal(total_rent * 1480)} IQD
║ {texts[language]['final_profit']}: {format_decimal(net_profit * 1480)} IQD"""

                # إغلاق المربع
                results_text += """
╚══════════════════════════════════════════════════════════════════╝"""

                # إنشاء DataFrame للرسم البياني
                chart_categories = [
                        f"🥚 {texts[language]['eggs_input']}",
                        f"🌽 {texts[language]['food_input']}",
                        f"📈 {texts[language]['net_profit']}",
                ]
                
                chart_values = [
                        total_egg_price,
                        total_feed_cost,
                        net_profit_before_rent,
                ]
                
                # إضافة سعر البيع والربح مع البيع إلى الرسم البياني
                if eggs_value >= 260 and chicken_sale_price_value > 0:
                    chart_categories.append(f"💰 {texts[language]['chicken_sale_price']}")
                    chart_categories.append(f"📊 {texts[language]['profit_with_sale']}")
                    chart_values.append(chicken_sale_price_value)
                    chart_values.append(profit_with_sale)
                
                # إضافة الإيجار والربح الصافي في النهاية
                chart_categories.append(f"🏠 {texts[language]['first_year_rental']}")
                chart_categories.append(f"💰 {texts[language]['final_profit']}")
                chart_values.append(total_rent)
                chart_values.append(net_profit)
                
                df = pd.DataFrame({
                    texts[language]["category"]: chart_categories,
                    texts[language]["value"]: chart_values
                })
                
                # تنسيق الجدول النهائي أولاً
                df = df.round(2)
                df[texts[language]["value"]] = df[texts[language]["value"]].apply(lambda x: f"{format_decimal(x)} {currency}")
                st.table(df)

                # عرض الرسم البياني
                chart_df = pd.DataFrame({
                    texts[language]["category"]: chart_categories,
                    texts[language]["value"]: chart_values
                })
                fig = create_profit_chart(chart_df, language)
                st.plotly_chart(fig, use_container_width=True)

                # عرض ملخص النتائج في النهاية
                st.markdown(f"### ✨ {texts[language]['summary']}")
                st.code(results_text)
                
                # إضافة قسم "كم ربحت من الدجاجة"
                st.markdown(f"""
                <div style="text-align: center; margin: 30px 0 15px; position: relative;">
                    <hr style="height: 2px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent); border: none; margin-bottom: 20px;" />
                    <h3 style="font-size: 1.5em; font-weight: bold; color: white; text-shadow: 0 0 5px rgba(100,200,255,0.5);">
                        📊 {texts[language]['progress_title']}
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                # إنشاء قسم بتصميم خاص للميزة
                st.markdown('<div class="progress-section">', unsafe_allow_html=True)
                
                # عرض معلومات توضيحية
                if progress_percentage >= 100:
                    st.success(texts[language]['completed_cycle'])
                else:
                    st.info(f"{texts[language]['remaining_eggs']} {format_decimal(remaining_eggs)} 🥚 | {texts[language]['remaining_days']} {format_decimal(remaining_days)} 📅")
                
                # عرض شريط التقدم
                progress_bar = st.progress(min(progress_percentage/100, 1.0))
                
                # تغيير لون شريط التقدم حسب النسبة
                st.markdown(f"""
                <style>
                    .stProgress > div > div > div {{
                        background: linear-gradient(90deg, 
                            {progress_color}aa,
                            {progress_color}
                        ) !important;
                        box-shadow: 0 0 10px {progress_color}88 !important;
                        position: relative;
                        overflow: hidden;
                    }}
                    
                    .stProgress > div > div > div::after {{
                        content: '';
                        position: absolute;
                        top: 0;
                        left: -100%;
                        width: 100%;
                        height: 100%;
                        background: linear-gradient(90deg, 
                            transparent,
                            rgba(255, 255, 255, 0.3),
                            transparent
                        );
                        animation: progressShine 2.5s ease-in-out infinite;
                    }}
                    
                    @keyframes progressShine {{
                        0% {{ transform: translateX(0%); }}
                        100% {{ transform: translateX(200%); }}
                    }}
                </style>
                """, unsafe_allow_html=True)
                
                # عرض النسبة المئوية والربح المحتمل
                col_prog1, col_prog2 = st.columns(2)
                
                with col_prog1:
                    st.markdown(f"""
                    <div class="progress-info">
                        <span class="progress-label">{texts[language]['progress_percentage']}</span>
                        <span class="progress-value" style="color: {progress_color}; display: flex; align-items: center; gap: 5px;">
                            <span>📈</span> {format_decimal(progress_percentage)}%
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="progress-info">
                        <span class="progress-label">{texts[language]['current_vs_max']}</span>
                        <span class="progress-value" style="display: flex; align-items: center; gap: 5px;">
                            <span>💰</span> {format_decimal(net_profit)} / {format_decimal(max_net_profit)} {currency}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_prog2:
                    st.markdown(f"""
                    <div class="progress-info">
                        <span class="progress-label">{texts[language]['max_potential_profit']}</span>
                        <span class="progress-value" style="display: flex; align-items: center; gap: 5px;">
                            <span>💎</span> {format_decimal(max_net_profit)} {currency}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # معلومات إضافية عن الحد الأقصى
                    st.markdown(f"""
                    <div class="progress-info">
                        <span class="progress-extras">({format_decimal(max_eggs)} 🥚, {format_decimal(max_days)} 📅)</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # إغلاق قسم "كم ربحت من الدجاجة"
                st.markdown('</div>', unsafe_allow_html=True)
                
        except ValueError:
            st.error(get_error_message("invalid_number", language))
