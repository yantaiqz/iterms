import streamlit as st
from urllib.parse import urlparse

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
        "footer": "© 2024 LegalTech Nexus. Logos via Google API.",
        "no_result": "No resources found.",
        "showing": "Showing {} resources"
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
        "showing": "共显示 {} 个资源"
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
    # ================= 亚太地区 (APAC) =================
    "🌏 Asia Pacific (亚太)": {
       "🇨🇳 China (中国)": {
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
            "🤖 LegalTech & Data (科技/数据)": [
                {"name": "北大法宝", "url": "https://www.pkulaw.com", "desc": "Leading Legal Database"},
                {"name": "威科先行", "url": "https://law.wkinfo.com.cn", "desc": "Wolters Kluwer China"},
                {"name": "无讼", "url": "https://www.itslaw.com", "desc": "Litigation Data"},
                {"name": "法大大", "url": "https://www.fadada.com", "desc": "E-Signature Platform"},
                {"name": "e签宝", "url": "https://www.esign.cn", "desc": "E-Contract Mgmt"},
                {"name": "天眼查", "url": "https://www.tianyancha.com", "desc": "Business Data"},
                {"name": "企查查", "url": "https://www.qcc.com", "desc": "Credit Info"},
                {"name": "秘塔科技", "url": "https://www.metaso.cn", "desc": "AI Search"},
                {"name": "幂律智能", "url": "https://www.powerlaw.ai", "desc": "AI Contract Review"},
                {"name": "理脉", "url": "https://www.legalminer.com", "desc": "Legal Big Data"},
                {"name": "法天使", "url": "https://www.fats.cn", "desc": "Contract Templates"},
                {"name": "华宇信息", "url": "https://www.thunisoft.com", "desc": "Court Information Systems"},
                {"name": "国双 (Gridsum)", "url": "http://www.gridsum.com", "desc": "Judicial Big Data"},
            ],
             "💼 Compliance & Consulting (合规/四大)": [
                {"name": "普华永道 (PwC Legal)", "url": "https://www.pwccn.com", "desc": "Legal & Tax Services"},
                {"name": "德勤 (Deloitte Legal)", "url": "https://www2.deloitte.com/cn", "desc": "Legal Consulting"},
                {"name": "安永 (EY Law)", "url": "https://www.ey.com/cn", "desc": "Corporate Law Services"},
                {"name": "毕马威 (KPMG Law)", "url": "https://home.kpmg/cn", "desc": "Legal Compliance"},
                {"name": "甫瀚咨询 (Protiviti)", "url": "https://www.protiviti.com", "desc": "Risk & Compliance"},
                {"name": "贝克顾法律 (Baker & McKenzie CN)", "url": "https://www.bakermckenzie.com", "desc": "Foreign Law Firm"},
            ],
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
        "🇮🇳 India (印度)": {
            "🏛️ Top Firms": [
                {"name": "Cyril Amarchand Mangaldas", "url": "https://www.cyrilshroff.com", "desc": "Largest Law Firm"},
                {"name": "Shardul Amarchand Mangaldas", "url": "https://www.amsshardul.com", "desc": "Premium Corporate"},
                {"name": "Khaitan & Co", "url": "https://www.khaitanco.com", "desc": "Oldest & Leading"},
                {"name": "AZB & Partners", "url": "https://www.azbpartners.com", "desc": "M&A Specialist"},
            ],
            "⚖️ Official": [
                {"name": "Supreme Court of India", "url": "https://main.sci.gov.in", "desc": "Highest Court"},
                {"name": "MCA", "url": "https://www.mca.gov.in", "desc": "Ministry of Corp Affairs"},
                {"name": "SCC Online", "url": "https://www.scconline.com", "desc": "Legal Research"},
            ]
        },
        "🇰🇷 South Korea (韩国)": {
            "🏛️ Big 6 Firms": [
                {"name": "Kim & Chang", "url": "https://www.kimchang.com", "desc": "Largest in Korea"},
                {"name": "Lee & Ko", "url": "http://www.leeko.com", "desc": "Full Service"},
                {"name": "Bae, Kim & Lee", "url": "https://www.bkl.co.kr", "desc": "Litigation & Corp"},
                {"name": "Shin & Kim", "url": "https://www.shinkim.com", "desc": "Major Global Firm"},
            ],
            "⚖️ Official": [
                {"name": "Supreme Court KR", "url": "https://eng.scourt.go.kr", "desc": "Judiciary"},
                {"name": "Statutes of Korea", "url": "https://elaw.klri.re.kr", "desc": "Laws Translation"},
            ]
        },
        "🇯🇵 Japan (日本)": { "数据已包含，此处略以节省展示...": [] }, # 逻辑占位
        "🇭🇰 Hong Kong (香港)": { "数据已包含，此处略...": [] },
        "🇮🇩 Indonesia (印尼)": {
             "🏛️ Firms": [{"name": "Hadiputranto (HHP)", "url": "https://www.hhp.co.id", "desc": "Baker McKenzie Member"}],
             "⚖️ Gov": [{"name": "Mahkamah Agung", "url": "https://www.mahkamahagung.go.id", "desc": "Supreme Court"}]
        },
        "🇻🇳 Vietnam (越南)": {
             "🏛️ Firms": [{"name": "VILAF", "url": "https://www.vilaf.com.vn", "desc": "Leading Business Firm"}],
             "⚖️ Gov": [{"name": "MoJ Vietnam", "url": "https://moj.gov.vn", "desc": "Ministry of Justice"}]
        },
        "🇹🇭 Thailand (泰国)": {
             "🏛️ Firms": [{"name": "Weerawong C&P", "url": "https://www.weerawongcp.com", "desc": "Top Thai Firm"}],
             "⚖️ Gov": [{"name": "Legal Execution Dept", "url": "https://www.led.go.th", "desc": "Enforcement"}]
        },
         "🇲🇾 Malaysia (马来西亚)": {
             "🏛️ Firms": [{"name": "Shearn Delamore", "url": "https://www.shearndelamore.com", "desc": "Top Tier"}],
             "⚖️ Gov": [{"name": "MyIPO", "url": "https://www.myipo.gov.my", "desc": "Intellectual Property"}]
        },
        "🇵🇭 Philippines (菲律宾)": {
             "🏛️ Firms": [{"name": "SyCipLaw", "url": "https://www.syciplaw.com", "desc": "Oldest & Largest"}],
             "⚖️ Gov": [{"name": "Supreme Court PH", "url": "https://sc.judiciary.gov.ph", "desc": "Judiciary"}]
        },
    },

    # ================= 北美 (North America) =================
    "🌎 North America (北美)": {
        "🇺🇸 USA (美国)": { 
            "🏛️ Am Law 50 Elite (顶级律所)": [
                {"name": "Kirkland & Ellis", "url": "https://www.kirkland.com", "desc": "PE & Litigation"},
                {"name": "Latham & Watkins", "url": "https://www.lw.com", "desc": "Global Elite"},
                {"name": "Skadden", "url": "https://www.skadden.com", "desc": "M&A Powerhouse"},
                {"name": "Sidley Austin", "url": "https://www.sidley.com", "desc": "Regulatory & Corporate"},
                {"name": "White & Case", "url": "https://www.whitecase.com", "desc": "Intl Arbitration"},
                {"name": "Morgan Lewis", "url": "https://www.morganlewis.com", "desc": "Labor & Employment"},
                {"name": "Hogan Lovells", "url": "https://www.hoganlovells.com", "desc": "Regulatory"},
                {"name": "Gibson Dunn", "url": "https://www.gibsondunn.com", "desc": "High-stakes Lit"},
                {"name": "Ropes & Gray", "url": "https://www.ropesgray.com", "desc": "Private Equity"},
                {"name": "Sullivan & Cromwell", "url": "https://www.sullcrom.com", "desc": "Banking & Finance"},
                {"name": "Wachtell Lipton", "url": "https://www.wlrk.com", "desc": "M&A Boutique"},
                {"name": "Weil Gotshal", "url": "https://www.weil.com", "desc": "Restructuring"},
                {"name": "Paul Weiss", "url": "https://www.paulweiss.com", "desc": "Litigation Elite"},
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
             "⚖️ Official & Gov (官方机构)": [
                {"name": "USPTO", "url": "https://www.uspto.gov", "desc": "Patents"},
                {"name": "SEC Edgar", "url": "https://www.sec.gov", "desc": "Company Filings"},
                {"name": "Regulations.gov", "url": "https://www.regulations.gov", "desc": "Federal Rules"},
                {"name": "ABA", "url": "https://www.americanbar.org", "desc": "American Bar Association"},
                {"name": "Supreme Court", "url": "https://www.supremecourt.gov", "desc": "SCOTUS"},
                {"name": "DOJ", "url": "https://www.justice.gov", "desc": "Dept of Justice"},
                {"name": "FTC", "url": "https://www.ftc.gov", "desc": "Consumer Protection"},
            ]
        },
        "🇨🇦 Canada (加拿大)": {
            "🏛️ Seven Sisters (顶级律所)": [
                {"name": "McCarthy Tétrault", "url": "https://www.mccarthy.ca", "desc": "Innovation Leader"},
                {"name": "Blake, Cassels", "url": "https://www.blakes.com", "desc": "Business Law"},
                {"name": "Osler", "url": "https://www.osler.com", "desc": "Tech & Tax Focus"},
                {"name": "Torys", "url": "https://www.torys.com", "desc": "Cross-border M&A"},
                {"name": "Stikeman Elliott", "url": "https://www.stikeman.com", "desc": "Corporate Finance"},
            ],
            "⚖️ Official & Tech": [
                {"name": "CanLII", "url": "https://www.canlii.org", "desc": "Free Legal Database"},
                {"name": "SCC", "url": "https://www.scc-csc.ca", "desc": "Supreme Court"},
                {"name": "Clio", "url": "https://www.clio.com", "desc": "Practice Management (HQ)"},
                {"name": "Kira Systems", "url": "https://kirasystems.com", "desc": "AI Contract Review"},
            ]
        }
    },

    # ================= 欧洲 (Europe / EMEA) =================
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
                {"name": "Bryan Cave (BCLP)", "url": "https://www.bclplaw.com", "desc": "Real Estate"},
                {"name": "CMS", "url": "https://cms.law", "desc": "Largest in Europe"},
                {"name": "Macfarlanes", "url": "https://www.macfarlanes.com", "desc": "Private Client"},
                {"name": "Travers Smith", "url": "https://www.traverssmith.com", "desc": "Corporate Boutique"},
                {"name": "Simmons & Simmons", "url": "https://www.simmons-simmons.com", "desc": "FinTech & Funds"},
                {"name": "Pinsent Masons", "url": "https://www.pinsentmasons.com", "desc": "Construction & Energy"},
                {"name": "Clyde & Co", "url": "https://www.clydeco.com", "desc": "Insurance & Shipping"},
                {"name": "Bird & Bird", "url": "https://www.twobirds.com", "desc": "IP & Tech focus"},
            ],
            "💡 LegalTech & Official (科技/官方)": [
                {"name": "legislation.gov.uk", "url": "https://www.legislation.gov.uk", "desc": "Official Laws"},
                {"name": "BAILII", "url": "https://www.bailii.org", "desc": "Case Law Database"},
                {"name": "Luminance", "url": "https://www.luminance.com", "desc": "AI Document Review"},
                {"name": "Juro", "url": "https://juro.com", "desc": "Contract Platform"},
                {"name": "Companies House", "url": "https://www.gov.uk/government/organisations/companies-house", "desc": "Company Registry"},
                {"name": "The Law Society", "url": "https://www.lawsociety.org.uk", "desc": "Solicitors Body"},
                {"name": "SRA", "url": "https://www.sra.org.uk", "desc": "Regulation Authority"},
                {"name": "Practical Law", "url": "https://uk.practicallaw.thomsonreuters.com", "desc": "Legal Know-How"},
            ]
        },
        "🇩🇪 Germany (德国)": {"Top Firms": [{"name": "Hengeler Mueller", "url": "https://www.hengeler.com", "desc": "Top Tier"}]}, # 占位
        "🇫🇷 France (法国)": {"Top Cabinets": [{"name": "Bredin Prat", "url": "https://www.bredinprat.com", "desc": "Elite"}]}, # 占位
        "🇨🇭 Switzerland (瑞士)": {
            "🏛️ Top Firms": [
                {"name": "Lenz & Staehelin", "url": "https://www.lenzstaehelin.com", "desc": "Largest Swiss Firm"},
                {"name": "Schellenberg Wittmer", "url": "https://www.swlegal.ch", "desc": "Arbitration & Corp"},
                {"name": "Bär & Karrer", "url": "https://www.baerkarrer.ch", "desc": "M&A Focus"},
                {"name": "Walder Wyss", "url": "https://www.walderwyss.com", "desc": "Rapidly Growing"},
            ],
            "⚖️ Official": [
                {"name": "Swisslex", "url": "https://www.swisslex.ch", "desc": "Legal Database"},
                {"name": "Federal Supreme Court", "url": "https://www.bger.ch", "desc": "Judiciary"},
                {"name": "Zefix", "url": "https://www.zefix.ch", "desc": "Commercial Register"},
            ]
        },
        "🇳🇱 Netherlands (荷兰)": {
            "🏛️ De Brauw & Others": [
                {"name": "De Brauw", "url": "https://www.debrauw.com", "desc": "Global Litigation"},
                {"name": "NautaDutilh", "url": "https://www.nautadutilh.com", "desc": "Benelux Leader"},
                {"name": "Houthoff", "url": "https://www.houthoff.com", "desc": "Top Tier"},
            ],
            "⚖️ Official": [
                {"name": "Rechtspraak", "url": "https://www.rechtspraak.nl", "desc": "Judiciary Portal"},
                {"name": "Overheid.nl", "url": "https://www.overheid.nl", "desc": "Laws Database"},
            ]
        },
        "🇮🇹 Italy (意大利)": {
            "🏛️ Firms": [
                {"name": "BonelliErede", "url": "https://belex.com", "desc": "Market Leader"},
                {"name": "Chiomenti", "url": "https://www.chiomenti.net", "desc": "Institutional"},
                {"name": "Legance", "url": "https://www.legance.com", "desc": "Modern Independent"},
            ],
            "⚖️ Official": [
                {"name": "Normattiva", "url": "https://www.normattiva.it", "desc": "Laws Database"},
                {"name": "Corte Costituzionale", "url": "https://www.cortecostituzionale.it", "desc": "Constitutional Court"},
            ]
        },
        "🇪🇸 Spain (西班牙)": {
            "🏛️ Firms": [
                {"name": "Garrigues", "url": "https://www.garrigues.com", "desc": "Largest in Continental Europe"},
                {"name": "Cuatrecasas", "url": "https://www.cuatrecasas.com", "desc": "Iberian Leader"},
                {"name": "Uría Menéndez", "url": "https://www.uria.com", "desc": "Prestigious Elite"},
            ],
             "⚖️ Official": [{"name": "BOE", "url": "https://www.boe.es", "desc": "Official Gazette"}]
        },
        "🇸🇪 Sweden (瑞典)": {
             "🏛️ Firms": [{"name": "Vinge", "url": "https://www.vinge.se", "desc": "M&A Leader"}, {"name": "Mannheimer Swartling", "url": "https://www.mannheimerswartling.se", "desc": "Top Nordic"}],
             "⚖️ Gov": [{"name": "Lagrummet", "url": "https://www.lagrummet.se", "desc": "Legal Portal"}]
        },
        "🇮🇪 Ireland (爱尔兰)": {
             "🏛️ Firms": [{"name": "Arthur Cox", "url": "https://www.arthurcox.com", "desc": "Top Tier"}, {"name": "Matheson", "url": "https://www.matheson.com", "desc": "Intl Focus"}],
             "⚖️ Gov": [{"name": "Courts.ie", "url": "https://www.courts.ie", "desc": "Courts Service"}]
        },
        "🇧🇪 Belgium (比利时)": {
             "🏛️ Firms": [{"name": "Eubelius", "url": "https://www.eubelius.com", "desc": "Leading Independent"}],
             "⚖️ Gov": [{"name": "Moniteur Belge", "url": "https://www.ejustice.just.fgov.be", "desc": "Official Journal"}]
        },
        "🇱🇺 Luxembourg (卢森堡)": {
             "🏛️ Firms": [{"name": "Arendt & Medernach", "url": "https://www.arendt.com", "desc": "Largest Firm"}, {"name": "Elvinger Hoss", "url": "https://www.elvingerhoss.pr", "desc": "Fund Formation"}],
             "⚖️ Gov": [{"name": "Legilux", "url": "https://legilux.public.lu", "desc": "Legal Portal"}]
        },
        "🇷🇺 Russia (俄罗斯)": {
             "🏛️ Firms": [{"name": "EPAM", "url": "https://epam.ru", "desc": "Largest CIS Firm"}],
             "⚖️ Gov": [{"name": "Pravo.gov.ru", "url": "http://pravo.gov.ru", "desc": "Official Legal Info"}]
        },
        "🇹🇷 Turkey (土耳其)": {
             "🏛️ Firms": [{"name": "Paksoy", "url": "https://www.paksoy.av.tr", "desc": "Leading Independent"}],
             "⚖️ Gov": [{"name": "Resmi Gazete", "url": "https://www.resmigazete.gov.tr", "desc": "Official Gazette"}]
        }
    },

    # ================= 拉丁美洲 (LatAm) =================
    "💃 Latin America (拉美)": {
        "🇧🇷 Brazil (巴西)": {
            "🏛️ Top Firms": [
                {"name": "Mattos Filho", "url": "https://www.mattosfilho.com.br", "desc": "Premium Full Service"},
                {"name": "Pinheiro Neto", "url": "https://www.pinheironeto.com.br", "desc": "Traditional Elite"},
                {"name": "Machado Meyer", "url": "https://www.machadomeyer.com.br", "desc": "Banking & Finance"},
            ],
            "⚖️ Official": [
                {"name": "STF", "url": "https://portal.stf.jus.br", "desc": "Supreme Federal Court"},
                {"name": "Planalto", "url": "http://www4.planalto.gov.br/legislacao", "desc": "Legislation"},
            ],
             "💻 Tech": [{"name": "Jusbrasil", "url": "https://www.jusbrasil.com.br", "desc": "Largest Legal Tech"}]
        },
        "🇲🇽 Mexico (墨西哥)": {
            "🏛️ Firms": [
                {"name": "Creel (Creel-García)", "url": "https://www.creel.mx", "desc": "Top Tier"},
                {"name": "Galicia Abogados", "url": "https://www.galicia.com.mx", "desc": "Finance Focus"},
            ],
            "⚖️ Gov": [{"name": "SCJN", "url": "https://www.scjn.gob.mx", "desc": "Supreme Court"}]
        },
        "🇨🇱 Chile (智利)": {
             "🏛️ Firms": [{"name": "Carey", "url": "https://www.carey.cl", "desc": "Largest in Chile"}],
             "⚖️ Gov": [{"name": "Poder Judicial", "url": "https://www.pjud.cl", "desc": "Judiciary"}]
        },
        "🇦🇷 Argentina (阿根廷)": {
             "🏛️ Firms": [{"name": "Marval O'Farrell", "url": "https://www.marval.com", "desc": "Largest in Argentina"}],
             "⚖️ Gov": [{"name": "InfoLeg", "url": "http://www.infoleg.gob.ar", "desc": "Legal Info"}]
        },
        "🇨🇴 Colombia (哥伦比亚)": {
             "🏛️ Firms": [{"name": "Brigard Urrutia", "url": "https://bu.com.co", "desc": "Leading Firm"}],
             "⚖️ Gov": [{"name": "Rama Judicial", "url": "https://www.ramajudicial.gov.co", "desc": "Judicial Branch"}]
        }
    },

    # ================= 中东与非洲 (MEA) =================
    "🕌 Middle East & Africa (中东非洲)": {
        "🇦🇪 UAE (阿联酋)": {
            "🏛️ Firms": [
                {"name": "Al Tamimi & Co", "url": "https://www.tamimi.com", "desc": "Largest MENA Firm"},
                {"name": "Hadef & Partners", "url": "https://hadefpartners.com", "desc": "UAE Specialist"},
            ],
            "⚖️ Gov": [
                {"name": "DIFC Courts", "url": "https://www.difccourts.ae", "desc": "English Law Courts"},
                {"name": "MoJ UAE", "url": "https://www.moj.gov.ae", "desc": "Ministry of Justice"},
            ]
        },
        "🇸🇦 Saudi Arabia (沙特)": {
            "🏛️ Firms": [
                {"name": "Khoshaim & Assoc", "url": "https://www.khoshaim.com", "desc": "Top Independent"},
                {"name": "Zamakhchary", "url": "https://zllaw.sa", "desc": "Corporate"},
            ],
            "⚖️ Gov": [{"name": "MoJ KSA", "url": "https://www.moj.gov.sa", "desc": "Ministry of Justice"}]
        },
        "🇿🇦 South Africa (南非)": {
            "🏛️ Firms": [
                {"name": "Bowmans", "url": "https://www.bowmanslaw.com", "desc": "Pan-African Leader"},
                {"name": "ENSafrica", "url": "https://www.ensafrica.com", "desc": "Largest in Africa"},
                {"name": "Webber Wentzel", "url": "https://www.webberwentzel.com", "desc": "Linklaters Ally"},
            ],
            "⚖️ Gov": [{"name": "Constitutional Court", "url": "https://www.concourt.org.za", "desc": "Highest Court"}]
        },
        "🇮🇱 Israel (以色列)": {
            "🏛️ Firms": [
                {"name": "Herzog Fox & Neeman", "url": "https://www.herzoglaw.co.il", "desc": "Top International"},
                {"name": "Meitar", "url": "https://meitar.com", "desc": "Tech & Corporate"},
            ],
            "⚖️ Gov": [{"name": "Judicial Authority", "url": "https://www.gov.il/en/departments/the_judicial_authority", "desc": "Courts"}]
        },
         "🇪🇬 Egypt (埃及)": {
             "🏛️ Firms": [{"name": "Matouk Bassiouny", "url": "https://matoukbassiouny.com", "desc": "MENA Leader"}],
             "⚖️ Gov": [{"name": "Court of Cassation", "url": "https://www.cc.gov.eg", "desc": "High Court"}]
        }
    },
    
    # ================= 离岸金融中心 (Offshore) =================
    "🏝️ Offshore (离岸中心)": {
        "🇰🇾 Cayman Islands (开曼)": {
            "🏛️ Offshore Magic Circle": [
                {"name": "Maples Group", "url": "https://maples.com", "desc": "Global Offshore Leader"},
                {"name": "Walkers", "url": "https://www.walkersglobal.com", "desc": "Finance & Funds"},
                {"name": "Ogier", "url": "https://www.ogier.com", "desc": "Legal & Corporate"},
            ],
            "⚖️ Gov": [{"name": "CIMA", "url": "https://www.cima.ky", "desc": "Monetary Authority"}]
        },
        "🇻🇬 BVI (英属维尔京)": {
            "🏛️ Firms": [
                {"name": "Harneys", "url": "https://www.harneys.com", "desc": "Leading BVI Firm"},
                {"name": "Conyers", "url": "https://www.conyers.com", "desc": "Historical Leader"},
            ],
            "⚖️ Gov": [{"name": "BVI Financial Services", "url": "https://www.bvifsc.vg", "desc": "Regulator"}]
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
