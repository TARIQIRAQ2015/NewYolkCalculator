import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os

# استيراد رسائل الخطأ المترجمة
from error_messages_fix import get_error_message, get_help_message

# قراءة ملف CSS الخاص بالتحسينات المحمولة
def load_css(css_file):
    if os.path.exists(css_file):
        with open(css_file, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تعديل طريقة عرض كود النتائج
def display_code_result(results_text, language):
    # إضافة كلاس للكود لتحسين العرض على الأجهزة المحمولة
    st.markdown(f"### ✨ {texts[language]['summary']}")
    st.markdown('<div class="code-container">', unsafe_allow_html=True)
    st.code(results_text)
    st.markdown('</div>', unsafe_allow_html=True)

# تحسين طريقة عرض الجداول
def display_responsive_table(df, language):
    # استخدام CSS لجعل الجداول متجاوبة
    st.markdown('<div class="responsive-table-container">', unsafe_allow_html=True)
    st.table(df)
    st.markdown('</div>', unsafe_allow_html=True)

# تحسين الواجهة
st.set_page_config(
    page_title="New Yolk Calculator",
    page_icon="🐔",
    layout="wide"
)

# تطبيق تحسينات CSS للهواتف المحمولة
mobile_css = load_css("mobile_fixes.css")
if mobile_css:
    st.markdown(f"<style>{mobile_css}</style>", unsafe_allow_html=True)

# تعريف النصوص بجميع اللغات
texts = {
    "العربية": {
        "title": "حاسبة الدجاج - نيويولك",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
        "language": "اللغة 🌍",
        "currency": "العملة 💵",
        "egg_price": "سعر البيض الحالي 🥚",
        "feed_price": "سعر العلف الحالي 🌽",
        "save_prices": "حفظ الأسعار 💾",
        "calculation_type": "نوع الحساب 📊",
        "chicken_profits": "أرباح الدجاج",
        "daily_rewards": "المكافآت اليومية",
        "eggs_input": "عدد البيض 🥚",
        "days_input": "عدد الأيام 📅",
        "food_input": "عدد الطعام المطلوب 🌽",
        "calculate_profits": "حساب الأرباح 🧮",
        "calculate_rewards": "حساب المكافآت ✨",
        "reset": "إعادة تعيين 🔄",
        "value": "القيمة",
        "category": "الفئة",
        "net_profit": "الربح في السنة الاولى 📈",
        "total_first_year_profit": "إجمالي الربح في السنة الاولى 📈",
        "total_rewards": "إجمالي المكافآت ⭐",
        "total_food_cost": "اجمالي العلف 🌽",
        "first_year_rental": "الإيجار 🏠",
        "final_profit": "الربح الصافي 💰",
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
        "total_eggs": "إجمالي عدد البيض",
        "total_feed": "إجمالي تكلفة العلف",
        "total_net_profit": "إجمالي الربح الصافي",
        "not_first_year_chicken": "لا يمكن بيع الدجاجة لأنها ليست في السنة الأولى (عدد البيض أقل من 260)"
    },
    "English": {
        "title": "Chicken Calculator - NewYolk",
        "subtitle": "Calculate Chicken Profits and Daily Rewards",
        "language": "Language 🌍",
        "currency": "Currency 💵",
        "egg_price": "Current Egg Price 🥚",
        "feed_price": "Current Feed Price 🌽",
        "save_prices": "Save Prices 💾",
        "calculation_type": "Calculation Type 📊",
        "chicken_profits": "Chicken Profits",
        "daily_rewards": "Daily Rewards",
        "eggs_input": "Number of Eggs 🥚",
        "days_input": "Number of Days 📅",
        "food_input": "Amount of Food Needed 🌽",
        "calculate_profits": "Calculate Profits 🧮",
        "calculate_rewards": "Calculate Rewards ✨",
        "reset": "Reset 🔄",
        "value": "Value",
        "category": "Category",
        "net_profit": "First Year Profit 📈",
        "total_first_year_profit": "Total First Year Profit 📈",
        "total_rewards": "Total Rewards ⭐",
        "total_food_cost": "Total Feed 🌽",
        "first_year_rental": "Rental 🏠",
        "final_profit": "Final Profit 💰",
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
        "total_eggs": "Total Eggs",
        "total_feed": "Total Feed Cost",
        "total_net_profit": "Total Net Profit",
        "not_first_year_chicken": "Chicken cannot be sold as it's not in the first year (egg count less than 260)"
    },
    "Română": {
        "title": "Calculator Găini - NewYolk",
        "subtitle": "Calculați Profiturile din Găini și Recompensele Zilnice",
        "language": "Limbă 🌍",
        "currency": "Monedă 💵",
        "egg_price": "Preț Curent Ouă 🥚",
        "feed_price": "Preț Curent Furaje 🌽",
        "save_prices": "Salvează Prețurile 💾",
        "calculation_type": "Tipul Calculului 📊",
        "chicken_profits": "Profituri din Găini",
        "daily_rewards": "Recompensele Zilnice",
        "eggs_input": "Număr de Ouă 🥚",
        "days_input": "Număr de Zile 📅",
        "food_input": "Cantitate de Hrană Necesară 🌽",
        "calculate_profits": "Calculați Profiturile 🧮",
        "calculate_rewards": "Calculați Recompensele ✨",
        "reset": "Resetare 🔄",
        "value": "Valoare",
        "category": "Categorie",
        "net_profit": "Profit În Primul An 📈",
        "total_first_year_profit": "Profit Total În Primul An 📈",
        "total_rewards": "Total Recompense ⭐",
        "total_food_cost": "Total Furaje 🌽",
        "first_year_rental": "Chirie 🏠",
        "final_profit": "Profit Final 💰",
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
        "total_eggs": "Total Ouă",
        "total_feed": "Cost Total Furaje",
        "total_net_profit": "Profit Net Total",
        "not_first_year_chicken": "Găina nu poate fi vândută deoarece nu este în primul an (numărul de ouă mai mic de 260)"
    }
}

# اختيار اللغة
language = st.selectbox(
    "اللغة | Language | Limbă 🌍",
    ["العربية", "English", "Română"],
    key="language_selector"
)

# دالة التحقق من المدخلات
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# اختيار العملة ونوع الحساب
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
    
    # اختصار أسماء الفئات للأجهزة المحمولة
    mobile_names = []
    for name in df[texts[language]["category"]]:
        # استخراج الإيموجي والجزء الأول من النص فقط
        parts = name.split(' ', 1)
        emoji = parts[0] if parts and len(parts) > 0 else ''
        # إذا كان هناك نص بعد الإيموجي
        name_text = parts[1] if parts and len(parts) > 1 else name
        # أخذ أول كلمة فقط من النص
        first_word = name_text.split()[0] if ' ' in name_text else name_text
        mobile_names.append(f"{emoji} {first_word}")
    
    # إضافة العمود الجديد للأسماء المختصرة
    df = df.copy()  # لتجنب التحذير
    df["mobile_names"] = mobile_names
    
    # إنشاء الرسم البياني
    fig = px.pie(
        df,
        values=texts[language]["value"],
        names="mobile_names" if len(df) > 3 else texts[language]["category"],
        title=texts[language]["summary"],
        color_discrete_sequence=['#4CAF50', '#FF9800', '#2196F3', '#F44336', '#9C27B0']
    )
    
    # تحديث تصميم الرسم البياني
    fig.update_traces(
        textposition='outside',
        textinfo='percent',
        hoverinfo='label+percent+value',
        hovertemplate='%{label}<br>%{value:.2f}<br>%{percent}'
    )
    
    # تعديل التصميم ليكون متجاوباً مع الأجهزة المحمولة
    fig.update_layout(
        title_x=0.5,
        title_font_size=24,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,  # زيادة المسافة للأجهزة المحمولة
            xanchor="center",
            x=0.5,
            font=dict(size=10)  # تصغير حجم خط الأسطورة للأجهزة المحمولة
        ),
        margin=dict(t=60, l=10, r=10, b=80),  # تعديل الهوامش لتناسب الأجهزة المحمولة
        height=400,  # تقليل الارتفاع في الشاشات الصغيرة
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        autosize=True,  # تفعيل التغيير التلقائي للحجم
        font=dict(
            size=12,  # تصغير حجم الخط العام
        )
    )
    
    return fig

