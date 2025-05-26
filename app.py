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

# إضافة Font Awesome للأيقونات
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

# الأنماط والتصميم
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
        
        /* تحسين القوائم المنسدلة */
        .stSelectbox > div > div,
        .stNumberInput > div > div,
        .stTextInput > div > div {
            background: rgba(30, 37, 48, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 10px !important;
            color: #ffffff !important;
            backdrop-filter: blur(15px);
            transition: all 0.3s ease;
            padding: 12px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .stSelectbox > div > div:hover,
        .stNumberInput > div > div:hover,
        .stTextInput > div > div:hover {
            background: rgba(22, 27, 37, 0.9) !important;
            border-color: rgba(255, 255, 255, 0.4) !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        
        /* تحسين الأزرار */
        .stButton > button {
            background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05)) !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            padding: 12px 20px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(15px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, rgba(255,255,255,0.25), rgba(255,255,255,0.15)) !important;
            border-color: rgba(255,255,255,0.5) !important;
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }
        
        /* تحسين النصوص */
        .stSelectbox label, .stTextInput label {
            color: #ffffff !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            margin-bottom: 8px !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        }
        
        /* إخفاء رسائل المساعدة */
        .stNumberInput [data-testid="InputHelpText"],
        .stTextInput [data-testid="InputHelpText"] {
            display: none !important;
        }
        
        /* تحسين حقول الإدخال */
        .stNumberInput > div > div > input,
        .stTextInput > div > div > input {
            background: transparent !important;
            border: none !important;
            color: #ffffff !important;
            font-size: 16px !important;
        }
        
        .stNumberInput > div > div > input:focus,
        .stTextInput > div > div > input:focus {
            outline: none !important;
            box-shadow: none !important;
        }
        
        /* إخفاء أزرار الأرقام */
        input[type="number"]::-webkit-inner-spin-button, 
        input[type="number"]::-webkit-outer-spin-button { 
            -webkit-appearance: none; 
            margin: 0; 
        }
        
        input[type="number"] {
            -moz-appearance: textfield;
        }
        
        /* تحسين ملخص النتائج */
        pre {
            background: linear-gradient(135deg, 
                rgba(26, 26, 46, 0.9),
                rgba(22, 33, 62, 0.9)
            ) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 15px !important;
            padding: 25px !important;
            color: #ffffff !important;
            font-family: 'Courier New', monospace !important;
            backdrop-filter: blur(20px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.3);
            transition: all 0.3s ease !important;
        }

        pre:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
            border-color: rgba(255, 255, 255, 0.3) !important;
        }
        
        /* تنسيق العنوان الرئيسي */
        .main-title {
            font-size: 2.8em !important;
            font-weight: bold !important;
            text-align: center !important;
            margin-bottom: 0.5em !important;
            color: #ffffff !important;
            text-shadow: 0 0 15px rgba(255,255,255,0.4);
        }
        
        .subtitle {
            font-size: 0.6em;
            text-align: center;
            margin-top: 0.5em;
            color: #e2e2e2;
            opacity: 0.9;
            font-weight: normal;
        }
        
        /* تأثير الإيموجي المتحرك */
        .chicken-emoji {
            display: inline-block;
            font-size: 1.2em;
            cursor: pointer;
            transition: all 0.3s ease;
            animation: float 3s ease-in-out infinite;
            margin-left: 15px;
        }
        
        .chicken-emoji:hover {
            transform: scale(1.3) rotate(15deg);
            filter: drop-shadow(0 0 15px rgba(255,255,255,0.6));
        }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
            100% { transform: translateY(0px); }
        }
        
        /* زر العودة للأعلى - نقل إلى اليسار */
        .scroll-top-btn {
            position: fixed;
            bottom: 30px;
            left: 30px;
            width: 55px;
            height: 55px;
            background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            color: #ffffff;
            font-size: 20px;
            cursor: pointer;
            opacity: 0;
            visibility: hidden;
            transform: translateY(30px);
            transition: all 0.4s ease;
            z-index: 1000;
            backdrop-filter: blur(20px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .scroll-top-btn.active {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }
        
        .scroll-top-btn:hover {
            background: linear-gradient(135deg, rgba(255,255,255,0.25), rgba(255,255,255,0.15));
            border-color: rgba(255,255,255,0.5);
            transform: translateY(-5px) scale(1.1);
            box-shadow: 0 12px 35px rgba(0,0,0,0.4);
        }
        
        .scroll-top-btn i {
            animation: bounce 2.5s infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-4px); }
        }
        
        /* تحسين الجداول */
        .stTable {
            background: rgba(30, 37, 48, 0.8) !important;
            border-radius: 15px !important;
            backdrop-filter: blur(15px);
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }
        
        /* تحسين الروابط الاجتماعية */
        .social-links {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 40px 0 25px;
        }
        
        .social-links a {
            display: inline-block;
            transition: all 0.3s ease;
            padding: 10px;
            border-radius: 50%;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
        }
        
        .social-links img {
            width: 40px;
            height: 40px;
            filter: brightness(1.2);
            transition: all 0.3s ease;
        }
        
        .social-links a:hover {
            transform: translateY(-5px) scale(1.1);
            background: rgba(255,255,255,0.2);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
        
        .social-links a:hover img {
            filter: brightness(1.5);
        }
        
        /* تحسين حقوق النشر */
        .copyright {
            text-align: center;
            color: rgba(255,255,255,0.8);
            padding: 30px 0;
            font-size: 18px !important;
            margin-top: 40px;
            border-top: 1px solid rgba(255,255,255,0.2);
            font-weight: 500;
            letter-spacing: 1px;
            text-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)

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
        "first_year_profit": "ربح السنة الأولى 📈",
        "total_first_year_profit": "ربح السنة الأولى 📈",
        "total_rewards": "مجموع سعر عدد البيض 🥚",
        "total_food_cost": "مجموع عدد الطعام المطلوب 🌽",
        "first_year_rental": "الإيجار للسنة الثانية 🏠",
        "second_year_profit": "ربح السنة الثانية 📈",
        "second_year_profit_after_rent": "ربح السنة الثانية مع خصم الإيجار 📈",
        "final_profit": "الربح الصافي خلال السنتين بدون بيع 💰",
        "calculation_time": "وقت الحساب ⏰",
        "summary": "ملخص النتائج ✨",
        "usd_results": "النتائج بالدولار الأمريكي 💵",
        "iqd_results": "النتائج بالدينار العراقي 💵",
        "daily_profit": "الربح اليومي 📈",
        "group_calculation": "الحساب الجماعي",
        "chicken_number": "رقم الدجاجة",
        "add_chicken": "إضافة دجاجة",
        "daily_egg_rate": "عدد البيض الحالي",
        "active_days": "عدد الأيام النشطة",
        "chicken_details": "تفاصيل الدجاج",
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
        "net_profit": "الربح الصافي"
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
        "first_year_profit": "First Year Profit 📈",
        "total_first_year_profit": "First Year Profit 📈",
        "total_rewards": "Total Egg Price 🥚",
        "total_food_cost": "Total Required Feed Amount 🌽",
        "first_year_rental": "Second Year Rental 🏠",
        "second_year_profit": "Second Year Profit 📈",
        "second_year_profit_after_rent": "Second Year Profit After Rent 📈",
        "final_profit": "Two Years Net Profit Without Sale 💰",
        "calculation_time": "Calculation Time ⏰",
        "summary": "Results Summary ✨",
        "usd_results": "Results in USD 💵",
        "iqd_results": "Results in IQD 💵",
        "daily_profit": "Daily Profit 📈",
        "group_calculation": "Group Calculation",
        "chicken_number": "Chicken Number",
        "add_chicken": "Add Chicken",
        "daily_egg_rate": "Current Egg Count",
        "active_days": "Active Days",
        "chicken_details": "Chicken Details",
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
        "net_profit": "Net Profit"
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
        "first_year_profit": "Profit În Primul An 📈",
        "total_first_year_profit": "Profit În Primul An 📈",
        "total_rewards": "Preț Total Ouă 🥚",
        "total_food_cost": "Cantitate Totală De Furaje Necesară 🌽",
        "first_year_rental": "Chirie Pentru Al Doilea An 🏠",
        "second_year_profit": "Profit În Al Doilea An 📈",
        "second_year_profit_after_rent": "Profit Al Doilea An După Chirie 📈",
        "final_profit": "Profit Net În Cei Doi Ani Fără Vânzare 💰",
        "calculation_time": "Ora Calculului ⏰",
        "summary": "Rezumatul Rezultatelor ✨",
        "usd_results": "Rezultate în USD 💵",
        "iqd_results": "Rezultate în IQD 💵",
        "daily_profit": "Profit Zilnic 📈",
        "group_calculation": "Calcul de Grup",
        "chicken_number": "Numărul Găinii",
        "add_chicken": "Adaugă Găină",
        "daily_egg_rate": "Numărul Actual de Ouă",
        "active_days": "Zile Active",
        "chicken_details": "Detalii Găini",
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
        "net_profit": "Profit Net"
    }
}

