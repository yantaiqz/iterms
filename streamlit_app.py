import streamlit as st

LANG_OPTIONS = {
    "中文": "zh",
    "English": "en",
    "العربية": "ar",
    "Español": "es"
}

# 多语言标题映射
TITLE_MAP = {
    "中文": "全球财富金字塔",
    "English": "Global Wealth Pyramid",
    "العربية": "هرم الثروة العالمي",
    "Español": "Pirámide de riqueza global"
}

# 列布局（更精细的比例）
col1, col2, col3 = st.columns([0.1, 7, 1.9])

with col1:
    st.markdown("💎", unsafe_allow_html=True)  # 图标

with col2:
    # 初始默认标题
    st.session_state.setdefault("current_lang", "中文")
    st.markdown(
        f"<h1 style='margin: 0; padding: 0; font-size: 2rem;'>{TITLE_MAP[st.session_state.current_lang]}</h1>",
        unsafe_allow_html=True
    )

with col3:
    # 语言选择器（仅展示，无实际切换功能）
    selected_lang = st.selectbox(
        "",
        options=list(LANG_OPTIONS.keys()),
        index=list(LANG_OPTIONS.keys()).index(st.session_state.current_lang),
        key="lang_sel"
    )
    # 仅更新状态但不切换语言（实现“仅展示”）
    st.session_state.current_lang = selected_lang

# 样式优化
st.markdown("""
<style>
    div[data-testid="stSelectbox"] > div {
        height: 40px !important;
        margin-top: 10px;
    }
    div[data-testid="stSelectbox"] label {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)
