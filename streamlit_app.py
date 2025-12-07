import streamlit as st
from urllib.parse import urlparse
import datetime

import json
import os

# 1. 注入 CSS 样式
st.markdown("""
<style>
    /* 底部导航栏容器 */
    .bottom-nav {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 60px !important;
        background-color: rgba(255, 255, 255, 0.90) !important; /* 半透明背景 */
        backdrop-filter: blur(16px) !important; /* 磨砂玻璃效果 */
        border-top: 1px solid rgba(226, 232, 240, 0.8) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-around !important; /* 均匀分布 */
        padding: 0 10px !important;
        z-index: 9999 !important;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.03) !important;
    }
    
    /* 导航项按钮 */
    .nav-item {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex: 1 !important;
        height: 40px !important;
        color: #94a3b8 !important;
        text-decoration: none !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        margin: 0 2px !important;
        white-space: nowrap !important;
    }
    
    .nav-item:hover {
        background-color: rgba(241, 245, 249, 0.8) !important;
        color: #64748b !important;
    }
    
    .nav-item.active {
        color: #2563eb !important;
        background-color: rgba(59, 130, 246, 0.1) !important;
    }
    
    /* 隐藏链接下划线 */
    .nav-item:hover, .nav-item:visited, .nav-item:active {
        text-decoration: none !important;
    }
    
    /* 调整主内容底部边距，防止被导航栏遮挡 */
    .stApp {
        padding-bottom: 80px !important;
    }
</style>
""", unsafe_allow_html=True)

COUNTER_FILE = "visit_stats.json"
def update_daily_visits():
    """读取并更新每日访问量"""
    try:
        today_str = datetime.date.today().isoformat()
        
        # 防止同一用户刷新页面导致计数增加
        if "has_counted" in st.session_state:
            if os.path.exists(COUNTER_FILE):
                with open(COUNTER_FILE, "r") as f:
                    return json.load(f).get("count", 0)
            return 0

        # 初始化数据结构
        data = {"date": today_str, "count": 0}
        
        # 读取现有文件
        if os.path.exists(COUNTER_FILE):
            try:
                with open(COUNTER_FILE, "r") as f:
                    file_data = json.load(f)
                    # 如果是当天，保留计数；如果是新的一天，计数重置(根据需求调整)
                    # 原代码逻辑是：如果日期匹配则累加，不匹配则重置为0开始
                    if file_data.get("date") == today_str:
                        data = file_data
            except:
                pass
        
        # 计数 +1 并写入
        data["count"] += 1
        with open(COUNTER_FILE, "w") as f:
            json.dump(data, f)
        
        # 标记该用户已统计
        st.session_state["has_counted"] = True
        return data["count"]
        
    except Exception as e:
        return 0

# 调用并显示
daily_visits = update_daily_visits()
st.caption(f"今日访问量: {daily_visits}")

# --- 权限配置 ---
FREE_PERIOD_SECONDS = 60      # 免费试用期 60 秒
ACCESS_DURATION_HOURS = 24    # 密码解锁后的访问时长 24 小时
UNLOCK_CODE = "vip24"        # 预设的解锁密码
# --- 配置结束 ---

# -------------------------------------------------------------
# --- 1. 初始化会话状态 ---
# -------------------------------------------------------------

# 'start_time': 首次访问时间，用于计算免费试用期
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.datetime.now()
    # 'access_status': 'free' (免费期), 'locked' (需解锁), 'unlocked' (已解锁)
    st.session_state.access_status = 'free'
    st.session_state.unlock_time = None # 记录密码解锁的时间点

# -------------------------------------------------------------
# --- 2. 检查访问状态和时间逻辑 ---
# -------------------------------------------------------------

current_time = datetime.datetime.now()
access_granted = False # 默认无权限

# 检查当前状态并更新
if st.session_state.access_status == 'free':
    time_elapsed = (current_time - st.session_state.start_time).total_seconds()
    
    if time_elapsed < FREE_PERIOD_SECONDS:
        # 仍在免费期内
        access_granted = True
        time_left = FREE_PERIOD_SECONDS - time_elapsed
        st.info(f"⏳ **免费试用中... 剩余 {time_left:.1f} 秒。**")
    else:
        # 免费期结束，进入锁定状态
        st.session_state.access_status = 'locked'
        st.session_state.start_time = None # 清除免费期计时
        st.rerun() # 强制刷新以立即显示锁定界面
        
