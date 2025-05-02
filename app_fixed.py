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
        # ... الباقي من النصوص كما هي ...
    },
    "English": {
        "title": "Chicken Calculator - NewYolk",
        "subtitle": "Calculate Chicken Profits and Daily Rewards",
        # ... الباقي من النصوص كما هي ...
    },
    "Română": {
        "title": "Calculator Găini - NewYolk",
        "subtitle": "Calculați Profiturile din Găini și Recompensele Zilnice",
        # ... الباقي من النصوص كما هي ...
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
                # حساب الأرباح (باقي الكود كما هو)...
                # عرض ملخص النتائج في النهاية
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
                # حساب الربح اليومي (باقي الكود كما هو)...
                # عرض ملخص النتائج في النهاية
                display_code_result(results_text, language)
        except ValueError:
            st.error(get_error_message("invalid_number", language))

# باقي الكود كما هو... 