# واجهة التطبيق الرئيسية
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

    if st.button(texts[language]["calculate_profits"], type="primary"):
        try:
            # التحويل من نص إلى رقم بشكل صحيح
            try:
                eggs_value = float(eggs) if eggs else None
                days_value = float(days) if days else None
            except ValueError:
                st.error(get_error_message("invalid_number", language))
                eggs_value = None
                days_value = None

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

                # تحويل العملة
                if currency == "IQD":
                    total_egg_price = total_egg_price * 1480
                    total_feed_cost = total_feed_cost * 1480
                    net_profit_before_rent = net_profit_before_rent * 1480
                    total_rent = total_rent * 1480
                    net_profit = net_profit * 1480
                
                # تنسيق التاريخ والوقت
                current_time = datetime.now() + timedelta(hours=3)
                date_str = current_time.strftime("%Y-%m-%d")
                time_str = current_time.strftime("%I:%M %p")

                # إنشاء نص النتائج
                results_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                  {texts[language]['summary']}                    ║
╠══════════════════════════════════════════════════════════════════╣
║ {texts[language]['calculation_time']}: {date_str} {time_str}
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['usd_results']}:
║ {texts[language]['egg_price']}: {format_decimal(total_egg_price)} USD
║ {texts[language]['feed_price']}: {format_decimal(total_feed_cost)} USD
║ {texts[language]['net_profit']}: {format_decimal(net_profit_before_rent)} USD
║ {texts[language]['first_year_rental']}: {format_decimal(total_rent)} USD
║ {texts[language]['final_profit']}: {format_decimal(net_profit)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['iqd_results']}:
║ {texts[language]['egg_price']}: {format_decimal(total_egg_price * 1480)} IQD
║ {texts[language]['feed_price']}: {format_decimal(total_feed_cost * 1480)} IQD
║ {texts[language]['net_profit']}: {format_decimal(net_profit_before_rent * 1480)} IQD
║ {texts[language]['first_year_rental']}: {format_decimal(total_rent * 1480)} IQD
║ {texts[language]['final_profit']}: {format_decimal(net_profit * 1480)} IQD
╚══════════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                display_code_result(results_text, language)
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
            # التحويل من نص إلى رقم بشكل صحيح
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
                else:
                    daily_profit = daily_profit

                # تنسيق التاريخ والوقت
                current_time = datetime.now() + timedelta(hours=3)
                date_str = current_time.strftime("%Y-%m-%d")
                time_str = current_time.strftime("%I:%M %p")

                # إنشاء نص النتائج
                results_text = f"""
╔═════════════════════════════════════════════════════════════╗
║ {texts[language]['calculation_time']}: {date_str} {time_str}
╟┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┑
║ {texts[language]['usd_results']}:
║ {texts[language]['egg_price']}: {format_decimal(rewards_value * float(new_egg_price))} USD
║ {texts[language]['feed_price']}: {format_decimal(food_value * float(new_feed_price))} USD
║ {texts[language]['daily_profit']}: {format_decimal(daily_profit)} USD
╟┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┑
║ {texts[language]['iqd_results']}:
║ {texts[language]['egg_price']}: {format_decimal(rewards_value * float(new_egg_price) * 1480)} IQD
║ {texts[language]['feed_price']}: {format_decimal(food_value * float(new_feed_price) * 1480)} IQD
║ {texts[language]['daily_profit']}: {format_decimal(daily_profit * 1480)} IQD
╚═════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                display_code_result(results_text, language)
        except ValueError:
            st.error(get_error_message("invalid_number", language))

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
        
    # حقل سعر بيع الدجاجة الاختياري - يظهر شرطياً إذا كان عدد البيض أكبر من 260
    try:
        egg_rate_value = float(egg_rate) if egg_rate else 0
        is_first_year = egg_rate_value >= 260
    except ValueError:
        is_first_year = False  # إذا لم يكن رقماً صحيحاً
        
    if is_first_year:  # لا يظهر في حالة كان عدد البيض أقل من 260
        chicken_sale_price = st.text_input(
            texts[language]["chicken_sale_price"],
            value=""
        )
    else:
        st.info(texts[language]["not_first_year_chicken"])
        chicken_sale_price = "0.0"  # لا يمكن بيع الدجاجة لأنها ليست في السنة الأولى
        
    if st.button(texts[language]["add_chicken"], type="primary"):
        try:
            # التحويل من نص إلى رقم بشكل صحيح
            egg_rate = float(egg_rate) if egg_rate else None
            active_days = float(active_days) if active_days else None
            
            # التحقق من قيمة سعر بيع الدجاجة
            if "chicken_sale_price" not in locals():
                chicken_sale_price = "0"  # تعيين القيمة الافتراضية إذا لم تكن موجودة
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
                # حساب النتائج للدجاجة الحالية
                # إضافة كود حساب النتائج

                # إضافة البيانات إلى قائمة الدجاج
                chicken_id = len(st.session_state.chicken_data) + 1
                st.session_state.chicken_data.append({
                    "id": chicken_id,
                    "eggs": egg_rate,
                    "days": active_days,
                    # إضافة باقي البيانات المحسوبة
                })
                
                st.success(get_error_message("chicken_added", language, chicken_id=chicken_id))
        except ValueError:
            st.error(get_error_message("invalid_number", language))
    
    # عرض الدجاج المضافة
    if st.session_state.chicken_data:
        st.subheader("🧮 " + texts[language]["chicken_details"])
        # إضافة كود عرض تفاصيل الدجاج المضافة
    else:
        st.warning(get_error_message("no_chicken_data", language))

# زر إعادة التعيين
if st.button(texts[language]["reset"], type="secondary"):
    # مسح بيانات الدجاج المخزنة في session_state
    if 'chicken_data' in st.session_state:
        st.session_state.chicken_data = []
    st.success(get_error_message("reset_success", language))
    st.rerun() 