elif st.session_state.access_status == 'unlocked':
    unlock_expiry = st.session_state.unlock_time + datetime.timedelta(hours=ACCESS_DURATION_HOURS)
    
    if current_time < unlock_expiry:
        # 在 24 小时有效期内
        access_granted = True
        time_left_delta = unlock_expiry - current_time
        hours = int(time_left_delta.total_seconds() // 3600)
        minutes = int((time_left_delta.total_seconds() % 3600) // 60)
        
        st.info(f"🔓 **付费权限剩余:** {hours} 小时 {minutes} 分钟")
    else:
        # 24 小时已过期，进入锁定状态
        st.session_state.access_status = 'locked'
        st.session_state.unlock_time = None
        st.rerun() # 强制刷新

# -------------------------------------------------------------
# --- 3. 锁定界面及密码输入 ---
# -------------------------------------------------------------

if not access_granted:
    st.error("🔒 **访问受限。免费试用期已结束！**")
    st.markdown(f"""
    <div style="background-color: #fff; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb; margin-top: 15px;">
        <p style="font-weight: 600; color: #1f2937; margin-bottom: 5px;">🔑 10元解锁无限制访问权限，获取代码链接 (请在微信中打开)</p>
        <p style="font-size: 0.9em; background-color: #eef2ff; padding: 8px; border-radius: 4px; overflow-wrap: break-word;">
            <code>#小程序://闲鱼/i4ahD0rqwGB5lba</code>
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("access_lock_form"):
        password_input = st.text_input("解锁代码:", type="password", key="password_input_key")
        submit_button = st.form_submit_button("验证并解锁")
        
        if submit_button:
            if password_input == UNLOCK_CODE:
                st.session_state.access_status = 'unlocked'
                st.session_state.unlock_time = datetime.datetime.now()
                st.success("🎉 解锁成功！您已获得 1 天访问权限。页面即将刷新...")
                st.rerun()
            else:
                st.error("❌ 代码错误，请重试。")
                
    # 强制停止脚本，隐藏所有受保护的内容
    st.stop()
# -------------------------------------------------------------
# 1. 页面配置
# -------------------------------------------------------------
st.set_page_config(
    page_title="Legal1000 Global",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# 2. 国际化 UI 文本
# -------------------------------------------------------------
UI_TEXT = {
    "EN": {
        "title": "LegalTech Global 1000",
        "subtitle": "Directory of top law firms, judiciary & compliance resources across 50+ economies.",
        "search_placeholder": "Search for firms, tools, or agencies globally...",
        "region_group_label": "Select Region Group",
        "country_label": "Select Jurisdiction",
        "filter_label": "Filter Categories",
        "filter_placeholder": "Filter by Category",  # <--- 之前漏了这行
        "footer": "© 2025 Legal1000 Global. Logos via Google API.",
        "no_result": "No resources found.",
        "showing": "Showing {} resources",
        "nav_1": "Wealth Rank",
        "nav_2": "Global Real Estate",
        "nav_3": "City Housing",
        "nav_4": "Global Legal",
        "nav_5": "Global Enterprises",
        "nav_6": "Contract Review",
        "nav_7": "German Tax",
        "nav_8": "Shenzhen Property"
    },
    "ZH": {
        "title": "全球法律与科技 The Legal 1000",
        "subtitle": "汇集全球 1000+ 经济体的顶尖律所、司法资源与合规工具。",
        "search_placeholder": "搜索全球律所、工具或监管机构...",
        "region_group_label": "选择区域板块",
        "country_label": "选择司法管辖区",
        "filter_label": "分类筛选",
        "filter_placeholder": "按分类筛选",  # <--- 之前漏了这行
        "footer": "© 2024 LegalTech Nexus. Logo 由 Google API 自动生成。",
        "no_result": "未找到匹配资源。",
        "showing": "共显示 {} 个资源",
        "nav_1": "财富排行",
        "nav_2": "世界房产",
        "nav_3": "城市房价",
        "nav_4": "全球法律",
        "nav_5": "全球企业",
        "nav_6": "合同审查",
        "nav_7": "德国财税",
        "nav_8": "深圳房市"
    }
}

# -------------------------------------------------------------
# 3. 核心大数据库 (按区域分组)
# -------------------------------------------------------------

# 为了代码整洁，定义通用分类图标
ICONS = {
    "firm": "⚖️", "official": "🏛️", "tech": "💻", "research": "📚", "compliance": "🛡️"
}

# 数据结构：区域组 -> 国家 -> 分类 -> 列表
DATA_SOURCE = {

    # ================= 🌏 亚太地区 (Asia Pacific) =================
    "🌏 Asia Pacific (亚太)": {
        "🇨🇳 China (中国)": {
            "🤖 LegalTech & Data (科技/数据)": [
                {"name": "法大大", "url": "https://www.fadada.com", "desc": "E-Signature Platform"},
                {"name": "iTerms", "url": "https://www.iterms.com", "desc": "AI Contract Revew"},
                {"name": "北大法宝", "url": "https://www.pkulaw.com", "desc": "Leading Legal Database"},
                {"name": "威科先行", "url": "https://law.wkinfo.com.cn", "desc": "Wolters Kluwer China"},
                {"name": "无讼", "url": "https://www.itslaw.com", "desc": "Litigation Data"},
                {"name": "天眼查", "url": "https://www.tianyancha.com", "desc": "Business Data"},
                {"name": "企查查", "url": "https://www.qcc.com", "desc": "Credit Info"},
                {"name": "秘塔科技", "url": "https://www.metaso.cn", "desc": "AI Search"},
                {"name": "幂律智能", "url": "https://www.powerlaw.ai", "desc": "AI Contract Review"},
                {"name": "理脉", "url": "https://www.legalminer.com", "desc": "Legal Big Data"},
                {"name": "法天使", "url": "https://www.fats.cn", "desc": "Contract Templates"},
                {"name": "华宇信息", "url": "https://www.thunisoft.com", "desc": "Court Information Systems"},
                {"name": "国双 (Gridsum)", "url": "http://www.gridsum.com", "desc": "Judicial Big Data"},
            ],
            "🏛️ Red Circle & Top Firms (红圈/顶级律所)": [
                {"name": "金杜 (KWM)", "url": "https://www.kwm.com", "desc": "Red Circle Elite"},
                {"name": "君合 (JunHe)", "url": "https://www.junhe.com", "desc": "Premier Commercial Firm"},
                {"name": "中伦 (Zhong Lun)", "url": "https://www.zhonglun.com", "desc": "Full Service Giant"},
                {"name": "方达 (Fangda)", "url": "https://www.fangdalaw.com", "desc": "M&A and Capital Markets"},
                {"name": "海问 (Haiwen)", "url": "https://www.haiwen-law.com", "desc": "Prestigious Securities"},
                {"name": "汉坤 (Han Kun)", "url": "https://www.hankunlaw.com", "desc": "Leading in PE/VC & Tech"},
                {"name": "竞天公诚 (Jingtian)", "url": "http://www.jingtian.com", "desc": "Capital Markets Specialist"},
                {"name": "通商 (C&F)", "url": "http://www.tongshang.com", "desc": "Capital Markets & Dispute"},
                {"name": "环球 (Global Law)", "url": "http://www.glo.com.cn", "desc": "Oldest PRC Firm"},
                {"name": "天同 (Tiantong)", "url": "https://www.tiantonglaw.com", "desc": "Supreme Court Litigation"},
                {"name": "植德 (Merits & Tree)", "url": "http://www.meritsandtree.com", "desc": "Asset Management"},
            ],
            "🏙️ Major Commercial Firms (大型综合律所)": [
                {"name": "锦天城 (AllBright)", "url": "https://www.allbrightlaw.com", "desc": "Shanghai-based Giant"},
                {"name": "大成 (Dentons CN)", "url": "https://www.dentons.com.cn", "desc": "Largest Global Coverage"},
                {"name": "盈科 (Yingke)", "url": "http://www.yingkelawyer.com", "desc": "Global Network Firm"},
                {"name": "国浩 (Grandall)", "url": "http://www.grandall.com.cn", "desc": "IPO/Securities Focus"},
                {"name": "天元 (Tian Yuan)", "url": "http://www.tylaw.com.cn", "desc": "Comprehensive Practice"},
                {"name": "中银 (Zhong Yin)", "url": "http://www.zhongyinlawyer.com", "desc": "Banking & Finance"},
                {"name": "德恒 (DeHeng)", "url": "http://www.dehenglaw.com", "desc": "Govt & Infrastructure"},
                {"name": "京师 (Jingsh)", "url": "http://www.jingsh.com", "desc": "Large Scale Partnership"},
                {"name": "隆安 (Long An)", "url": "http://www.longanlaw.com", "desc": "IP & Commercial"},
                {"name": "炜衡 (Weiheng)", "url": "http://www.weihenglaw.com", "desc": "Comprehensive Litigation"},
                {"name": "康达 (Kangda)", "url": "http://www.kangdalawyers.com", "desc": "Criminal Defense"},
                {"name": "泰和泰 (Tahota)", "url": "http://www.tahota.com", "desc": "Leading West China Firm"},
                {"name": "建纬 (City Development)", "url": "http://www.jianwei.com", "desc": "Construction & RE"},
                {"name": "广悦 (Guangyue)", "url": "http://www.guangyuelaw.com", "desc": "Guangzhou Leading"},
                {"name": "安杰世泽 (AnJie Broad)", "url": "http://www.anjielaw.com", "desc": "Insurance & Antitrust"},
                {"name": "汇业 (Hui Ye)", "url": "http://www.huiyelaw.com", "desc": "Corporate & Compliance"},
                {"name": "中伦文德 (ZW)", "url": "http://www.zlwd.com", "desc": "Insurance & Dispute"},
                {"name": "融孚 (Rong Fu)", "url": "http://www.rongfulaw.com", "desc": "Finance & Real Estate"},
                {"name": "万商天勤 (WS)", "url": "http://www.wandl-law.com", "desc": "Commercial & Dispute"},
                {"name": "法兰克 (Frank)", "url": "http://www.franklawfirm.com", "desc": "IP & Tech"},
                {"name": "浩天 (Hao Tian)", "url": "http://www.haotianlawyers.com", "desc": "Dispute Resolution"},
            ],
            "🔬 IP & Boutique (知识产权/精品)": [
                {"name": "CCPIT Patent (贸促会)", "url": "https://www.ccpit-patent.com.cn", "desc": "Oldest IP Agency"},
                {"name": "Lung Tin (隆天)", "url": "http://www.lungtin.com", "desc": "IP Litigation"},
                {"name": "Liu, Shen (柳沈)", "url": "http://www.liushen.com", "desc": "Patent Prosecution"},
                {"name": "Wanhuida (万慧达)", "url": "http://www.wanhuida.com", "desc": "Trademark & IP"},
                {"name": "Merits & Tree (植德)", "url": "http://www.meritsandtree.com", "desc": "Asset Management"},
                {"name": "Llinks (通力)", "url": "http://www.llinkslaw.com", "desc": "Financial Law"},
                {"name": "AnJie Broad (安杰世泽)", "url": "http://www.anjielaw.com", "desc": "Antitrust & Insurance"},
            ],
             "💼 Compliance & Consulting (合规/四大)": [
                {"name": "普华永道 (PwC Legal)", "url": "https://www.pwccn.com", "desc": "Legal & Tax Services"},
                {"name": "德勤 (Deloitte Legal)", "url": "https://www2.deloitte.com/cn", "desc": "Legal Consulting"},
                {"name": "安永 (EY Law)", "url": "https://www.ey.com/cn", "desc": "Corporate Law Services"},
                {"name": "毕马威 (KPMG Law)", "url": "https://home.kpmg/cn", "desc": "Legal Compliance"},
                {"name": "甫瀚咨询 (Protiviti)", "url": "https://www.protiviti.com", "desc": "Risk & Compliance"},
                {"name": "贝克顾法律 (Baker & McKenzie CN)", "url": "https://www.bakermckenzie.com", "desc": "Foreign Law Firm"},
            ],
            "⚖️ Official & Judiciary (官方司法/监管)": [
                {"name": "裁判文书网", "url": "https://wenshu.court.gov.cn", "desc": "Supreme Court Judgments"},
                {"name": "法律法规库", "url": "https://flk.npc.gov.cn", "desc": "Official Laws Database"},
                {"name": "执行信息网", "url": "http://zxgk.court.gov.cn", "desc": "Enforcement Information"},
                {"name": "庭审公开网", "url": "http://tingshen.court.gov.cn", "desc": "Court Trial Live"},
                {"name": "知识产权局 (CNIPA)", "url": "https://www.cnipa.gov.cn", "desc": "Patent & Trademark Office"},
                {"name": "市监总局 (SAMR)", "url": "https://www.samr.gov.cn", "desc": "Antitrust & Regulation"},
                {"name": "网信办 (CAC)", "url": "http://www.cac.gov.cn", "desc": "Cybersecurity"},
                {"name": "证监会 (CSRC)", "url": "http://www.csrc.gov.cn", "desc": "Securities Regulator"},
                {"name": "最高检 (SPP)", "url": "https://www.spp.gov.cn", "desc": "Supreme Procuratorate"},
                {"name": "司法部 (MoJ)", "url": "http://www.moj.gov.cn", "desc": "Ministry of Justice"},
                {"name": "中国律协", "url": "http://www.allchina-lawyers.org", "desc": "All China Lawyers Assn"},
                {"name": "贸仲委 (CIETAC)", "url": "http://www.cietac.org", "desc": "Intl Arbitration"},
                {"name": "北仲 (BAC)", "url": "https://www.bjac.org.cn", "desc": "Beijing Arbitration"},
                {"name": "深仲 (SCIA)", "url": "http://www.scia.com.cn", "desc": "Shenzhen Arbitration"},
                {"name": "上仲 (SHiac)", "url": "http://www.shiac.org", "desc": "Shanghai Arbitration"},
            ],
        },        
        "🇯🇵 Japan (日本)": {
            "🏛️ Big Four (四大律所)": [
                {"name": "Nishimura & Asahi", "url": "https://www.nishimura.com", "desc": "Largest in Japan"},
                {"name": "Nagashima Ohno (NO&T)", "url": "https://www.noandt.com", "desc": "Corporate Elite"},
                {"name": "Mori Hamada (MHM)", "url": "https://www.mhmjapan.com", "desc": "M&A and Finance"},
                {"name": "Anderson Mori (AMT)", "url": "https://www.amt-law.com", "desc": "International Focus"},
            ],
            "⛩️ Major Firms (主要律所)": [
                {"name": "TMI Associates", "url": "https://www.tmi.gr.jp", "desc": "IP & Corporate Mix"},
                {"name": "City-Yuwa", "url": "https://www.city-yuwa.com", "desc": "Finance Real Estate"},
                {"name": "Atsumi & Sakai", "url": "https://www.aplaw.jp", "desc": "Fintech Innovation"},
                {"name": "Oh-Ebashi", "url": "https://www.ohebashi.com", "desc": "Osaka Leader"},
                {"name": "Ushijima & Partners", "url": "https://www.ushijima-law.gr.jp", "desc": "Litigation"},
            ],
            "🌍 Gaiben (外资所)": [
                {"name": "Baker McKenzie Tokyo", "url": "https://www.bakermckenzie.co.jp", "desc": "Largest International"},
                {"name": "Morrison Foerster", "url": "https://www.mofo.com", "desc": "Tech & IP Leader"},
                {"name": "White & Case Tokyo", "url": "https://www.whitecase.com", "desc": "Projects"},
                {"name": "Skadden Tokyo", "url": "https://www.skadden.com", "desc": "M&A"},
            ],
            "💻 Tech & Official": [
                {"name": "Bengo4.com", "url": "https://www.bengo4.com", "desc": "Lawyer Portal"},
                {"name": "LegalOn Cloud", "url": "https://www.legalon-cloud.com", "desc": "AI Contract"},
                {"name": "CloudSign", "url": "https://www.cloudsign.jp", "desc": "E-Signature"},
                {"name": "MNTSQ", "url": "https://www.mntsq.co.jp", "desc": "Contract Database"},
                {"name": "J-PlatPat", "url": "https://www.j-platpat.inpit.go.jp", "desc": "IP Database"},
                {"name": "e-Gov Japan", "url": "https://www.e-gov.go.jp", "desc": "Laws"},
            ]
        },
        "🇸🇬 Singapore (新加坡)": {
            "🏛️ Big Four Firms": [
                {"name": "Allen & Gledhill", "url": "https://www.allenandgledhill.com", "desc": "Largest SG Firm"},
                {"name": "Rajah & Tann", "url": "https://www.rajahtannasia.com", "desc": "Full Service Asia"},
                {"name": "WongPartnership", "url": "https://www.wongpartnership.com", "desc": "Corporate Elite"},
                {"name": "Drew & Napier", "url": "https://www.drewnapier.com", "desc": "Litigation Powerhouse"},
                {"name": "Dentons Rodyk", "url": "https://www.dentonsrodyk.com", "desc": "Oldest SG Firm"},
                {"name": "Shook Lin & Bok", "url": "https://www.shooklin.com", "desc": "Banking & Finance"},
                {"name": "RPC Premier Law", "url": "https://www.rpc.com.sg", "desc": "Insurance & Dispute"},
                {"name": "TSMP Law", "url": "https://tsmplaw.com", "desc": "Boutique Corporate"},
                {"name": "Duane Morris & Selvam", "url": "https://www.duanemorris.com/singapore", "desc": "US Intl Presence"},
                {"name": "Withers KhattarWong", "url": "https://www.withersworldwide.com", "desc": "Private Client"},
                {"name": "Cavenagh Law", "url": "https://www.cliffordchance.com", "desc": "Clifford Chance JLV"},
                {"name": "Allen & Overy SG", "url": "https://www.allenovery.com", "desc": "Projects & Finance"},
                {"name": "Freshfields SG", "url": "https://www.freshfields.com", "desc": "M&A & Arbitration"},
                {"name": "Linklaters SG", "url": "https://www.linklaters.com", "desc": "Capital Markets"},
                {"name": "Gibson Dunn SG", "url": "https://www.gibsondunn.com", "desc": "Disputes"},
            ],
            "⚖️ Official & Tech": [
                {"name": "Singapore Law Watch", "url": "https://www.singaporelawwatch.sg", "desc": "Legal News & Updates"},
                {"name": "LawNet", "url": "https://www.lawnet.sg", "desc": "Legal Research Portal"},
                {"name": "Supreme Court SG", "url": "https://www.judiciary.gov.sg", "desc": "Judiciary"},
                {"name": "ACRA", "url": "https://www.acra.gov.sg", "desc": "Company Registry"},
                {"name": "IPOS", "url": "https://www.ipos.gov.sg", "desc": "Intellectual Property"},
                {"name": "SIAC", "url": "https://siac.org.sg", "desc": "Intl Arbitration Centre"},
                {"name": "LiteLab", "url": "https://litelab.com", "desc": "Legal Intelligence"},
                {"name": "Lupl", "url": "https://www.lupl.com", "desc": "Matter Management"},
                {"name": "MinLaw", "url": "https://www.mlaw.gov.sg", "desc": "Ministry of Law"},
                {"name": "SICC", "url": "https://www.sicc.gov.sg", "desc": "Intl Commercial Court"},
                {"name": "Law Society SG", "url": "https://www.lawsociety.org.sg", "desc": "Professional Body"},
            ],
            "💼 Consulting": [
                {"name": "Deloitte Legal SG", "url": "https://www2.deloitte.com/sg", "desc": "Consulting"},
                {"name": "PwC Legal SG", "url": "https://www.pwc.com/sg", "desc": "Advisory"},
            ]
        },
        "🇰🇷 South Korea (韩国)": {
            "🏛️ Big 6 Firms": [
                {"name": "Kim & Chang", "url": "https://www.kimchang.com", "desc": "Dominant Leader"},
                {"name": "Lee & Ko", "url": "http://www.leeko.com", "desc": "Premier Firm"},
                {"name": "Bae, Kim & Lee (BKL)", "url": "https://www.bkl.co.kr", "desc": "Litigation"},
                {"name": "Shin & Kim", "url": "https://www.shinkim.com", "desc": "Global Corp"},
                {"name": "Yulchon", "url": "https://www.yulchon.com", "desc": "Tax & Dispute"},
                {"name": "Yoon & Yang", "url": "https://www.yoonyang.com", "desc": "Antitrust"},
            ],
            "⚖️ Official": [
                {"name": "Supreme Court", "url": "https://eng.scourt.go.kr", "desc": "Judiciary"},
                {"name": "Statutes of Korea", "url": "https://elaw.klri.re.kr", "desc": "Laws"},
                {"name": "KIPO", "url": "https://www.kipo.go.kr", "desc": "IP Office"},
            ]
        },
        "🇮🇳 India (印度)": {
            "🏛️ Top Firms": [
                {"name": "Cyril Amarchand Mangaldas", "url": "https://www.cyrilshroff.com", "desc": "Largest Firm"},
                {"name": "Shardul Amarchand Mangaldas", "url": "https://www.amsshardul.com", "desc": "Premium Corp"},
                {"name": "Khaitan & Co", "url": "https://www.khaitanco.com", "desc": "Oldest & Leading"},
                {"name": "AZB & Partners", "url": "https://www.azbpartners.com", "desc": "M&A Specialist"},
                {"name": "Trilegal", "url": "https://www.trilegal.com", "desc": "Modern Full Service"},
                {"name": "IndusLaw", "url": "https://www.induslaw.com", "desc": "Tech & VC"},
                {"name": "Nishith Desai", "url": "https://www.nishithdesai.com", "desc": "Tax & Tech Boutique"},
            ],
            "⚖️ Gov": [
                {"name": "Supreme Court", "url": "https://main.sci.gov.in", "desc": "Highest Court"},
                {"name": "Manupatra", "url": "https://www.manupatra.com", "desc": "Legal Research"},
            ]
        },
      "🇭🇰 Hong Kong (香港)": {
             "🏛️ Leading Local Firms (本地大所)": [
                 {"name": "Deacons (的近)", "url": "https://www.deacons.com", "desc": "Largest Independent HK Firm"},
                 {"name": "Woo Kwan Lee & Lo (胡关李罗)", "url": "https://www.wkll.com", "desc": "Real Estate & Corporate"},
                 {"name": "Gall", "url": "https://www.gallhk.com", "desc": "Dispute Resolution Specialist"},
                 {"name": "Tanner De Witt", "url": "https://www.tannerdewitt.com", "desc": "Insolvency & Restructuring"},
                 {"name": "Wilkinson & Grist (高露云)", "url": "https://www.wilgrist.com", "desc": "IP & Conveyancing"},
                 {"name": "P.C. Woo & Co (胡百全)", "url": "https://www.pcwoo.com", "desc": "Established 1945"},
                 {"name": "Howse Williams", "url": "https://www.howsewilliams.com", "desc": "Independent Full Service"},
                 {"name": "Robertsons", "url": "https://www.robertsons-hk.com", "desc": "Commercial & Criminal"},
                 {"name": "Charltons", "url": "https://www.charltonslaw.com", "desc": "Boutique Corporate Finance"},
             ],
             "⚖️ Barristers Chambers (大律师办事处)": [
                 {"name": "Temple Chambers", "url": "https://templechambers.com", "desc": "Top Commercial Chambers"},
                 {"name": "Des Voeux Chambers (DVC)", "url": "https://dvc.hk", "desc": "Leading Commercial & IP"},
                 {"name": "Denis Chang's Chambers", "url": "https://dcc.law", "desc": "Public Law & Civil"},
                 {"name": "Plowman Chambers", "url": "https://www.plowman.com.hk", "desc": "Criminal Litigation"},
                 {"name": "Parkside Chambers", "url": "https://www.parksidechambers.com", "desc": "General Civil"},
             ],
             "🌏 International Giants in HK (国际所)": [
                 {"name": "Mayer Brown", "url": "https://www.mayerbrown.com", "desc": "Massive HK Presence"},
                 {"name": "Clifford Chance HK", "url": "https://www.cliffordchance.com", "desc": "Magic Circle"},
                 {"name": "Linklaters HK", "url": "https://www.linklaters.com", "desc": "Capital Markets"},
                 {"name": "Allen & Overy HK", "url": "https://www.allenovery.com", "desc": "Finance"},
                 {"name": "Kirkland & Ellis HK", "url": "https://www.kirkland.com", "desc": "PE & Restructuring"},
                 {"name": "Skadden HK", "url": "https://www.skadden.com", "desc": "IPO & M&A"},
                 {"name": "Davis Polk HK", "url": "https://www.davispolk.com", "desc": "US Law in HK"},
                 {"name": "King & Wood HK", "url": "https://www.kwm.com", "desc": "KWM Base"},
             ],
             "🏛️ Official & Regulators (官方/监管)": [
                 {"name": "HK Judiciary", "url": "https://www.judiciary.hk", "desc": "Courts System"},
                 {"name": "HKLII", "url": "https://www.hklii.org", "desc": "Free Legal Info"},
                 {"name": "SFC (证监会)", "url": "https://www.sfc.hk", "desc": "Securities Regulator"},
                 {"name": "HKEX (港交所)", "url": "https://www.hkex.com.hk", "desc": "Stock Exchange"},
                 {"name": "HKIAC (仲裁中心)", "url": "https://www.hkiac.org", "desc": "Arbitration Centre"},
                 {"name": "DoJ (律政司)", "url": "https://www.doj.gov.hk", "desc": "Dept of Justice"},
                 {"name": "Law Society of HK", "url": "https://www.hklawsoc.org.hk", "desc": "Solicitors Body"},
                 {"name": "HK Bar Assoc", "url": "https://www.hkba.org", "desc": "Barristers Body"},
                 {"name": "IPD (知识产权署)", "url": "https://www.ipd.gov.hk", "desc": "IP Office"},
                 {"name": "e-Bram", "url": "https://www.ebram.org", "desc": "Online Dispute Resolution"},
             ]
        },
        "🇹🇼 Taiwan (中国台湾)": {
            "🏛️ Top Firms (顶级律所)": [
                {"name": "Lee and Li (理律)", "url": "https://www.leeandli.com", "desc": "Largest & Full Service"},
                {"name": "Tsar & Tsai (常在)", "url": "https://www.tsartsai.com.tw", "desc": "Prestigious Corporate"},
                {"name": "Formosa Transnational (万国)", "url": "https://www.fts.com.tw", "desc": "Litigation Experts"},
                {"name": "LCS & Partners (协合)", "url": "https://www.lcs.com.tw", "desc": "M&A and Finance"},
                {"name": "Baker McKenzie Taipei", "url": "https://www.bakermckenzie.com", "desc": "Global Reach"},
                {"name": "Jones Day Taipei", "url": "https://www.jonesday.com", "desc": "Leading US Firm in TW"},
                {"name": "Chen & Lin (众达)", "url": "https://www.chenandlin.com", "desc": "IP & Tech"},
                {"name": "Brain Trust (博思)", "url": "https://www.braintrustlaw.com", "desc": "International Disputes"},
            ],
            "🔬 IP & Agencies (知产代理)": [
                {"name": "Saint Island (圣岛)", "url": "http://www.saint-island.com.tw", "desc": "Top IP Agency"},
                {"name": "Tai E (台一)", "url": "http://www.taie.com.tw", "desc": "Patent & Trademark"},
            ],
            "⚖️ Official & Gov (官方)": [
                {"name": "Judicial Yuan (司法院)", "url": "https://www.judicial.gov.tw", "desc": "Highest Judicial Organ"},
                {"name": "Laws & Regulations (法规)", "url": "https://law.moj.gov.tw", "desc": "MoJ Database"},
                {"name": "TIPO (智慧局)", "url": "https://www.tipo.gov.tw", "desc": "Intellectual Property Office"},
                {"name": "Ministry of Justice", "url": "https://www.moj.gov.tw", "desc": "Justice Dept"},
                {"name": "Fair Trade Comm", "url": "https://www.ftc.gov.tw", "desc": "Antitrust Regulator"},
            ]
        },
        "🇦🇺 Australia (澳大利亚)": {
            "🏛️ Top Tier Firms": [
                {"name": "King & Wood Mallesons AU", "url": "https://www.kwm.com/au", "desc": "Top Tier Intl"},
                {"name": "MinterEllison", "url": "https://www.minterellison.com", "desc": "Largest AU Firm"},
                {"name": "Allens", "url": "https://www.allens.com.au", "desc": "Linklaters Alliance"},
                {"name": "Clayton Utz", "url": "https://www.claytonutz.com", "desc": "Independent Leader"},
                {"name": "Herbert Smith Freehills AU", "url": "https://www.herbertsmithfreehills.com", "desc": "Litigation Focus"},
                {"name": "Gilbert + Tobin", "url": "https://www.gtlaw.com.au", "desc": "Corporate/TMT"},
                {"name": "Ashurst AU", "url": "https://www.ashurst.com", "desc": "Projects & Finance"},
                {"name": "Corrs Chambers Westgarth", "url": "https://www.corrs.com.au", "desc": "Major Commercial"},
                {"name": "Johnson Winter & Slattery", "url": "https://www.jws.com.au", "desc": "M&A Specialist"},
                {"name": "Norton Rose Fulbright AU", "url": "https://www.nortonrosefulbright.com", "desc": "Global"},
            ],
            "⚖️ Research & Official": [
                {"name": "AustLII", "url": "http://www.austlii.edu.au", "desc": "Free Legal Info"},
                {"name": "Federal Court", "url": "https://www.fedcourt.gov.au", "desc": "Judiciary"},
                {"name": "ASIC", "url": "https://asic.gov.au", "desc": "Corporate Regulator"},
                {"name": "IP Australia", "url": "https://www.ipaustralia.gov.au", "desc": "Patents & TM"},
                {"name": "Law Council of Australia", "url": "https://www.lawcouncil.asn.au", "desc": "Peak Body"},
            ]
        },
        "🇻🇳 Vietnam (越南)": {
             "🏛️ Firms": [
                 {"name": "VILAF", "url": "https://www.vilaf.com.vn", "desc": "Leading Local"},
                 {"name": "YKVN", "url": "https://ykvn-law.com", "desc": "Litigation"},
                 {"name": "Tilleke & Gibbins", "url": "https://www.tilleke.com", "desc": "IP Expert"},
             ]
        },
        "🇮🇩 Indonesia (印尼)": {
             "🏛️ Firms": [
                 {"name": "Hadiputranto (HHP)", "url": "https://www.hhp.co.id", "desc": "Baker McKenzie"},
                 {"name": "Assegaf Hamzah", "url": "https://www.ahp.co.id", "desc": "Top Tier"},
                 {"name": "SSEK", "url": "https://www.ssek.com", "desc": "Consultants"},
             ]
        },
        "🇹🇭 Thailand (泰国)": {
             "🏛️ Firms": [
                 {"name": "Weerawong C&P", "url": "https://www.weerawongcp.com", "desc": "Top Thai"},
                 {"name": "Chandler MHM", "url": "https://www.chandlermhm.com", "desc": "Energy"},
             ]
        },
        "🇲🇾 Malaysia (马来西亚)": {
             "🏛️ Firms": [
                 {"name": "Shearn Delamore", "url": "https://www.shearndelamore.com", "desc": "Top Tier"},
                 {"name": "Skrine", "url": "https://www.skrine.com", "desc": "Large Firm"},
                 {"name": "Rahmat Lim", "url": "https://www.rahmatlim.com", "desc": "A&G Affiliate"},
             ]
        },
    },

    # ================= 北美 (North America) =================

    "🌎 North America (北美)": {
        "🇺🇸 USA (美国)": {
            "🏛️ Am Law 20 Elite (顶级律所)": [
                {"name": "Kirkland & Ellis", "url": "https://www.kirkland.com", "desc": "#1 Revenue Global"},
                {"name": "Latham & Watkins", "url": "https://www.lw.com", "desc": "Global Elite"},
                {"name": "Skadden Arps", "url": "https://www.skadden.com", "desc": "M&A Powerhouse"},
                {"name": "Sidley Austin", "url": "https://www.sidley.com", "desc": "Regulatory & Corp"},
                {"name": "Morgan Lewis", "url": "https://www.morganlewis.com", "desc": "Labor & Employment"},
                {"name": "White & Case", "url": "https://www.whitecase.com", "desc": "Intl Arbitration"},
                {"name": "Hogan Lovells", "url": "https://www.hoganlovells.com", "desc": "Gov & Regulatory"},
                {"name": "DLA Piper", "url": "https://www.dlapiper.com", "desc": "Global Volume"},
                {"name": "Jones Day", "url": "https://www.jonesday.com", "desc": "Litigation"},
                {"name": "Ropes & Gray", "url": "https://www.ropesgray.com", "desc": "Private Equity"},
                {"name": "Gibson Dunn", "url": "https://www.gibsondunn.com", "desc": "High-stakes Lit"},
                {"name": "Simpson Thacher", "url": "https://www.stblaw.com", "desc": "Banking & PE"},
                {"name": "Davis Polk", "url": "https://www.davispolk.com", "desc": "Capital Markets"},
                {"name": "Sullivan & Cromwell", "url": "https://www.sullcrom.com", "desc": "Finance Prestige"},
                {"name": "Paul Weiss", "url": "https://www.paulweiss.com", "desc": "Litigation Elite"},
                {"name": "Cravath", "url": "https://www.cravath.com", "desc": "White Shoe"},
                {"name": "Wachtell Lipton", "url": "https://www.wlrk.com", "desc": "M&A Boutique"},
                {"name": "Cleary Gottlieb", "url": "https://www.clearygottlieb.com", "desc": "Intl Finance"},
                {"name": "Weil Gotshal", "url": "https://www.weil.com", "desc": "Restructuring"},
                {"name": "Goodwin", "url": "https://www.goodwinlaw.com", "desc": "Life Sciences"},
            ],
            "⚔️ Litigation & Employment (诉讼/劳动)": [
                {"name": "Quinn Emanuel", "url": "https://www.quinnemanuel.com", "desc": "Litigation Only"},
                {"name": "Boies Schiller", "url": "https://www.bsfllp.com", "desc": "High Profile Lit"},
                {"name": "Littler Mendelson", "url": "https://www.littler.com", "desc": "Employment Global"},
                {"name": "Jackson Lewis", "url": "https://www.jacksonlewis.com", "desc": "Workplace Law"},
                {"name": "Ogletree Deakins", "url": "https://ogletree.com", "desc": "Labor Law"},
                {"name": "Fragomen", "url": "https://www.fragomen.com", "desc": "Immigration"},
            ],
             "🦄 Tech & Boutique Firms (科技/精品所)": [
                {"name": "Cooley", "url": "https://www.cooley.com", "desc": "Tech & Life Sciences"},
                {"name": "Wilson Sonsini", "url": "https://www.wsgr.com", "desc": "Silicon Valley Pioneer"},
                {"name": "Fenwick & West", "url": "https://www.fenwick.com", "desc": "Tech Transactions"},
                {"name": "Quinn Emanuel", "url": "https://www.quinnemanuel.com", "desc": "Business Litigation Only"},
                {"name": "Fragomen", "url": "https://www.fragomen.com", "desc": "Immigration Law"},
                {"name": "Littler Mendelson", "url": "https://www.littler.com", "desc": "Employment Law"},
                {"name": "WilmerHale", "url": "https://www.wilmerhale.com", "desc": "IP & Appellate"},
                {"name": "Covington & Burling", "url": "https://www.cov.com", "desc": "Regulatory"},
                {"name": "Goodwin", "url": "https://www.goodwinlaw.com", "desc": "Life Sciences & RE"},
                {"name": "Orrick", "url": "https://www.orrick.com", "desc": "Innovation Focus"},
                {"name": "Shearman & Sterling", "url": "https://www.shearman.com", "desc": "M&A & Finance"},
                {"name": "King & Spalding", "url": "https://www.kslaw.com", "desc": "Energy & Litigation"},
            ],
            "💻 LegalTech & Research (法律科技)": [
                {"name": "Westlaw", "url": "https://legal.thomsonreuters.com", "desc": "Premier Research"},
                {"name": "LexisNexis", "url": "https://www.lexisnexis.com", "desc": "Legal Research"},
                {"name": "Clio", "url": "https://www.clio.com", "desc": "Practice Management"},
                {"name": "Ironclad", "url": "https://ironcladapp.com", "desc": "CLM Platform"},
                {"name": "Relativity", "url": "https://www.relativity.com", "desc": "E-Discovery"},
                {"name": "Everlaw", "url": "https://www.everlaw.com", "desc": "Cloud Litigation"},
                {"name": "DocuSign", "url": "https://www.docusign.com", "desc": "E-Signatures"},
                {"name": "Harvey", "url": "https://www.harvey.ai", "desc": "GenAI for Law"},
                {"name": "LegalZoom", "url": "https://www.legalzoom.com", "desc": "Consumer Legal"},
                {"name": "Casetext", "url": "https://casetext.com", "desc": "AI Research"},
                {"name": "Fastcase", "url": "https://www.fastcase.com", "desc": "Affordable Research"},
                {"name": "Intapp", "url": "https://www.intapp.com", "desc": "Firm Management Software"},
                {"name": "DISCO", "url": "https://www.csdisco.com", "desc": "E-Discovery SaaS"},
                {"name": "Evisort", "url": "https://www.evisort.com", "desc": "AI Contract Mgmt"},
            ], 
            "⚖️ Official (官方)": [
                {"name": "Supreme Court", "url": "https://www.supremecourt.gov", "desc": "SCOTUS"},
                {"name": "USPTO", "url": "https://www.uspto.gov", "desc": "Patents"},
                {"name": "SEC Edgar", "url": "https://www.sec.gov", "desc": "Filings"},
                {"name": "Regulations.gov", "url": "https://www.regulations.gov", "desc": "Rulemaking"},
            ]
        },
        "🇨🇦 Canada (加拿大)": {
            "🏛️ Seven Sisters (七大律所)": [
                {"name": "McCarthy Tétrault", "url": "https://www.mccarthy.ca", "desc": "Innovation Leader"},
                {"name": "Blake, Cassels", "url": "https://www.blakes.com", "desc": "Business Law"},
                {"name": "Osler", "url": "https://www.osler.com", "desc": "Tech & Tax Focus"},
                {"name": "Torys", "url": "https://www.torys.com", "desc": "Cross-border M&A"},
                {"name": "Stikeman Elliott", "url": "https://www.stikeman.com", "desc": "Corporate Finance"},
                {"name": "Davies Ward", "url": "https://www.dwpv.com", "desc": "High-stakes Deal"},
                {"name": "Goodmans", "url": "https://www.goodmans.ca", "desc": "REITs & Restructuring"},
            ],
            "⚖️ Major Firms": [
                {"name": "Gowling WLG", "url": "https://gowlingwlg.com", "desc": "IP & International"},
                {"name": "Norton Rose Fulbright CA", "url": "https://www.nortonrosefulbright.com", "desc": "Global"},
                {"name": "Fasken", "url": "https://www.fasken.com", "desc": "Mining & Litigation"},
                {"name": "Borden Ladner Gervais (BLG)", "url": "https://www.blg.com", "desc": "Largest Full Service"},
                {"name": "Dentons Canada", "url": "https://www.dentons.com", "desc": "Polycentric"},
                {"name": "Bennett Jones", "url": "https://www.bennettjones.com", "desc": "Energy Focus"},
            ],
            "💻 Tech & Gov": [
                {"name": "CanLII", "url": "https://www.canlii.org", "desc": "Free Legal Database"},
                {"name": "SCC", "url": "https://www.scc-csc.ca", "desc": "Supreme Court"},
                {"name": "Kira Systems", "url": "https://kirasystems.com", "desc": "AI Contract Review"},
                {"name": "Clio (HQ)", "url": "https://www.clio.com", "desc": "Practice Management"},
            ]
        },
        "🇲🇽 Mexico (墨西哥)": {
            "🏛️ Top Firms": [
                {"name": "Creel (Creel-García)", "url": "https://www.creel.mx", "desc": "Top Tier"},
                {"name": "Galicia Abogados", "url": "https://www.galicia.com.mx", "desc": "Finance Focus"},
                {"name": "Nader, Hayaux & Goebel", "url": "https://nhg.mx", "desc": "Banking & Insurance"},
                {"name": "Mijares, Angoitia", "url": "https://www.mamg.com.mx", "desc": "Corporate"},
                {"name": "Basham", "url": "https://basham.com.mx", "desc": "IP Leader"},
            ],
            "⚖️ Gov": [{"name": "SCJN", "url": "https://www.scjn.gob.mx", "desc": "Supreme Court"}]
        },
        "🇧🇲 Bermuda (百慕大)": {
            "🏛️ Offshore Leaders": [
                {"name": "Conyers", "url": "https://www.conyers.com", "desc": "Leading Firm"},
                {"name": "Appleby", "url": "https://www.applebyglobal.com", "desc": "Global Offshore"},
                {"name": "Walkers", "url": "https://www.walkersglobal.com", "desc": "Finance Focus"},
            ],
             "⚖️ Official": [{"name": "Bermuda Laws", "url": "http://www.bermudalaws.bm", "desc": "Legislation"}]
        },
        "🇵🇦 Panama (巴拿马)": {
             "🏛️ Firms": [
                 {"name": "Morgan & Morgan", "url": "https://www.morimor.com", "desc": "Largest in Panama"},
                 {"name": "Arias, Fábrega (ARIFA)", "url": "https://www.arifajo.com", "desc": "Top Tier"},
             ]
        },
         "🇨🇷 Costa Rica (哥斯达黎加)": {
             "🏛️ Firms": [
                 {"name": "BLP", "url": "https://www.blplegal.com", "desc": "Business Law"},
                 {"name": "Consortium Legal", "url": "https://consortiumlegal.com", "desc": "Regional"},
             ]
        }
    },

# ================= 🌍 欧洲 (Europe / EMEA) =================
    "🌍 Europe (欧洲)": {
        "🇬🇧 UK (英国)": {
            "🏰 Magic & Silver Circle (顶尖律所)": [
                {"name": "Allen & Overy", "url": "https://www.allenovery.com", "desc": "Global Elite"},
                {"name": "Clifford Chance", "url": "https://www.cliffordchance.com", "desc": "Global Finance"},
                {"name": "Freshfields", "url": "https://www.freshfields.com", "desc": "Corporate & M&A"},
                {"name": "Linklaters", "url": "https://www.linklaters.com", "desc": "Corporate Elite"},
                {"name": "Slaughter and May", "url": "https://www.slaughterandmay.com", "desc": "Prestigious Blue-blood"},
                {"name": "Herbert Smith Freehills", "url": "https://www.herbertsmithfreehills.com", "desc": "Litigation Powerhouse"},
                {"name": "Ashurst", "url": "https://www.ashurst.com", "desc": "Projects & Finance"},
                {"name": "Macfarlanes", "url": "https://www.macfarlanes.com", "desc": "Private Client & Corp"},
                {"name": "Travers Smith", "url": "https://www.traverssmith.com", "desc": "Corporate Boutique"},
            ],
            "🎓 Barristers Chambers (大律师公会)": [
                {"name": "Essex Court", "url": "https://essexcourt.com", "desc": "Commercial Arbitration"},
                {"name": "Blackstone", "url": "https://www.blackstonechambers.com", "desc": "Public Law & Comm"},
                {"name": "Brick Court", "url": "https://www.brickcourt.co.uk", "desc": "Competition & EU"},
                {"name": "Fountain Court", "url": "https://www.fountaincourt.co.uk", "desc": "Banking & Fraud"},
                {"name": "One Essex Court", "url": "https://www.oeclaw.co.uk", "desc": "Commercial Lit"},
                {"name": "Monckton", "url": "https://www.monckton.com", "desc": "Competition Law"},
            ],
            "💡 Tech & Official (科技/官方)": [
                {"name": "legislation.gov.uk", "url": "https://www.legislation.gov.uk", "desc": "Official Laws"},
                {"name": "Supreme Court UK", "url": "https://www.supremecourt.uk", "desc": "Highest Court"},
                {"name": "BAILII", "url": "https://www.bailii.org", "desc": "Case Law Database"},
                {"name": "Luminance", "url": "https://www.luminance.com", "desc": "AI Document Review"},
                {"name": "Juro", "url": "https://juro.com", "desc": "Contract Platform"},
                {"name": "Companies House", "url": "https://www.gov.uk/government/organisations/companies-house", "desc": "Company Registry"},
                {"name": "SRA", "url": "https://www.sra.org.uk", "desc": "Solicitors Regulation"},
            ]
        },
        "🇩🇪 Germany (德国)": {
            "🏛️ Top Kanzleien (顶尖律所)": [
                {"name": "Hengeler Mueller", "url": "https://www.hengeler.com", "desc": "Market Leader"},
                {"name": "Gleiss Lutz", "url": "https://www.gleisslutz.com", "desc": "Full Service Elite"},
                {"name": "Noerr", "url": "https://www.noerr.com", "desc": "Leading Independent"},
                {"name": "Luther", "url": "https://www.luther-lawfirm.com", "desc": "Mid-market specialist"},
                {"name": "Heuking", "url": "https://www.heuking.de", "desc": "Large partnership"},
                {"name": "CMS Germany", "url": "https://cms.law/en/deu", "desc": "Largest Tech Practice"},
                {"name": "Flick Gocke Schaumburg", "url": "https://www.fgs.de", "desc": "Tax Heavyweight"},
                {"name": "Görg", "url": "https://www.goerg.de", "desc": "Insolvency"},
                {"name": "Beiten Burkhardt", "url": "https://www.advant-beiten.com", "desc": "Advant Network"},
            ],
            "⚖️ Official & Tech": [
                {"name": "Juris", "url": "https://www.juris.de", "desc": "Legal Database"},
                {"name": "Beck-Online", "url": "https://beck-online.beck.de", "desc": "Legal Research"},
                {"name": "Gesetze-im-internet", "url": "https://www.gesetze-im-internet.de", "desc": "Federal Laws"},
                {"name": "BVerfG", "url": "https://www.bundesverfassungsgericht.de", "desc": "Constitutional Court"},
                {"name": "DPMA", "url": "https://www.dpma.de", "desc": "Patent Office"},
                {"name": "BRYTER", "url": "https://bryter.com", "desc": "No-code Automation"},
            ]
        },
        "🇫🇷 France (法国)": {
            "🏛️ Top Cabinets (顶尖律所)": [
                {"name": "Bredin Prat", "url": "https://www.bredinprat.com", "desc": "Corporate & Litigation"},
                {"name": "Darrois Villey", "url": "https://www.darroisvilley.com", "desc": "M&A Prestige"},
                {"name": "Gide Loyrette Nouel", "url": "https://www.gide.com", "desc": "International French Firm"},
                {"name": "Fidal", "url": "https://www.fidal.com", "desc": "Largest Business Firm"},
                {"name": "August Debouzy", "url": "https://www.august-debouzy.com", "desc": "Modern Full Service"},
                {"name": "DS Avocats", "url": "https://www.dsavocats.com", "desc": "International Network"},
                {"name": "De Pardieu Brocas", "url": "https://www.de-pardieu.com", "desc": "Finance & Real Estate"},
                {"name": "Jeantet", "url": "https://www.jeantet.fr", "desc": "Historical Business Firm"},
            ],
            "⚖️ Official & Tech": [
                {"name": "Légifrance", "url": "https://www.legifrance.gouv.fr", "desc": "Official Laws"},
                {"name": "Cour de cassation", "url": "https://www.courdecassation.fr", "desc": "Supreme Court"},
                {"name": "Doctrine", "url": "https://www.doctrine.fr", "desc": "Legal Intelligence"},
                {"name": "Jus Mundi", "url": "https://jusmundi.com", "desc": "Intl Arbitration Search"},
                {"name": "CNIL", "url": "https://www.cnil.fr", "desc": "Data Protection"},
            ]
        },
        "🇨🇭 Switzerland (瑞士)": {
            "🏛️ Top Firms (顶尖律所)": [
                {"name": "Lenz & Staehelin", "url": "https://www.lenzstaehelin.com", "desc": "Largest Swiss Firm"},
                {"name": "Bär & Karrer", "url": "https://www.baerkarrer.ch", "desc": "M&A & Capital Markets"},
                {"name": "Schellenberg Wittmer", "url": "https://www.swlegal.ch", "desc": "Arbitration & Corp"},
                {"name": "Walder Wyss", "url": "https://www.walderwyss.com", "desc": "Rapidly Growing"},
                {"name": "Niederer Kraft Frey", "url": "https://www.nkf.ch", "desc": "Finance & Corporate"},
                {"name": "Homburger", "url": "https://homburger.ch", "desc": "Commercial Law"},
            ],
            "⚖️ Official": [
                {"name": "Swisslex", "url": "https://www.swisslex.ch", "desc": "Legal Database"},
                {"name": "Federal Supreme Court", "url": "https://www.bger.ch", "desc": "Judiciary"},
                {"name": "Zefix", "url": "https://www.zefix.ch", "desc": "Commercial Register"},
                {"name": "Fedlex", "url": "https://www.fedlex.admin.ch", "desc": "Federal Law"},
            ]
        },
        "🇳🇱 Netherlands (荷兰)": {
            "🏛️ De Brauw & Others (顶级律所)": [
                {"name": "De Brauw", "url": "https://www.debrauw.com", "desc": "Global Litigation"},
                {"name": "NautaDutilh", "url": "https://www.nautadutilh.com", "desc": "Benelux Leader"},
                {"name": "Houthoff", "url": "https://www.houthoff.com", "desc": "Top Tier"},
                {"name": "Loyens & Loeff", "url": "https://www.loyensloeff.com", "desc": "Tax & Civil Law"},
                {"name": "Stibbe", "url": "https://www.stibbe.com", "desc": "Internationally Oriented"},
                {"name": "Van Doorne", "url": "https://www.vandoorne.com", "desc": "Independent"},
            ],
            "⚖️ Official": [
                {"name": "Rechtspraak", "url": "https://www.rechtspraak.nl", "desc": "Judiciary Portal"},
                {"name": "Overheid.nl", "url": "https://www.overheid.nl", "desc": "Laws Database"},
            ]
        },
        "🇮🇹 Italy (意大利)": {
            "🏛️ Top Firms (顶尖律所)": [
                {"name": "BonelliErede", "url": "https://belex.com", "desc": "Market Leader"},
                {"name": "Chiomenti", "url": "https://www.chiomenti.net", "desc": "Institutional Elite"},
                {"name": "Legance", "url": "https://www.legance.com", "desc": "Modern Independent"},
                {"name": "Gianni & Origoni", "url": "https://www.gop.it", "desc": "International Corporate"},
                {"name": "NCTM", "url": "https://www.nctm.it", "desc": "Tech & Innovation"},
                {"name": "Pedersoli", "url": "https://www.pedersoli.it", "desc": "M&A Boutique"},
            ],
            "⚖️ Official": [
                {"name": "Normattiva", "url": "https://www.normattiva.it", "desc": "Laws Database"},
                {"name": "Corte Costituzionale", "url": "https://www.cortecostituzionale.it", "desc": "Constitutional Court"},
                {"name": "Giustizia", "url": "https://www.giustizia.it", "desc": "Ministry of Justice"},
            ]
        },
        "🇪🇸 Spain (西班牙)": {
            "🏛️ Top Firms (顶尖律所)": [
                {"name": "Garrigues", "url": "https://www.garrigues.com", "desc": "Largest in Continental Europe"},
                {"name": "Cuatrecasas", "url": "https://www.cuatrecasas.com", "desc": "Iberian Leader"},
                {"name": "Uría Menéndez", "url": "https://www.uria.com", "desc": "Prestigious Elite"},
                {"name": "Pérez-Llorca", "url": "https://www.perezllorca.com", "desc": "High-end Corporate"},
                {"name": "Gómez-Acebo & Pombo", "url": "https://www.ga-p.com", "desc": "Full Service"},
            ],
            "⚖️ Official": [
                {"name": "BOE", "url": "https://www.boe.es", "desc": "Official Gazette"},
                {"name": "Poder Judicial", "url": "https://www.poderjudicial.es", "desc": "Judiciary"},
            ]
        },
        "🇸🇪 Sweden (瑞典)": {
             "🏛️ Firms": [
                 {"name": "Vinge", "url": "https://www.vinge.se", "desc": "M&A Leader"},
                 {"name": "Mannheimer Swartling", "url": "https://www.mannheimerswartling.se", "desc": "Top Nordic Firm"},
                 {"name": "Setterwalls", "url": "https://setterwalls.se", "desc": "Oldest Firm"},
             ],
             "⚖️ Official": [{"name": "Lagrummet", "url": "https://www.lagrummet.se", "desc": "Legal Portal"}]
        },
        "🇮🇪 Ireland (爱尔兰)": {
             "🏛️ Firms": [
                 {"name": "Arthur Cox", "url": "https://www.arthurcox.com", "desc": "Top Tier"},
                 {"name": "Matheson", "url": "https://www.matheson.com", "desc": "Intl Focus"},
                 {"name": "A&L Goodbody", "url": "https://www.algoodbody.com", "desc": "Corporate Leader"},
                 {"name": "McCann FitzGerald", "url": "https://www.mccannfitzgerald.com", "desc": "Banking & Finance"},
             ],
             "⚖️ Official": [{"name": "Courts.ie", "url": "https://www.courts.ie", "desc": "Courts Service"}]
        },
        "🇧🇪 Belgium (比利时)": {
             "🏛️ Firms": [
                 {"name": "Eubelius", "url": "https://www.eubelius.com", "desc": "Leading Independent"},
                 {"name": "Liedekerke", "url": "https://liedekerke.com", "desc": "Business Law"},
                 {"name": "Stibbe Brussels", "url": "https://www.stibbe.com", "desc": "Benelux Giant"},
             ],
             "⚖️ Official": [{"name": "Moniteur Belge", "url": "https://www.ejustice.just.fgov.be", "desc": "Official Journal"}]
        },
        "🇱🇺 Luxembourg (卢森堡)": {
             "🏛️ Firms": [
                 {"name": "Arendt & Medernach", "url": "https://www.arendt.com", "desc": "Largest Firm"},
                 {"name": "Elvinger Hoss", "url": "https://www.elvingerhoss.pr", "desc": "Fund Formation"},
                 {"name": "Bonn Steichen", "url": "https://www.bsp.lu", "desc": "Full Service"},
             ],
             "⚖️ Official": [{"name": "Legilux", "url": "https://legilux.public.lu", "desc": "Legal Portal"}]
        },
        "🇷🇺 Russia (俄罗斯)": {
            "🏛️ Market Giants (本土巨头)": [
                {"name": "EPAM", "url": "https://epam.ru", "desc": "Largest Law Firm in CIS"},
                {"name": "ALRUD", "url": "https://www.alrud.com", "desc": "Top Tier Corporate"},
                {"name": "Pepeliaev Group", "url": "https://www.pepeliaevgroup.ru", "desc": "Tax Litigation Leader"},
                {"name": "Monastyrsky (MZS)", "url": "https://www.mzs.ru", "desc": "Dispute Resolution"},
                {"name": "Lidings", "url": "https://www.lidings.com", "desc": "Advising Foreign Business"},
            ],
            "🔄 New Wave / Spin-offs (原外资所重组)": [
                {"name": "Rybalkin (RGD)", "url": "https://rgd.legal", "desc": "Ex-Freshfields/Cleary Team"},
                {"name": "Better Chance", "url": "https://betterchance.ru", "desc": "Ex-Clifford Chance Team"},
                {"name": "Stonebridge", "url": "https://stonebridgelegal.ru", "desc": "Ex-Freshfields Team"},
                {"name": "Nikolskaya Consulting", "url": "https://nikolskaya.ru", "desc": "Ex-Herbert Smith Freehills"},
                {"name": "Level Legal", "url": "https://level.legal", "desc": "Ex-Hogan Lovells Team"},
                {"name": "Nextons", "url": "https://nextons.ru", "desc": "Ex-Dentons Russia"},
                {"name": "Kept Legal", "url": "https://kept.ru", "desc": "Ex-KPMG Law"},
                {"name": "TeDo", "url": "https://tedo.ru", "desc": "Ex-PwC Legal"},
            ],
            "💻 LegalTech & Official (科技/官方)": [
                {"name": "Pravo.gov.ru", "url": "http://pravo.gov.ru", "desc": "Official Legal Information"},
                {"name": "Kad.Arbitr", "url": "https://kad.arbitr.ru", "desc": "Commercial Case Database"},
                {"name": "Consultant Plus", "url": "http://www.consultant.ru", "desc": "Leading Legal Research"},
                {"name": "Garant", "url": "https://www.garant.ru", "desc": "Legal Reference System"},
                {"name": "Casebook", "url": "https://casebook.ru", "desc": "Litigation Analytics"},
                {"name": "Doczilla", "url": "https://doczilla.pro", "desc": "AI Contract Drafting"},
            ]
        },
        "🇹🇷 Turkey (土耳其)": {
            "🏛️ Top Tier Firms (顶级律所)": [
                {"name": "Paksoy", "url": "https://www.paksoy.av.tr", "desc": "Leading Independent Firm"},
                {"name": "Herguner Bilgen Ozeke", "url": "https://www.herguner.av.tr", "desc": "Corporate Powerhouse"},
                {"name": "Pekin & Pekin", "url": "https://www.pekin.com.tr", "desc": "Oldest Firm in Turkey"},
                {"name": "Esin Attorney", "url": "https://www.esin.av.tr", "desc": "Baker McKenzie Member"},
                {"name": "BASEAK", "url": "https://www.baseak.com", "desc": "Dentons Affiliate"},
                {"name": "Balcioglu Selcuk (BSEL)", "url": "https://www.bsel.com.tr", "desc": "Capital Markets"},
                {"name": "Turunc", "url": "https://turunc.com", "desc": "M&A and Finance"},
                {"name": "Kolcuoglu (KDK)", "url": "https://www.kolcuoglu.av.tr", "desc": "Energy & Infrastructure"},
                {"name": "Moroglu Arseven", "url": "https://www.morogluarseven.com", "desc": "IP & Dispute"},
                {"name": "Gun + Partners", "url": "https://gun.av.tr", "desc": "IP & Commercial"},
            ],
            "⚖️ Official & LegalTech (官方/科技)": [
                {"name": "Resmi Gazete", "url": "https://www.resmigazete.gov.tr", "desc": "Official Gazette"},
                {"name": "UYAP", "url": "https://www.uyap.gov.tr", "desc": "National Judiciary Network"},
                {"name": "Mevzuat", "url": "https://www.mevzuat.gov.tr", "desc": "Legislation Database"},
                {"name": "Lexpera", "url": "https://www.lexpera.com.tr", "desc": "Legal Info System"},
                {"name": "Corpus", "url": "https://www.corpus.com.tr", "desc": "Case Law Search"},
                {"name": "Constitutional Court", "url": "https://www.anayasa.gov.tr", "desc": "Highest Court"},
            ]
        }
    },
    # ================= 💃 拉丁美洲 (Latin America) =================
    "💃 Latin America (拉美)": {
        "🇧🇷 Brazil (巴西)": {
            "🏛️ Big Law (顶级律所)": [
                {"name": "Mattos Filho", "url": "https://www.mattosfilho.com.br", "desc": "Premium Full Service"},
                {"name": "Pinheiro Neto", "url": "https://www.pinheironeto.com.br", "desc": "Traditional Elite"},
                {"name": "Machado Meyer", "url": "https://www.machadomeyer.com.br", "desc": "Banking & Finance"},
                {"name": "Demarest Advogados", "url": "https://www.demarest.com.br", "desc": "Major Corporate Firm"},
                {"name": "Veirano Advogados", "url": "https://www.veirano.com.br", "desc": "International Focus"},
                {"name": "BMA Advogados", "url": "https://www.bmalaw.com.br", "desc": "M&A & Crypto"},
                {"name": "TozziniFreire", "url": "https://tozzinifreire.com.br", "desc": "Established Leader"},
                {"name": "Lefosse", "url": "https://www.lefosse.com", "desc": "Capital Markets"},
            ],
            "💻 Tech & Official (科技/官方)": [
                {"name": "Jusbrasil", "url": "https://www.jusbrasil.com.br", "desc": "Largest Legal Tech"},
                {"name": "STF (Supreme Court)", "url": "https://portal.stf.jus.br", "desc": "Constitutional Court"},
                {"name": "STJ (High Court)", "url": "https://www.stj.jus.br", "desc": "Superior Court of Justice"},
                {"name": "Planalto Legislacao", "url": "http://www4.planalto.gov.br/legislacao", "desc": "Federal Laws"},
                {"name": "CADE", "url": "https://www.gov.br/cade", "desc": "Antitrust Authority"},
            ]
        },
        "🇲🇽 Mexico (墨西哥)": {
            "🏛️ Top Firms": [
                {"name": "Creel (Creel-García)", "url": "https://www.creel.mx", "desc": "Market Leader"},
                {"name": "Galicia Abogados", "url": "https://www.galicia.com.mx", "desc": "Finance & Energy"},
                {"name": "Mijares, Angoitia", "url": "https://www.mamg.com.mx", "desc": "Corporate Elite"},
                {"name": "Nader, Hayaux & Goebel", "url": "https://nhg.mx", "desc": "Banking & Insurance"},
                {"name": "Von Wobeser", "url": "https://www.vonwobeser.com", "desc": "Dispute Resolution"},
                {"name": "Basham, Ringe", "url": "https://basham.com.mx", "desc": "IP Leader"},
                {"name": "Ritch Mueller", "url": "https://www.ritch.com.mx", "desc": "Projects & Energy"},
            ],
            "⚖️ Official": [
                {"name": "SCJN", "url": "https://www.scjn.gob.mx", "desc": "Supreme Court"},
                {"name": "Diario Oficial", "url": "https://www.dof.gob.mx", "desc": "Official Gazette"},
            ]
        },
        "🇨🇱 Chile (智利)": {
            "🏛️ Top Firms": [
                {"name": "Carey", "url": "https://www.carey.cl", "desc": "Largest in Chile"},
                {"name": "Philippi (PPU)", "url": "https://ppulegal.com", "desc": "Regional Powerhouse"},
                {"name": "Barros & Errázuriz", "url": "https://www.bye.cl", "desc": "Corporate & Tax"},
                {"name": "Claro & Cía", "url": "https://www.claro.cl", "desc": "Prestigious Elite"},
                {"name": "Guerrero Olivos", "url": "https://www.guerrero.cl", "desc": "Mining & Finance"},
            ],
            "⚖️ Official": [
                {"name": "Poder Judicial", "url": "https://www.pjud.cl", "desc": "Judiciary"},
                {"name": "Ley Chile", "url": "https://www.bcn.cl/leychile", "desc": "Library of Congress Laws"},
            ]
        },
        "🇦🇷 Argentina (阿根廷)": {
            "🏛️ Top Firms": [
                {"name": "Marval O'Farrell", "url": "https://www.marval.com", "desc": "Largest in Argentina"},
                {"name": "Beccar Varela", "url": "https://beccarvarela.com", "desc": "Corporate Leader"},
                {"name": "Bruchou & Funes", "url": "https://bruchoufunes.com", "desc": "Banking & Finance"},
                {"name": "Pérez Alati (PAGBAM)", "url": "https://www.pagbam.com", "desc": "Full Service"},
            ],
            "⚖️ Official": [
                {"name": "InfoLeg", "url": "http://www.infoleg.gob.ar", "desc": "Legal Information"},
                {"name": "CSJN", "url": "https://www.csjn.gov.ar", "desc": "Supreme Court"},
            ]
        },
        "🇨🇴 Colombia (哥伦比亚)": {
            "🏛️ Top Firms": [
                {"name": "Brigard Urrutia", "url": "https://bu.com.co", "desc": "Leading Firm"},
                {"name": "Posse Herrera Ruiz", "url": "https://www.phrlegal.com", "desc": "M&A and Dispute"},
                {"name": "Gómez-Pinzón", "url": "https://gomezpinzon.com", "desc": "Full Service"},
                {"name": "Philippi (PPU)", "url": "https://ppulegal.com", "desc": "Regional Leader"},
            ],
            "⚖️ Official": [
                {"name": "Rama Judicial", "url": "https://www.ramajudicial.gov.co", "desc": "Judicial Branch"},
                {"name": "Corte Constitucional", "url": "https://www.corteconstitucional.gov.co", "desc": "Constitutional Court"},
            ]
        },
        "🇵🇪 Peru (秘鲁)": {
            "🏛️ Top Firms": [
                {"name": "Rodrigo, Elías & Medrano", "url": "https://www.estudiorodrigo.com", "desc": "Market Leader"},
                {"name": "Miranda & Amado", "url": "https://www.mirandaamado.com", "desc": "Corporate Elite"},
                {"name": "Payet, Rey, Cauvi", "url": "https://www.prcp.com.pe", "desc": "Finance & M&A"},
            ],
            "⚖️ Official": [{"name": "Poder Judicial", "url": "https://www.pj.gob.pe", "desc": "Judiciary"}]
        }
    },

    # ================= 🕌 中东与非洲 (Middle East & Africa) =================
    "🕌 Middle East & Africa (中东非洲)": {
        "🇦🇪 UAE (阿联酋)": {
            "🏛️ Local Giants & Intl": [
                {"name": "Al Tamimi & Co", "url": "https://www.tamimi.com", "desc": "Largest MENA Firm"},
                {"name": "Hadef & Partners", "url": "https://hadefpartners.com", "desc": "UAE Specialist"},
                {"name": "Afridi & Angell", "url": "https://afridi-angell.com", "desc": "Established Firm"},
                {"name": "Galadari", "url": "https://www.galadarilaw.com", "desc": "Dispute Resolution"},
                {"name": "Clyde & Co UAE", "url": "https://www.clydeco.com", "desc": "Top International"},
                {"name": "Allen & Overy UAE", "url": "https://www.allenovery.com", "desc": "Banking & Projects"},
            ],
            "⚖️ Official & Courts": [
                {"name": "DIFC Courts", "url": "https://www.difccourts.ae", "desc": "English Law Courts"},
                {"name": "ADGM Courts", "url": "https://www.adgm.com/courts", "desc": "Abu Dhabi Global Market"},
                {"name": "MoJ UAE", "url": "https://www.moj.gov.ae", "desc": "Ministry of Justice"},
                {"name": "SCA", "url": "https://www.sca.gov.ae", "desc": "Securities Authority"},
            ]
        },
        "🇸🇦 Saudi Arabia (沙特)": {
            "🏛️ Top Firms": [
                {"name": "Khoshaim & Assoc", "url": "https://www.khoshaim.com", "desc": "Top Independent"},
                {"name": "Zamakhchary", "url": "https://zllaw.sa", "desc": "Corporate & Regulatory"},
                {"name": "Abuhimed Alsheikh (AS&H)", "url": "https://www.ashlawksa.com", "desc": "Clifford Chance Ally"},
                {"name": "Megren Al-Shaalan", "url": "https://www.whitecase.com", "desc": "White & Case Ally"},
                {"name": "Derayah", "url": "https://derayahllc.com", "desc": "Dispute Resolution"},
            ],
            "⚖️ Official": [
                {"name": "MoJ KSA", "url": "https://www.moj.gov.sa", "desc": "Ministry of Justice"},
                {"name": "Saudi Laws", "url": "https://laws.boe.gov.sa", "desc": "Bureau of Experts"},
            ]
        },
        "🇿🇦 South Africa (南非)": {
            "🏛️ Big Five Firms": [
                {"name": "Bowmans", "url": "https://www.bowmanslaw.com", "desc": "Pan-African Leader"},
                {"name": "ENSafrica", "url": "https://www.ensafrica.com", "desc": "Largest in Africa"},
                {"name": "Webber Wentzel", "url": "https://www.webberwentzel.com", "desc": "Linklaters Ally"},
                {"name": "Werksmans", "url": "https://www.werksmans.com", "desc": "Corporate Commercial"},
                {"name": "Cliffe Dekker Hofmeyr", "url": "https://www.cliffedekkerhofmeyr.com", "desc": "Full Service"},
            ],
            "⚖️ Official": [
                {"name": "Constitutional Court", "url": "https://www.concourt.org.za", "desc": "Highest Court"},
                {"name": "SAFLII", "url": "http://www.saflii.org", "desc": "Free Legal Info"},
                {"name": "CIPC", "url": "http://www.cipc.co.za", "desc": "Companies Commission"},
            ]
        },
        "🇮🇱 Israel (以色列)": {
            "🏛️ Top Firms": [
                {"name": "Herzog Fox & Neeman", "url": "https://www.herzoglaw.co.il", "desc": "Top International"},
                {"name": "Meitar", "url": "https://meitar.com", "desc": "Tech & Corporate"},
                {"name": "Fischer (FBC)", "url": "https://www.fbclawyers.com", "desc": "Litigation & RE"},
                {"name": "Goldfarb Gross Seligman", "url": "https://www.goldfarb.com", "desc": "Mega Firm"},
                {"name": "Gornitzky", "url": "https://www.gornitzky.com", "desc": "Tax & Commercial"},
            ],
            "⚖️ Official": [
                {"name": "Judicial Authority", "url": "https://www.gov.il/en/departments/the_judicial_authority", "desc": "Courts"},
                {"name": "Nevo", "url": "https://www.nevo.co.il", "desc": "Legal Database"},
            ]
        },
        "🇪🇬 Egypt (埃及)": {
             "🏛️ Top Firms": [
                 {"name": "Matouk Bassiouny", "url": "https://matoukbassiouny.com", "desc": "MENA Leader"},
                 {"name": "Sharkawy & Sarhan", "url": "https://www.sharkawylaw.com", "desc": "Premium Corporate"},
                 {"name": "Zulficar & Partners", "url": "https://zulficarpartners.com", "desc": "Arbitration & Finance"},
                 {"name": "Shalakany", "url": "https://www.shalakany.com", "desc": "Oldest Firm"},
             ],
             "⚖️ Official": [{"name": "Court of Cassation", "url": "https://www.cc.gov.eg", "desc": "High Court"}]
        },
        "🇳🇬 Nigeria (尼日利亚)": {
            "🏛️ Top Firms": [
                {"name": "Aluko & Oyebode", "url": "https://www.aluko-oyebode.com", "desc": "Top Tier"},
                {"name": "Banwo & Ighodalo", "url": "https://www.banwo-ighodalo.com", "desc": "Corporate & Energy"},
                {"name": "Templars", "url": "https://www.templars-law.com", "desc": "Full Service"},
                {"name": "Udo Udoma (UUBO)", "url": "https://www.uubo.org", "desc": "Private Equity"},
            ],
            "⚖️ Official": [{"name": "CAC Nigeria", "url": "https://www.cac.gov.ng", "desc": "Corporate Affairs"}]
        },
        "🇰🇪 Kenya (肯尼亚)": {
            "🏛️ Top Firms": [
                {"name": "Anjarwalla & Khanna", "url": "https://www.africalegalnetwork.com/kenya", "desc": "ALN Leader"},
                {"name": "Bowmans Kenya", "url": "https://www.bowmanslaw.com", "desc": "Pan-African"},
                {"name": "Dentons Hamilton Harrison", "url": "https://www.dentons.com", "desc": "Oldest Firm"},
            ],
            "⚖️ Official": [{"name": "Kenya Law", "url": "http://kenyalaw.org", "desc": "Case Law"}]
        },
        "🇶🇦 Qatar (卡塔尔)": {
            "🏛️ Firms": [
                {"name": "Al Sulaiti", "url": "https://www.alsulaitilawfirm.com", "desc": "Full Service"},
                {"name": "Sharq Law Firm", "url": "https://sharqlawfirm.com", "desc": "Leading Local"},
            ],
            "⚖️ Official": [{"name": "QICDRC", "url": "https://www.qicdrc.gov.qa", "desc": "Intl Court"}]
        }
    },

    # ================= 🏝️ 离岸 (Offshore) =================
    "🏝️ Offshore (离岸中心)": {
        "🇰🇾 Cayman Islands (开曼)": {
            "🏛️ Firms": [
                {"name": "Maples Group", "url": "https://maples.com", "desc": "Global Offshore Leader"},
                {"name": "Walkers", "url": "https://www.walkersglobal.com", "desc": "Finance & Funds"},
                {"name": "Ogier", "url": "https://www.ogier.com", "desc": "Legal & Corporate"},
                {"name": "Campbells", "url": "https://www.campbellslegal.com", "desc": "Litigation"},
            ],
            "⚖️ Gov": [{"name": "CIMA", "url": "https://www.cima.ky", "desc": "Monetary Authority"}]
        },
        "🇻🇬 BVI (英属维尔京)": {
            "🏛️ Firms": [
                {"name": "Harneys", "url": "https://www.harneys.com", "desc": "Leading BVI Firm"},
                {"name": "Conyers", "url": "https://www.conyers.com", "desc": "Historical Leader"},
            ],
            "⚖️ Gov": [{"name": "BVI FSC", "url": "https://www.bvifsc.vg", "desc": "Regulator"}]
        }
    }
}

# -------------------------------------------------------------
# 4. 注入 CSS (硅谷风格)
# -------------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #FAFAFA; color: #111827; font-family: 'Inter', sans-serif; }
    header[data-testid="stHeader"] {display: none;}
    
    .main-title { font-size: 2.2rem; font-weight: 800; color: #111827; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1rem; color: #6B7280; margin-bottom: 2rem; }
    
    .category-header {
        font-size: 1.1rem; font-weight: 700; color: #374151; margin-top: 24px; margin-bottom: 12px;
        display: flex; align-items: center; border-bottom: 1px solid #E5E7EB; padding-bottom: 8px;
    }
    
    .grid-container {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; margin-bottom: 20px;
    }
    
    .card {
        background: #FFFFFF; border: 1px solid #F3F4F6; border-radius: 10px; padding: 16px;
        text-decoration: none; transition: transform 0.2s, box-shadow 0.2s; display: flex; flex-direction: column;
        height: 100%;
    }
    .card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-color: #E5E7EB; }
    
    .card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
    .icon-box {
        width: 36px; height: 36px; min-width: 36px; background: #FFF; border: 1px solid #F3F4F6;
        border-radius: 6px; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 2px;
    }
    .icon-img { width: 100%; height: 100%; object-fit: contain; }
    .card-name { font-size: 0.95rem; font-weight: 600; color: #111827; line-height: 1.2; }
    .card-desc { font-size: 0.8rem; color: #6B7280; line-height: 1.4; }
    
    a { text-decoration: none !important; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 5. 状态与语言
# -------------------------------------------------------------
if 'lang' not in st.session_state: st.session_state.lang = "ZH"

col_h, col_c = st.columns([1.5, 2])
with col_c:
    c_reg_g, c_reg_c, c_lang = st.columns([1.5, 1.5, 1])
    with c_lang:
        l = st.selectbox("Lang/语言", ["中文", "English"], index=0 if st.session_state.lang=="ZH" else 1, label_visibility="collapsed")
        st.session_state.lang = "ZH" if l == "中文" else "EN"

t = UI_TEXT[st.session_state.lang]

with col_h:
    st.markdown(f'<div class="main-title">{t["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-title">{t["subtitle"]}</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 6. 级联选择器 (Region Group -> Country)
# -------------------------------------------------------------
with c_reg_g:
    region_groups = list(DATA_SOURCE.keys())
    selected_group = st.selectbox(t["region_group_label"], region_groups, index=0, label_visibility="collapsed")

with c_reg_c:
    countries_in_group = list(DATA_SOURCE[selected_group].keys())
    selected_country = st.selectbox(t["country_label"], countries_in_group, index=0, label_visibility="collapsed")

# 获取最终数据
country_data = DATA_SOURCE[selected_group][selected_country]

# 如果是简化占位数据（如列表中有字符串占位符），这里可以做扩展处理，但目前结构已统一为字典列表。
all_cats = list(country_data.keys())

# -------------------------------------------------------------
# 7. 搜索与过滤
# -------------------------------------------------------------
col_s, col_f = st.columns([1, 2])
with col_s:
    search_query = st.text_input("Search", placeholder=t["search_placeholder"], label_visibility="collapsed")
with col_f:
    selected_cats = st.multiselect(t["filter_label"], all_cats, placeholder=t["filter_placeholder"], label_visibility="collapsed")

# -------------------------------------------------------------
# 8. 渲染逻辑 (Favicon API)
# -------------------------------------------------------------
def render_cards(tools):
    html = '<div class="grid-container">'
    for tool in tools:
        # 使用 Google Favicon API
        logo = f"https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url={tool['url']}&size=128"
        
        card = f"""
<a href="{tool['url']}" target="_blank" class="card">
    <div class="card-header">
        <div class="icon-box"><img src="{logo}" class="icon-img" loading="lazy"></div>
        <div class="card-name">{tool['name']}</div>
    </div>
    <div class="card-desc">{tool['desc']}</div>
</a>
        """
        html += card
    html += '</div>'
    return html

total = 0
final_html = ""

# 搜索模式
if search_query:
    res = []
    for cat, tools in country_data.items():
        if selected_cats and cat not in selected_cats: continue
        for tool in tools:
            if search_query.lower() in tool['name'].lower() or search_query.lower() in tool['desc'].lower():
                res.append(tool)
    if res:
        total = len(res)
        final_html = render_cards(res)
    else:
        st.info(t["no_result"])
# 浏览模式
else:
    cats = selected_cats if selected_cats else all_cats
    for cat in cats:
        tools = country_data[cat]
        if tools:
            total += len(tools)
            final_html += f'<div class="category-header">{cat}</div>'
            final_html += render_cards(tools)

if total > 0:
    st.caption(t["showing"].format(total))
    st.markdown(final_html, unsafe_allow_html=True)

st.markdown(f'<div style="margin-top:50px;text-align:center;color:#9CA3AF;font-size:0.8rem;border-top:1px solid #EEE;padding-top:20px;">{t["footer"]}</div>', unsafe_allow_html=True)

def render_bottom_nav(text_data):
    """
    渲染底部导航栏
    target="_self" 用于在当前窗口打开(通常是主页)
    target="_blank" 用于在新标签页打开
    class="nav-item active" 表示该项为当前激活状态
    """
    nav_html = f"""
    <div class="bottom-nav">
        <a href="https://youqian.streamlit.app/" class="nav-item active" target="_self">
            {text_data['nav_1']}
        </a>
        <a href="https://fangchan.streamlit.app/" class="nav-item" target="_blank">
            {text_data['nav_2']}
        </a>
        <a href="https://fangjia.streamlit.app/" class="nav-item" target="_blank">
            {text_data['nav_3']}
        </a>
        <a href="https://chuhai.streamlit.app/" class="nav-item" target="_blank">
            {text_data['nav_4']}
        </a>
        <a href="https://chuhai.streamlit.app/" class="nav-item" target="_blank">
            {text_data['nav_5']}
        </a>
        <a href="https://chuhai.streamlit.app/" class="nav-item" target="_blank">
            {text_data['nav_6']}
        </a>
        <a href="https://qfschina.streamlit.app/" class="nav-item" target="_blank">
            {text_data['nav_7']}
        </a>
        <a href="https://fangjia.streamlit.app/" class="nav-item" target="_blank">
            {text_data['nav_8']}
        </a>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)
    
# 调用渲染函数
render_bottom_nav(NAV_TEXT)
