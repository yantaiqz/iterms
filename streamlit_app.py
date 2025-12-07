import streamlit as st

# -------------------------------------------------------------
# 1. 配置页面
# -------------------------------------------------------------
st.set_page_config(
    page_title="LegalTech Nexus Global",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------------
# 2. 国际化 UI 文本配置 (UI Text)
# -------------------------------------------------------------
UI_TEXT = {
    "EN": {
        "title": "LegalTech Nexus",
        "subtitle": "The curated directory of global legal technology & compliance resources.",
        "search_placeholder": "Search tools, descriptions...",
        "filter_placeholder": "Filter by Category",
        "filter_label": "Filter",
        "region_label": "Region",
        "lang_label": "Language",
        "footer": "© 2024 LegalTech Nexus. Connecting Global Law & Technology.",
        "no_result": "No tools found matching your criteria.",
        "showing": "Showing {} tools"
    },
    "ZH": {
        "title": "全球法律科技导航",
        "subtitle": "汇集全球顶尖法律科技、合规工具与司法资源。",
        "search_placeholder": "搜索工具名称或描述...",
        "filter_placeholder": "按分类筛选 (如: 法律检索, 合规...)",
        "filter_label": "分类筛选",
        "region_label": "选择地区",
        "lang_label": "界面语言",
        "footer": "© 2024 LegalTech Nexus. 连接法律与科技。",
        "no_result": "未找到匹配的工具。",
        "showing": "显示 {} 个工具"
    }
}

# -------------------------------------------------------------
# 3. 核心数据源 (按地区和分类组织)
# -------------------------------------------------------------
# 结构: Region -> Category -> List of Tools
DATA_SOURCE = {
    "🇨🇳 CN (China)": {
        "Official / Judiciary (官方司法)": [
            {"name": "裁判文书网", "desc": "Supreme Court's judgment database", "url": "https://wenshu.court.gov.cn", "icon": "⚖️"},
            {"name": "中国法律法规库", "desc": "Official laws & regulations database", "url": "https://flk.npc.gov.cn", "icon": "📜"},
            {"name": "执行信息公开网", "desc": "Enforcement information disclosure", "url": "http://zxgk.court.gov.cn", "icon": "🔨"},
            {"name": "知识产权局 (CNIPA)", "desc": "Patent & Trademark Office", "url": "https://www.cnipa.gov.cn", "icon": "®️"},
        ],
        "Research & Data (检索与数据)": [
            {"name": "北大法宝", "desc": "Leading legal research database", "url": "https://www.pkulaw.com", "icon": "📚"},
            {"name": "威科先行", "desc": "Professional legal insights (Wolters Kluwer)", "url": "https://law.wkinfo.com.cn", "icon": "🧠"},
            {"name": "无讼 (Itslaw)", "desc": "Litigation data & case search", "url": "https://www.itslaw.com", "icon": "🔍"},
        ],
        "Compliance & Credit (合规征信)": [
            {"name": "天眼查", "desc": "Business background check", "url": "https://www.tianyancha.com", "icon": "👁️"},
            {"name": "企查查", "desc": "Enterprise credit inquiry", "url": "https://www.qcc.com", "icon": "🏢"},
            {"name": "启信宝", "desc": "Business data intelligence", "url": "https://www.qixin.com", "icon": "📊"},
        ],
        "LegalTech / SaaS (法律科技)": [
            {"name": "法大大", "desc": "E-signature & contract management", "url": "https://www.fadada.com", "icon": "✍️"},
            {"name": "秘塔科技 (MetaSo)", "desc": "AI translation & search", "url": "https://www.metaso.cn", "icon": "🤖"},
            {"name": "e签宝", "desc": "Electronic signature services", "url": "https://www.esign.cn", "icon": "🔒"},
        ]
    },
    "🇺🇸 US (USA)": {
        "Legal Research": [
            {"name": "Westlaw", "desc": "Premium legal research (Thomson Reuters)", "url": "https://legal.thomsonreuters.com", "icon": "🦅"},
            {"name": "LexisNexis", "desc": "Legal research & risk solutions", "url": "https://www.lexisnexis.com", "icon": "🌐"},
            {"name": "Casetext", "desc": "AI-powered legal research (CoCounsel)", "url": "https://casetext.com", "icon": "🧠"},
        ],
        "Practice Management": [
            {"name": "Clio", "desc": "Cloud-based practice management", "url": "https://www.clio.com", "icon": "☁️"},
            {"name": "MyCase", "desc": "Case management software", "url": "https://www.mycase.com", "icon": "💼"},
        ],
        "Contracts (CLM)": [
            {"name": "Ironclad", "desc": "Digital contracting platform", "url": "https://ironcladapp.com", "icon": "⛓️"},
            {"name": "DocuSign", "desc": "Global standard for e-signature", "url": "https://www.docusign.com", "icon": "✒️"},
            {"name": "ContractBook", "desc": "End-to-end contract automation", "url": "https://contractbook.com", "icon": "📄"},
        ],
        "GenAI & Emerging": [
            {"name": "Harvey AI", "desc": "Generative AI for elite law firms", "url": "https://www.harvey.ai", "icon": "✨"},
            {"name": "LegalZoom", "desc": "Online legal help for SMBs", "url": "https://www.legalzoom.com", "icon": "🚀"},
        ]
    },
    "🇬🇧 UK (United Kingdom)": {
        "Official / Resources": [
            {"name": "legislation.gov.uk", "desc": "Official home of UK legislation", "url": "https://www.legislation.gov.uk", "icon": "🇬🇧"},
            {"name": "BAILII", "desc": "British & Irish Legal Info Institute", "url": "https://www.bailii.org", "icon": "🏛️"},
        ],
        "LegalTech": [
            {"name": "Luminance", "desc": "AI for document review", "url": "https://www.luminance.com", "icon": "💡"},
            {"name": "Juro", "desc": "All-in-one contract automation", "url": "https://juro.com", "icon": "⚡"},
            {"name": "vLex", "desc": "Intelligent legal research platform", "url": "https://vlex.com", "icon": "🌍"},
        ]
    },
    "🇭🇰 HK (Hong Kong)": {
        "Judiciary / Official": [
            {"name": "HKLII", "desc": "Hong Kong Legal Information Institute", "url": "https://www.hklii.org", "icon": "⚖️"},
            {"name": "e-Legislation", "desc": "Hong Kong e-Legislation (HKeL)", "url": "https://www.elegislation.gov.hk", "icon": "📜"},
            {"name": "IPD HK", "desc": "Intellectual Property Department", "url": "https://www.ipd.gov.hk", "icon": "®️"},
        ],
        "Firms / Services": [
            {"name": "The Law Society of HK", "desc": "Professional body for solicitors", "url": "https://www.hklawsoc.org.hk", "icon": "🏢"},
            {"name": "Zegal", "desc": "Legal software for businesses", "url": "https://zegal.com", "icon": "☁️"},
        ]
    },
    "🇯🇵 JP (Japan)": {
        "Research & Official": [
            {"name": "e-Gov Japan", "desc": "Portal of Official Statistics & Laws", "url": "https://www.e-gov.go.jp", "icon": "🇯🇵"},
            {"name": "Courts in Japan", "desc": "Judgments of the Supreme Court", "url": "https://www.courts.go.jp", "icon": "⚖️"},
        ],
        "LegalTech": [
            {"name": "Bengo4.com", "desc": "Largest lawyer portal & e-sign", "url": "https://www.bengo4.com", "icon": "👨‍⚖️"},
            {"name": "LegalOn Cloud", "desc": "AI contract review (fmr. LegalForce)", "url": "https://www.legalon-cloud.com", "icon": "🌩️"},
            {"name": "Holmes", "desc": "Contract lifecycle management", "url": "https://www.holmescloud.com", "icon": "🕵️"},
        ]
    },
    "🇩🇪 DE (Germany)": {
        "Research": [
            {"name": "Juris", "desc": "Legal Information System for Germany", "url": "https://www.juris.de", "icon": "🇩🇪"},
            {"name": "Beck-Online", "desc": "Leading legal database", "url": "https://beck-online.beck.de", "icon": "📕"},
            {"name": "Gesetze-im-internet", "desc": "Federal Law Gazette online", "url": "https://www.gesetze-im-internet.de", "icon": "§"},
        ],
        "Tech": [
            {"name": "BRYTER", "desc": "No-code service automation platform", "url": "https://bryter.com", "icon": "🔧"},
            {"name": "Legalos", "desc": "Legal tech platform", "url": "https://www.legalos.com", "icon": "🛡️"},
        ]
    },
    "🇫🇷 FR (France)": {
        "Official": [
            {"name": "Légifrance", "desc": "French public service for law", "url": "https://www.legifrance.gouv.fr", "icon": "🇫🇷"},
        ],
        "Innovation": [
            {"name": "Doctrine", "desc": "Legal intelligence platform", "url": "https://www.doctrine.fr", "icon": "🧠"},
            {"name": "Hyperlex", "desc": "Contract management & analysis", "url": "https://hyperlex.ai", "icon": "📝"},
        ]
    }
}

# -------------------------------------------------------------
# 4. 注入 CSS (硅谷极简风格 - 增强版)
# -------------------------------------------------------------
st.markdown("""
<style>
    /* 全局重置 */
    .stApp {
        background-color: #FAFAFA;
        color: #111827;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    header[data-testid="stHeader"] {display: none;}

    /* 标题系统 */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #111827 0%, #4B5563 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #6B7280;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    /* 分类标题 */
    .category-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #374151;
        margin-top: 32px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
    }
    .category-header::before {
        content: '';
        display: inline-block;
        width: 4px;
        height: 1.25rem;
        background-color: #3B82F6;
        margin-right: 12px;
        border-radius: 2px;
    }

    /* 卡片网格 */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 20px;
        margin-bottom: 20px;
    }

    /* 卡片设计 */
    .card {
        background: #FFFFFF;
        border: 1px solid #F3F4F6;
        border-radius: 12px;
        padding: 20px;
        text-decoration: none;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        height: 100%;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        position: relative;
        overflow: hidden;
    }

    /* 悬停微交互 */
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.08);
        border-color: #E5E7EB;
    }
    .card:hover .icon-box {
        background: #EFF6FF;
        transform: scale(1.05);
    }

    /* 图标与内容 */
    .card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }
    .icon-box {
        width: 40px;
        height: 40px;
        background: #F9FAFB;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        transition: all 0.2s ease;
        flex-shrink: 0;
    }
    .card-name {
        font-size: 1rem;
        font-weight: 600;
        color: #111827;
        line-height: 1.3;
    }
    .card-desc {
        font-size: 0.85rem;
        color: #6B7280;
        line-height: 1.5;
        flex-grow: 1;
    }
    
    /* 标签 */
    .tag {
        display: inline-block;
        margin-top: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        color: #6B7280;
        background-color: #F3F4F6;
        padding: 4px 8px;
        border-radius: 6px;
        align-self: flex-start;
    }

    /* 去除链接样式 */
    a, a:hover, a:visited { text-decoration: none !important; }

    /* Streamlit 组件微调 */
    .stRadio > div {gap: 16px;}
    div[data-baseweb="select"] > div {
        background-color: #FFF;
        border-color: #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 5. 状态管理与语言设置
# -------------------------------------------------------------
if 'lang' not in st.session_state:
    st.session_state.lang = "ZH"  # 默认中文

# 顶部栏布局
col_header, col_controls = st.columns([1.5, 2])

# 语言切换逻辑 (通过 Radio 实现，放在右上角更显眼)
with col_controls:
    c_region, c_lang = st.columns([2, 1])
    with c_lang:
        lang_select = st.selectbox(
            "Language / 语言", 
            ["中文", "English"], 
            index=0 if st.session_state.lang == "ZH" else 1,
            label_visibility="collapsed"
        )
        st.session_state.lang = "ZH" if lang_select == "中文" else "EN"

t = UI_TEXT[st.session_state.lang]

with col_header:
    st.markdown(f'<div class="main-title">{t["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-title">{t["subtitle"]}</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 6. 地区与数据加载
# -------------------------------------------------------------
with c_region:
    # 地区选择
    region_options = list(DATA_SOURCE.keys())
    selected_region = st.selectbox(
        t["region_label"], 
        region_options, 
        index=0, 
        label_visibility="collapsed"
    )

# 获取当前地区的数据字典 (Category -> List)
region_data = DATA_SOURCE[selected_region]

# 提取所有分类供过滤器使用
all_categories = list(region_data.keys())

# -------------------------------------------------------------
# 7. 控制栏：搜索与分类过滤
# -------------------------------------------------------------
col_search, col_filter = st.columns([1, 2])

with col_search:
    search_query = st.text_input(
        "Search", 
        placeholder=t["search_placeholder"], 
        label_visibility="collapsed"
    )

with col_filter:
    selected_cats = st.multiselect(
        t["filter_label"],
        options=all_categories,
        placeholder=t["filter_placeholder"],
        label_visibility="collapsed"
    )

# -------------------------------------------------------------
# 8. 渲染逻辑 (分组 vs 扁平)
# -------------------------------------------------------------

def render_grid(tools_list, category_name=None):
    """辅助函数：渲染一个工具列表的网格"""
    html = ""
    if category_name:
        html += f'<div class="category-header">{category_name}</div>'
    
    html += '<div class="grid-container">'
    for tool in tools_list:
        # 如果是搜索模式，可以在卡片上显示它所属的原始分类作为Tag
        display_tag = category_name if category_name else tool.get('tag', '')
        
        card = f"""
        <a href="{tool['url']}" target="_blank" class="card">
            <div class="card-header">
                <div class="icon-box">{tool['icon']}</div>
                <div class="card-name">{tool['name']}</div>
            </div>
            <div class="card-desc">{tool['desc']}</div>
            <div class="tag">{display_tag}</div>
        </a>
        """
        html += card
    html += '</div>'
    return html

final_html = ""
tool_count = 0

# --- 逻辑 A: 用户进行了搜索 ---
if search_query:
    # 扁平化所有数据进行搜索
    flat_results = []
    for cat, tools in region_data.items():
        # 如果选了分类，先过滤分类
        if selected_cats and cat not in selected_cats:
            continue
            
        for tool in tools:
            # 搜索匹配
            q = search_query.lower()
            if q in tool['name'].lower() or q in tool['desc'].lower():
                # 临时把分类名赋给 tag 字段，方便显示
                tool_copy = tool.copy()
                tool_copy['tag'] = cat 
                flat_results.append(tool_copy)
    
    if flat_results:
        tool_count = len(flat_results)
        final_html = render_grid(flat_results)
    else:
        st.info(t["no_result"])

# --- 逻辑 B: 用户仅选择了分类过滤，没有搜索词 ---
elif selected_cats:
    for cat in selected_cats:
        tools = region_data[cat]
        tool_count += len(tools)
        final_html += render_grid(tools, category_name=cat)

# --- 逻辑 C: 默认展示 (全部按分类分组) ---
else:
    for cat, tools in region_data.items():
        tool_count += len(tools)
        final_html += render_grid(tools, category_name=cat)

# -------------------------------------------------------------
# 9. 输出结果
# -------------------------------------------------------------
if tool_count > 0:
    st.caption(t["showing"].format(tool_count))
    st.markdown(final_html, unsafe_allow_html=True)

# 页脚
st.markdown(f"""
<div style="margin-top: 60px; border-top: 1px solid #E5E7EB; padding-top: 20px; text-align: center; color: #9CA3AF; font-size: 0.8rem;">
    {t["footer"]}
</div>
""", unsafe_allow_html=True)
