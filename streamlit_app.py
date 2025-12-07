import streamlit as st

# -------------------------------------------------------------
# 1. 配置页面与数据
# -------------------------------------------------------------
st.set_page_config(
    page_title="LegalTech Nexus",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# 定义数据结构：中国 (CN) 和 美国 (US)
DATA_SOURCE = {
    "CN": [
        {"name": "裁判文书网", "desc": "全国法院裁判文书公开平台", "url": "https://wenshu.court.gov.cn", "icon": "⚖️", "tag": "官方司法"},
        {"name": "北大法宝", "desc": "中国最权威的法律法规数据库", "url": "https://www.pkulaw.com", "icon": "📚", "tag": "法律检索"},
        {"name": "天眼查", "desc": "商业安全工具与企业征信", "url": "https://www.tianyancha.com", "icon": "👁️", "tag": "合规调查"},
        {"name": "法大大", "desc": "电子合同与电子签章平台", "url": "https://www.fadada.com", "icon": "✍️", "tag": "合同科技"},
        {"name": "无讼", "desc": "互联网法律服务与案例检索", "url": "https://www.itslaw.com", "icon": "🔍", "tag": "法律服务"},
        {"name": "威科先行", "desc": "专业法律信息与实务指南", "url": "https://law.wkinfo.com.cn", "icon": "🧠", "tag": "外资合规"},
        {"name": "企查查", "desc": "企业信用信息查询平台", "url": "https://www.qcc.com", "icon": "🏢", "tag": "尽职调查"},
        {"name": "秘塔科技", "desc": "AI翻译与法律智能检索", "url": "https://www.metaso.cn", "icon": "🤖", "tag": "Legal AI"},
    ],
    "US": [
        {"name": "Westlaw", "desc": "Comprehensive legal research service", "url": "https://legal.thomsonreuters.com/en/products/westlaw", "icon": "🦅", "tag": "Research"},
        {"name": "LexisNexis", "desc": "Legal & professional information", "url": "https://www.lexisnexis.com", "icon": "🌐", "tag": "Analytics"},
        {"name": "Clio", "desc": "Cloud-based practice management", "url": "https://www.clio.com", "icon": "☁️", "tag": "Management"},
        {"name": "Ironclad", "desc": "Digital contracting platform", "url": "https://ironcladapp.com", "icon": "⛓️", "tag": "CLM"},
        {"name": "Carta", "desc": "Equity management & compliance", "url": "https://carta.com", "icon": "📈", "tag": "Equity"},
        {"name": "DocuSign", "desc": "Electronic signature & agreement cloud", "url": "https://www.docusign.com", "icon": "✒️", "tag": "eSignature"},
        {"name": "LegalZoom", "desc": "Online legal tech for small biz", "url": "https://www.legalzoom.com", "icon": "🚀", "tag": "Services"},
        {"name": "Harvey AI", "desc": "Generative AI for elite law firms", "url": "https://www.harvey.ai", "icon": "✨", "tag": "GenAI"},
    ]
}

# -------------------------------------------------------------
# 2. 注入自定义 CSS (硅谷风格)
# -------------------------------------------------------------
st.markdown("""
<style>
    /* 全局字体与背景 */
    .stApp {
        background-color: #FAFAFA; /* 极简灰白背景 */
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* 隐藏 Streamlit 默认头部装饰 */
    header[data-testid="stHeader"] {display: none;}
    
    /* 标题样式 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* 卡片网格布局 */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 24px;
        padding: 10px 0;
    }

    /* 卡片主体样式 */
    .card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 24px;
        text-decoration: none;
        transition: all 0.2s ease-in-out;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        height: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* 悬停效果：轻微上浮 + 阴影加深 */
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: #3B82F6; /* 悬停时边框变蓝 */
    }

    /* 图标容器 */
    .icon-box {
        width: 48px;
        height: 48px;
        background: #EFF6FF; /* 浅蓝背景 */
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin-bottom: 16px;
    }

    /* 文本样式 */
    .card-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1F2937;
        margin-bottom: 8px;
    }
    .card-desc {
        font-size: 0.875rem;
        color: #6B7280;
        line-height: 1.5;
        flex-grow: 1; /* 让描述占据剩余空间 */
    }
    
    /* 标签样式 */
    .tag {
        margin-top: 16px;
        font-size: 0.75rem;
        font-weight: 500;
        color: #3B82F6;
        background-color: #EFF6FF;
        padding: 4px 10px;
        border-radius: 9999px;
    }

    /* 强制移除链接下划线 */
    a, a:hover, a:visited, a:active {
        text-decoration: none !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. 页面布局逻辑
# -------------------------------------------------------------

# 3.1 头部区域 (Header)
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<div class="main-title">LegalTech Nexus</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Discover the world\'s leading legal & compliance platforms.</div>', unsafe_allow_html=True)

with col2:
    # 地区切换器 (使用 Segmented Control 风格)
    region = st.radio(
        "Select Region",
        ["🇺🇸 USA", "🇨🇳 China"],
        horizontal=True,
        label_visibility="collapsed"
    )

# 3.2 数据过滤
current_key = "CN" if "China" in region else "US"
items = DATA_SOURCE[current_key]

# 3.3 搜索栏 (可选增强功能)
search_query = st.text_input("", placeholder="Search for tools or companies...", label_visibility="collapsed")
if search_query:
    items = [i for i in items if search_query.lower() in i['name'].lower() or search_query.lower() in i['desc'].lower()]

# -------------------------------------------------------------
# 4. 生成卡片网格 (核心渲染)
# -------------------------------------------------------------

# 拼接 HTML 字符串
cards_html = '<div class="grid-container">'

for item in items:
    card = f"""
    <a href="{item['url']}" target="_blank" class="card">
        <div class="icon-box">{item['icon']}</div>
        <div class="card-name">{item['name']}</div>
        <div class="card-desc">{item['desc']}</div>
        <div class="tag">{item['tag']}</div>
    </a>
    """
    cards_html += card

cards_html += '</div>'

# 渲染 HTML
st.markdown(cards_html, unsafe_allow_html=True)

# -------------------------------------------------------------
# 5. 页脚
# -------------------------------------------------------------
st.markdown("""
<div style="margin-top: 50px; text-align: center; color: #9CA3AF; font-size: 0.8rem;">
    © 2023 LegalTech Nexus. Designed for minimalists.
</div>
""", unsafe_allow_html=True)
