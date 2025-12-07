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
# Tag 字段即为分类依据
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
        background-color: #FAFAFA;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* 隐藏 Streamlit 默认头部 */
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

    /* 网格布局 */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
        gap: 24px;
        padding: 10px 0;
    }

    /* 卡片主体 */
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

    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: #3B82F6;
    }

    /* 图标盒子 */
    .icon-box {
        width: 48px;
        height: 48px;
        background: #EFF6FF;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin-bottom: 16px;
    }

    /* 文本内容 */
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
        flex-grow: 1;
    }
    
    /* 标签/分类 Pill */
    .tag {
        margin-top: 16px;
        font-size: 0.75rem;
        font-weight: 500;
        color: #3B82F6;
        background-color: #EFF6FF;
        padding: 4px 10px;
        border-radius: 9999px;
        text-transform: uppercase; /* 标签大写更具设计感 */
        letter-spacing: 0.05em;
    }

    a, a:hover, a:visited, a:active { text-decoration: none !important; }

    /* 优化 Multiselect 样式，使其更扁平 */
    span[data-baseweb="tag"] {
        background-color: #EFF6FF !important;
        border: 1px solid #BFDBFE !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF;
        border-color: #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. 页面布局与逻辑
# -------------------------------------------------------------

# 3.1 头部与地区切换
col_header, col_region = st.columns([3, 1])

with col_header:
    st.markdown('<div class="main-title">LegalTech Nexus</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Discover the world\'s leading legal & compliance platforms.</div>', unsafe_allow_html=True)

with col_region:
    # 地区切换
    region = st.radio(
        "Select Region",
        ["🇺🇸 USA", "🇨🇳 China"],
        horizontal=True,
        label_visibility="collapsed"
    )

# 3.2 确定当前数据源
current_key = "CN" if "China" in region else "US"
raw_items = DATA_SOURCE[current_key]

# -------------------------------------------------------------
# 4. 控制栏：搜索与分类过滤 (新增核心功能)
# -------------------------------------------------------------

# 动态提取当前地区的所有分类标签
available_tags = sorted(list(set(item['tag'] for item in raw_items)))

# 使用两列布局控制栏：左侧搜索，右侧过滤
c_search, c_filter = st.columns([1, 2])

with c_search:
    search_query = st.text_input(
        "Search", 
        placeholder="Search tools...", 
        label_visibility="collapsed"
    )

with c_filter:
    # 多选过滤器
    selected_categories = st.multiselect(
        "Filter by Category",
        options=available_tags,
        placeholder="Filter by category (e.g., Legal AI, Compliance...)",
        label_visibility="collapsed"
    )

# -------------------------------------------------------------
# 5. 数据过滤逻辑
# -------------------------------------------------------------
filtered_items = raw_items

# 1. 应用分类过滤
if selected_categories:
    filtered_items = [i for i in filtered_items if i['tag'] in selected_categories]

# 2. 应用搜索过滤
if search_query:
    query = search_query.lower()
    filtered_items = [i for i in filtered_items if query in i['name'].lower() or query in i['desc'].lower()]

# -------------------------------------------------------------
# 6. 生成卡片网格
# -------------------------------------------------------------

# 显示结果计数 (提升用户体验的小细节)
if len(filtered_items) == 0:
    st.info("No tools found matching your criteria.")
else:
    st.caption(f"Showing {len(filtered_items)} tools")

# 拼接 HTML
cards_html = '<div class="grid-container">'

for item in filtered_items:
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

# 渲染
st.markdown(cards_html, unsafe_allow_html=True)

# -------------------------------------------------------------
# 7. 页脚
# -------------------------------------------------------------
st.markdown("""
<div style="margin-top: 50px; text-align: center; color: #9CA3AF; font-size: 0.8rem;">
    © 2023 LegalTech Nexus. Filter, Explore, Connect.
</div>
""", unsafe_allow_html=True)