# اختيار اللغة
language = st.selectbox(
    "اللغة | Language | Limbă 🌍",
    ["العربية", "English", "Română"],
    key="language_selector"
)

# تحسين الواجهة حسب اللغة
st.markdown(
    f"""
    <style>
        .stApp {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
        }}
        .stButton {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
        }}
        .stSelectbox, .stTextInput {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
        }}
        .stTable th, .stTable td {{
            text-align: {'right' if language == 'العربية' else 'left'} !important;
            direction: {'rtl' if language == 'العربية' else 'ltr'} !important;
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

# استخدام الأعمدة لتخطيط أفضل
col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox(
        texts[language]["currency"],
        ["USD", "IQD"]
    )

with col2:
    calculation_type = st.selectbox(
        texts[language]["calculation_type"],
        [texts[language]["chicken_profits"], texts[language]["daily_rewards"], texts[language]["group_calculation"]]
    )

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
    fig = px.pie(
        df,
        values=texts[language]["value"],
        names=texts[language]["category"],
        title=texts[language]["summary"],
        color_discrete_sequence=['#4CAF50', '#FF9800', '#2196F3', '#F44336', '#9C27B0']
    )
    
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

# دالة إنشاء نتائج موحدة لجميع اللغات
def create_unified_results(eggs_value, days_value, first_year_eggs, first_year_days, first_year_egg_price, 
                          first_year_feed_cost, first_year_profit, second_year_eggs, second_year_days, 
                          second_year_egg_price, second_year_feed_cost, second_year_profit, 
                          total_rent, second_year_profit_after_rent, net_profit, 
                          chicken_sale_price_value, profit_with_sale, current_time, language):
    
    date_str = current_time.strftime("%Y-%m-%d")
    time_str = current_time.strftime("%I:%M %p")
    
    results_text = f"""
║ {texts[language]['summary']} ✨

║ {texts[language]['calculation_time']} ⏰: {date_str} {time_str}
║ 
║ {texts[language]['usd_results']} 💵:
"""

    # عرض معلومات السنة الأولى فقط إذا كان عدد البيض أكبر من 260
    if eggs_value > 260:
        results_text += f"""║ 
║ السنة الأولى (حد أقصى 320 بيضة):
║ عدد البيض: {format_decimal(first_year_eggs)} 🥚
║ سعر البيض: {format_decimal(first_year_egg_price)} 💵
║ تكلفة العلف: {format_decimal(first_year_feed_cost)} 🌽
║ {texts[language]['first_year_profit']}: {format_decimal(first_year_profit)} 📈"""

        # إضافة سعر البيع والربح مع البيع إذا كان عدد البيض 320 أو أكثر
        if eggs_value >= 320 and chicken_sale_price_value > 0:
            results_text += f"""
║ {texts[language]['chicken_sale_price']}: {format_decimal(chicken_sale_price_value)} 💰
║ {texts[language]['profit_with_sale']}: {format_decimal(profit_with_sale)} 📈"""

    # عرض معلومات السنة الثانية
    if eggs_value <= 260:
        results_text += f"""║ 
║ السنة الثانية (حد أقصى 260 بيضة):
║ عدد البيض: {format_decimal(eggs_value)} 🥚
║ سعر البيض: {format_decimal(eggs_value * float(new_egg_price))} 💵
║ تكلفة العلف: {format_decimal((days_value * 2) * float(new_feed_price))} 🌽
║ {texts[language]['second_year_profit']}: {format_decimal((eggs_value * float(new_egg_price)) - ((days_value * 2) * float(new_feed_price)))} 📈
║ {texts[language]['final_profit']}: {format_decimal((eggs_value * float(new_egg_price)) - ((days_value * 2) * float(new_feed_price)))} 💰"""
    else:
        results_text += f"""║ 
║ السنة الثانية (حد أقصى 260 بيضة):
║ عدد البيض: {format_decimal(second_year_eggs)} 🥚
║ سعر البيض: {format_decimal(second_year_egg_price)} 💵
║ تكلفة العلف: {format_decimal(second_year_feed_cost)} 🌽
║ {texts[language]['first_year_rental']}: {format_decimal(total_rent)} 🏠
║ {texts[language]['second_year_profit']}: {format_decimal(second_year_profit)} 📈
║ {texts[language]['second_year_profit_after_rent']}: {format_decimal(second_year_profit_after_rent)} 📈
║ 
║ {texts[language]['final_profit']}: {format_decimal(net_profit)} 💰"""

    # استكمال النص بالدينار العراقي
    results_text += f"""

║ {texts[language]['iqd_results']} 💵:"""

    # عرض معلومات السنة الأولى بالدينار العراقي
    if eggs_value > 260:
        results_text += f"""║ 
║ السنة الأولى (حد أقصى 320 بيضة):
║ عدد البيض: {format_decimal(first_year_eggs)} 🥚
║ سعر البيض: {format_decimal(first_year_egg_price * 1480)} 💵
║ تكلفة العلف: {format_decimal(first_year_feed_cost * 1480)} 🌽
║ {texts[language]['first_year_profit']}: {format_decimal(first_year_profit * 1480)} 📈"""

        # إضافة سعر البيع والربح مع البيع بالدينار العراقي
        if eggs_value >= 320 and chicken_sale_price_value > 0:
            results_text += f"""
║ {texts[language]['chicken_sale_price']}: {format_decimal(chicken_sale_price_value * 1480)} 💰
║ {texts[language]['profit_with_sale']}: {format_decimal(profit_with_sale * 1480)} 📈"""

    # عرض معلومات السنة الثانية بالدينار العراقي
    if eggs_value <= 260:
        results_text += f"""║ 
║ السنة الثانية (حد أقصى 260 بيضة):
║ عدد البيض: {format_decimal(eggs_value)} 🥚
║ سعر البيض: {format_decimal((eggs_value * float(new_egg_price)) * 1480)} 💵
║ تكلفة العلف: {format_decimal(((days_value * 2) * float(new_feed_price)) * 1480)} 🌽
║ {texts[language]['second_year_profit']}: {format_decimal(((eggs_value * float(new_egg_price)) - ((days_value * 2) * float(new_feed_price))) * 1480)} 📈
║ {texts[language]['final_profit']}: {format_decimal(((eggs_value * float(new_egg_price)) - ((days_value * 2) * float(new_feed_price))) * 1480)} 💰"""
    else:
        results_text += f"""║ 
║ السنة الثانية (حد أقصى 260 بيضة):
║ عدد البيض: {format_decimal(second_year_eggs)} 🥚
║ سعر البيض: {format_decimal(second_year_egg_price * 1480)} 💵
║ تكلفة العلف: {format_decimal(second_year_feed_cost * 1480)} 🌽
║ {texts[language]['first_year_rental']}: {format_decimal(total_rent * 1480)} 🏠
║ {texts[language]['second_year_profit']}: {format_decimal(second_year_profit * 1480)} 📈
║ {texts[language]['second_year_profit_after_rent']}: {format_decimal(second_year_profit_after_rent * 1480)} 📈
║ 
║ {texts[language]['final_profit']}: {format_decimal(net_profit * 1480)} 💰"""

    return results_text

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
        is_first_year = False
        
    if is_first_year:
        chicken_sale_price = st.text_input(
            texts[language]["chicken_sale_price"],
            value=""
        )
    else:
        chicken_sale_price = "0"

    if st.button(texts[language]["calculate_profits"], type="primary"):
        try:
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
                # حساب الأرباح للسنة الأولى (320 بيضة كحد أقصى)
                first_year_eggs = min(eggs_value, 320)
                first_year_days = min(days_value, 365)
                first_year_egg_price = first_year_eggs * float(new_egg_price)
                first_year_feed_cost = (first_year_days * 2) * float(new_feed_price)
                first_year_profit = first_year_egg_price - first_year_feed_cost

                # حساب الأرباح للسنة الثانية (البيض المتبقي)
                second_year_eggs = max(0, min(eggs_value - 320, 260))
                second_year_days = max(0, min(days_value - 365, 365))
                second_year_egg_price = second_year_eggs * float(new_egg_price)
                second_year_feed_cost = (second_year_days * 2) * float(new_feed_price)
                
                # حساب الإيجار للسنة الثانية
                total_rent = 6 if eggs_value >= 320 else 0
                
                # حساب النتائج النهائية
                second_year_profit = second_year_egg_price - second_year_feed_cost
                second_year_profit_after_rent = second_year_profit - total_rent
                net_profit = first_year_profit + second_year_profit_after_rent
                
                # حساب الربح مع بيع الدجاجة
                profit_with_sale = 0
                if eggs_value >= 320 and chicken_sale_price_value > 0:
                    profit_with_sale = first_year_profit + chicken_sale_price_value

                # تنسيق التاريخ والوقت حسب توقيت بغداد
                current_time = datetime.now() + timedelta(hours=3)

                # إنشاء النتائج الموحدة
                results_text = create_unified_results(
                    eggs_value, days_value, first_year_eggs, first_year_days, first_year_egg_price,
                    first_year_feed_cost, first_year_profit, second_year_eggs, second_year_days,
                    second_year_egg_price, second_year_feed_cost, second_year_profit,
                    total_rent, second_year_profit_after_rent, net_profit,
                    chicken_sale_price_value, profit_with_sale, current_time, language
                )

                # تحويل العملة لعرض الجدول والرسم البياني
                if currency == "IQD":
                    first_year_profit = first_year_profit * 1480
                    second_year_profit_after_rent = second_year_profit_after_rent * 1480
                    net_profit = net_profit * 1480
                    if profit_with_sale > 0:
                        profit_with_sale = profit_with_sale * 1480
                    chicken_sale_price_value = chicken_sale_price_value * 1480 if chicken_sale_price_value > 0 else 0

                # إنشاء DataFrame للرسم البياني - بدون الأسعار في الفئات
                chart_categories = [
                    f"🥇 ربح السنة الأولى",
                    f"🥈 ربح السنة الثانية مع خصم الإيجار",
                    f"💰 الربح الصافي خلال السنتين بدون بيع"
                ]
                
                chart_values = [
                    first_year_profit,
                    second_year_profit_after_rent,
                    net_profit
                ]
                
                # إضافة سعر البيع إذا كان متاحاً
                if eggs_value >= 320 and chicken_sale_price_value > 0:
                    chart_categories.append(f"💰 ربح البيع")
                    chart_values.append(chicken_sale_price_value)
                
                df = pd.DataFrame({
                    texts[language]["category"]: chart_categories,
                    texts[language]["value"]: chart_values
                })
                
                # تنسيق الجدول النهائي
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
                
        except ValueError:
            st.error(get_error_message("invalid_number", language))

elif calculation_type == texts[language]["daily_rewards"]:
    st.subheader(texts[language]["daily_rewards"] + " 📈")
    col7, col8 = st.columns(2)

    with col7:
        rewards = st.text_input(
            texts[language]["total_rewards"],
            value="",
            help=get_help_message("rewards_input", language)
        )

    with col8:
        food = st.text_input(
            texts[language]["total_food_cost"],
            value="",
            help=get_help_message("food_input", language)
        )

    if st.button(texts[language]["calculate_rewards"], type="primary"):
        try:
            try:
                rewards_value = float(rewards) if rewards else None
                food_value = float(food) if food else None
            except ValueError:
                st.error(get_error_message("invalid_number", language))
                rewards_value = None
                food_value = None

            if rewards_value is None or food_value is None:
                st.error(get_error_message("missing_values", language))
            else:
                # حساب الربح اليومي
                daily_profit = rewards_value * float(new_egg_price) - food_value * float(new_feed_price)

                # تحويل العملة
                if currency == "IQD":
                    daily_profit = daily_profit * 1480

                # تنسيق التاريخ والوقت حسب توقيت بغداد
                current_time = datetime.now() + timedelta(hours=3)
                date_str = current_time.strftime("%Y-%m-%d")
                time_str = current_time.strftime("%I:%M %p")

                # إنشاء نص النتائج (نفس النمط المستخدم في العربية)
                results_text = f"""
║ {texts[language]['summary']} ✨

║ {texts[language]['calculation_time']} ⏰: {date_str} {time_str}
║ 
║ {texts[language]['usd_results']} 💵:
║ {texts[language]['summary_egg_price']}: {format_decimal(rewards_value * float(new_egg_price))} USD
║ {texts[language]['summary_feed_price']}: {format_decimal(food_value * float(new_feed_price))} USD
║ {texts[language]['daily_profit']}: {format_decimal(daily_profit)} USD

║ {texts[language]['iqd_results']} 💵:
║ {texts[language]['summary_egg_price']}: {format_decimal(rewards_value * float(new_egg_price) * 1480)} IQD
║ {texts[language]['summary_feed_price']}: {format_decimal(food_value * float(new_feed_price) * 1480)} IQD
║ {texts[language]['daily_profit']}: {format_decimal(daily_profit * 1480)} IQD"""

                # إنشاء DataFrame للرسم البياني - بدون الأسعار في الفئات
                df = pd.DataFrame({
                    texts[language]["category"]: [
                        f"🥚 {texts[language]['total_rewards']}",
                        f"🌽 {texts[language]['total_food_cost']}",
                        f"💰 {texts[language]['daily_profit']}"
                    ],
                    texts[language]["value"]: [
                        rewards_value * float(new_egg_price),
                        food_value * float(new_feed_price),
                        daily_profit
                    ]
                })
                
                # تنسيق القيم في الجدول
                df = df.round(2)
                df[texts[language]["value"]] = df[texts[language]["value"]].apply(lambda x: f"{format_decimal(x)} {currency}")
                st.table(df)

                # عرض الرسم البياني
                chart_df = pd.DataFrame({
                    texts[language]["category"]: [
                        f"🥚 {texts[language]['total_rewards']}",
                        f"🌽 {texts[language]['total_food_cost']}",
                        f"💰 {texts[language]['daily_profit']}"
                    ],
                    texts[language]["value"]: [
                        rewards_value * float(new_egg_price),
                        food_value * float(new_feed_price),
                        daily_profit
                    ]
                })
                fig = create_profit_chart(chart_df, language)
                st.plotly_chart(fig, use_container_width=True)

                # عرض ملخص النتائج في النهاية
                st.markdown(f"### ✨ {texts[language]['summary']}")
                st.code(results_text)
                
        except ValueError:
            st.error(get_error_message("invalid_number", language))

# إضافة قسم الحساب الجماعي
elif calculation_type == texts[language]["group_calculation"]:
    st.subheader(texts[language]["group_calculation"] + " 🐔")
    
    # إنشاء أو الوصول إلى جلسة لتخزين بيانات الدجاج
    if 'chicken_data' not in st.session_state:
        st.session_state.chicken_data = []
    
    # إضافة دجاجة جديدة
    st.subheader("➕ " + texts[language]["add_chicken"])
    col1, col2 = st.columns(2)
    
    with col1:
        egg_rate = st.text_input(
            texts[language]["daily_egg_rate"],
            value=""
        )
        
    with col2:
        active_days = st.text_input(
            texts[language]["active_days"],
            value=""
        )
        
    # حقل سعر بيع الدجاجة الاختياري
    try:
        egg_rate_value = float(egg_rate) if egg_rate else 0
        is_first_year = egg_rate_value >= 260
    except ValueError:
        is_first_year = False
        
    if is_first_year:
        chicken_sale_price = st.text_input(
            texts[language]["chicken_sale_price"],
            value=""
        )
    else:
        st.info(texts[language]["not_first_year_chicken"])
        chicken_sale_price = 0.0
        
    if st.button(texts[language]["add_chicken"], type="primary"):
        try:
            egg_rate = float(egg_rate) if egg_rate else None
            active_days = float(active_days) if active_days else None
            
            if "chicken_sale_price" not in locals():
                chicken_sale_price = "0"
            try:
                chicken_sale_price_value = float(chicken_sale_price) if chicken_sale_price else 0
            except ValueError:
                chicken_sale_price_value = 0
            
            if egg_rate is None or active_days is None:
                st.error(get_error_message("missing_values", language))
            elif egg_rate > 580:
                st.error(get_error_message("eggs_exceed", language))
            elif active_days > 730:
                st.error(get_error_message("days_exceed", language))
            else:
                eggs_count = egg_rate
                egg_income = eggs_count * float(new_egg_price)
                feed_cost = active_days * 2 * float(new_feed_price)
                rent = 6 if eggs_count >= 260 else 0
                net_profit_before_rent = egg_income - feed_cost
                net_profit = egg_income - feed_cost - rent
                
                if eggs_count >= 260 and chicken_sale_price_value > 0:
                    profit_with_sale = net_profit_before_rent + chicken_sale_price_value
                else:
                    profit_with_sale = 0
                    chicken_sale_price_value = 0.0
                
                chicken_id = len(st.session_state.chicken_data) + 1
                st.session_state.chicken_data.append({
                    "id": chicken_id,
                    "eggs": eggs_count,
                    "days": active_days,
                    "income": egg_income,
                    "feed_cost": feed_cost,
                    "rent": rent,
                    "net_profit_before_rent": net_profit_before_rent,
                    "net_profit": net_profit,
                    "chicken_sale_price": chicken_sale_price_value,
                    "profit_with_sale": profit_with_sale
                })
                
                st.success(get_error_message("chicken_added", language, chicken_id=chicken_id))
        except ValueError:
            st.error(get_error_message("invalid_number", language))
    
    # عرض الدجاج المضافة 
    if st.session_state.chicken_data:
        st.subheader("🧮 " + texts[language]["chicken_details"])
        
        for i, chicken in enumerate(st.session_state.chicken_data):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"🐔 {texts[language]['chicken_number']} {chicken['id']}: {texts[language]['eggs_input']}: {format_decimal(chicken['eggs'])}, {texts[language]['days_input']}: {format_decimal(chicken['days'])}")
            
            with col3:
                if st.button(f"❌ {texts[language]['remove_chicken']}", key=f"remove_{i}"):
                    st.session_state.chicken_data.pop(i)
                    st.rerun()
        
        # زر حساب النتائج الجماعية
        if st.button(texts[language]["calculate_group"], type="primary"):
            # إعداد الجدول التفصيلي
            detailed_df = pd.DataFrame([
                {
                    texts[language]["chicken_number"]: chicken["id"],
                    texts[language]["eggs_input"]: format_decimal(chicken["eggs"]),
                    texts[language]["days_input"]: format_decimal(chicken["days"]),
                    texts[language]["income"]: format_decimal(chicken["income"]),
                    texts[language]["feed_cost"]: format_decimal(chicken["feed_cost"]),
                    texts[language]["net_profit"]: format_decimal(chicken["net_profit_before_rent"]),
                    texts[language]["profit_with_sale"]: format_decimal(chicken["profit_with_sale"]) if chicken["eggs"] >= 260 and chicken["profit_with_sale"] > 0 else "",
                    texts[language]["rent"]: format_decimal(chicken["rent"]),
                    texts[language]["net_profit_per_chicken"]: format_decimal(chicken["net_profit"])
                }
                for chicken in st.session_state.chicken_data
            ])
            
            # حساب الإجماليات
            total_eggs = sum(chicken["eggs"] for chicken in st.session_state.chicken_data)
            total_income = sum(chicken["income"] for chicken in st.session_state.chicken_data)
            total_feed_cost = sum(chicken["feed_cost"] for chicken in st.session_state.chicken_data)
            total_rent = sum(chicken["rent"] for chicken in st.session_state.chicken_data)
            total_net_profit_before_rent = sum(chicken["net_profit_before_rent"] for chicken in st.session_state.chicken_data)
            total_net_profit = sum(chicken["net_profit"] for chicken in st.session_state.chicken_data)
            
            total_chicken_sale_prices = sum(chicken["chicken_sale_price"] for chicken in st.session_state.chicken_data if chicken["eggs"] >= 260 and chicken["chicken_sale_price"] > 0)
            total_profit_with_sale = total_net_profit_before_rent + total_chicken_sale_prices
            
            has_sales_prices = any(chicken["eggs"] >= 260 and chicken["chicken_sale_price"] > 0 for chicken in st.session_state.chicken_data)
            
            # تحويل العملة إذا لزم الأمر
            if currency == "IQD":
                conversion_rate = 1480
                total_income_display = total_income * conversion_rate
                total_feed_cost_display = total_feed_cost * conversion_rate
                total_rent_display = total_rent * conversion_rate
                total_net_profit_before_rent_display = total_net_profit_before_rent * conversion_rate
                total_net_profit_display = total_net_profit * conversion_rate
                total_profit_with_sale_display = total_profit_with_sale * conversion_rate
                display_currency = "IQD"
            else:
                total_income_display = total_income
                total_feed_cost_display = total_feed_cost
                total_rent_display = total_rent
                total_net_profit_before_rent_display = total_net_profit_before_rent
                total_net_profit_display = total_net_profit
                total_profit_with_sale_display = total_profit_with_sale
                display_currency = "USD"
                
            # عرض الجدول التفصيلي
            st.subheader("📋 " + texts[language]["chicken_details"])
            st.table(detailed_df)
            
            # إنشاء بيانات ملخص للرسم البياني
            summary_data = [
                {
                    texts[language]["category"]: texts[language]["total_eggs"],
                    texts[language]["value"]: f"{format_decimal(total_eggs)}"
                },
                {
                    texts[language]["category"]: texts[language]["total_income"],
                    texts[language]["value"]: f"{format_decimal(total_income_display)} {display_currency}"
                },
                {
                    texts[language]["category"]: texts[language]["total_feed"],
                    texts[language]["value"]: f"{format_decimal(total_feed_cost_display)} {display_currency}"
                },
                {
                    texts[language]["category"]: texts[language]["net_profit"],
                    texts[language]["value"]: f"{format_decimal(total_net_profit_before_rent_display)} {display_currency}"
                },
                {
                    texts[language]["category"]: texts[language]["total_profit_with_sale"],
                    texts[language]["value"]: f"{format_decimal(total_profit_with_sale_display)} {display_currency}"
                } if has_sales_prices else None,
                {
                    texts[language]["category"]: texts[language]["total_rent"],
                    texts[language]["value"]: f"{format_decimal(total_rent_display)} {display_currency}"
                },
                {
                    texts[language]["category"]: texts[language]["net_profit_per_chicken"],
                    texts[language]["value"]: f"{format_decimal(total_net_profit_display)} {display_currency}"
                }
            ]
            
            # إزالة القيم None من قائمة البيانات قبل إنشاء DataFrame
            filtered_summary_data = [item for item in summary_data if item is not None]
            summary_df = pd.DataFrame(filtered_summary_data)
            
            # عرض جدول الملخص الإجمالي
            st.subheader("📊 " + texts[language]["total_summary"])
            st.table(summary_df)
            
            # تنسيق التاريخ والوقت حسب توقيت بغداد
            current_time = datetime.now() + timedelta(hours=3)
            date_str = current_time.strftime("%Y-%m-%d")
            time_str = current_time.strftime("%I:%M %p")
            
            # إنشاء نص النتائج (نفس النمط المستخدم في العربية)
            results_text = f"""
║ {texts[language]['summary']} ✨

║ {texts[language]['calculation_time']} ⏰: {date_str} {time_str}
║ 
║ {texts[language]['usd_results']} 💵:
║ {texts[language]['total_eggs']}: {format_decimal(total_eggs)}
║ {texts[language]['total_income']}: {format_decimal(total_income)} USD
║ {texts[language]['total_feed']}: {format_decimal(total_feed_cost)} USD
║ {texts[language]['total_first_year_profit']}: {format_decimal(total_net_profit_before_rent)} USD
║ {texts[language]['total_rent']}: {format_decimal(total_rent)} USD
║ {texts[language]['total_net_profit']}: {format_decimal(total_net_profit)} USD
║ {texts[language]['total_profit_with_sale']}: {format_decimal(total_profit_with_sale)} USD

║ {texts[language]['iqd_results']} 💵:
║ {texts[language]['total_eggs']}: {format_decimal(total_eggs)}
║ {texts[language]['total_income']}: {format_decimal(total_income * 1480)} IQD
║ {texts[language]['total_feed']}: {format_decimal(total_feed_cost * 1480)} IQD
║ {texts[language]['total_first_year_profit']}: {format_decimal(total_net_profit_before_rent * 1480)} IQD
║ {texts[language]['total_rent']}: {format_decimal(total_rent * 1480)} IQD
║ {texts[language]['total_net_profit']}: {format_decimal(total_net_profit * 1480)} IQD
║ {texts[language]['total_profit_with_sale']}: {format_decimal(total_profit_with_sale * 1480)} IQD"""
            
            st.markdown(f"### ✨ {texts[language]['summary']}")
            st.code(results_text)
            
            # عرض الرسم البياني - بدون الأسعار في الفئات
            chart_df = pd.DataFrame({
                texts[language]["category"]: [
                    f"💰 {texts[language]['total_income']}",
                    f"🌽 {texts[language]['total_feed']}",
                    f"📈 {texts[language]['total_first_year_profit']}",
                    f"🏠 {texts[language]['total_rent']}",
                    f"💰 {texts[language]['total_net_profit']}"
                ],
                texts[language]["value"]: [
                    total_income_display,
                    total_feed_cost_display,
                    total_net_profit_before_rent_display,
                    total_rent_display,
                    total_net_profit_display
                ]
            })
            
            fig = px.pie(
                chart_df,
                values=texts[language]["value"],
                names=texts[language]["category"],
                title=texts[language]["total_summary"],
                color_discrete_sequence=['#4CAF50', '#FF9800', '#F44336', '#9C27B0']
            )
            
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
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(get_error_message("no_chicken_data", language))

# زر إعادة التعيين
if st.button(texts[language]["reset"], type="secondary"):
    if 'chicken_data' in st.session_state:
        st.session_state.chicken_data = []
    st.success(get_error_message("reset_success", language))
    st.rerun()

# إضافة الأيقونات والروابط
st.markdown("""
    <div class="social-links">
        <a href="https://farm.newyolk.io/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/3059/3059997.png" alt="Website">
        </a>
        <a href="https://discord.gg/RYDExGGWXh" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/5968/5968756.png" alt="Discord">
        </a>
        <a href="https://t.me/newyolkfarm" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" alt="Telegram">
        </a>
        <a href="https://www.facebook.com/newyolkfarming" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook">
        </a>
    </div>
    <div class="copyright">By Tariq Al-Yaseen &copy; 2025-2026</div>
    """,
    unsafe_allow_html=True
)

# إضافة زر العودة للأعلى
st.markdown("""
    <button id="scroll-top" class="scroll-top-btn">
        <i class="fas fa-chevron-up"></i>
    </button>
    
    <script>
        const scrollTopBtn = document.getElementById('scroll-top');
        
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollTopBtn.classList.add('active');
            } else {
                scrollTopBtn.classList.remove('active');
            }
        });
        
        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    </script>
    """,
    unsafe_allow_html=True
)