import streamlit as st
from urllib.parse import urlparse

# -------------------------------------------------------------
# 1. 页面配置
# -------------------------------------------------------------
st.set_page_config(
    page_title="LegalTech Nexus Global Ultimate",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------------
# 2. 国际化 UI 文本 (i18n)
# -------------------------------------------------------------
UI_TEXT = {
    "EN": {
        "title": "LegalTech Nexus Global",
        "subtitle": "The definitive directory of 500+ top law firms, legal tech, compliance, and judiciary resources.",
        "search_placeholder": "Search for firms (e.g., Clifford Chance), tools, or agencies...",
        "filter_placeholder": "Filter by Category",
        "filter_label": "Filter",
        "region_label": "Select Region",
        "footer": "© 2024 LegalTech Nexus. Auto-curated logos via Google API.",
        "no_result": "No resources found matching your criteria.",
        "showing": "Showing {} resources"
    },
    "ZH": {
        "title": "全球法律科技导航 Ultimate",
        "subtitle": "汇集全球 500+ 顶尖律所、法律科技、合规咨询与司法资源。",
        "search_placeholder": "搜索律所 (如: 金杜)、工具或监管机构...",
        "filter_placeholder": "按分类筛选 (如: 顶级律所, 官方司法...)",
        "filter_label": "分类筛选",
        "region_label": "选择地区",
        "footer": "© 2024 LegalTech Nexus. Logo 由 Google API 自动生成。",
        "no_result": "未找到匹配的资源。",
        "showing": "共显示 {} 个资源"
    }
}

# -------------------------------------------------------------
# 3. 核心大数据库 (Massive Data Source)
# -------------------------------------------------------------
DATA_SOURCE = {
    "🇨🇳 CN (China)": {
        "🏛️ Red Circle & Top Firms (红圈/顶级律所)": [
            {"name": "金杜 (KWM)", "desc": "King & Wood Mallesons", "url": "https://www.kwm.com"},
            {"name": "君合 (JunHe)", "desc": "Pioneer of Chinese firms", "url": "https://www.junhe.com"},
            {"name": "中伦 (Zhong Lun)", "desc": "Full service elite", "url": "https://www.zhonglun.com"},
            {"name": "方达 (Fangda)", "desc": "M&A and Capital Markets", "url": "https://www.fangdalaw.com"},
            {"name": "海问 (Haiwen)", "desc": "Prestigious securities practice", "url": "https://www.haiwen-law.com"},
            {"name": "汉坤 (Han Kun)", "desc": "Leading in PE/VC & Tech", "url": "https://www.hankunlaw.com"},
            {"name": "竞天公诚 (Jingtian)", "desc": "Capital markets specialist", "url": "http://www.jingtian.com"},
            {"name": "通商 (Commerce & Finance)", "desc": "Capital markets & Dispute", "url": "http://www.tongshang.com"},
            {"name": "环球 (Global Law)", "desc": "Oldest PRC law firm", "url": "http://www.glo.com.cn"},
        ],
        "🏙️ Major Commercial Firms (大型综合律所)": [
            {"name": "锦天城 (AllBright)", "desc": "Shanghai-based giant", "url": "https://www.allbrightlaw.com"},
            {"name": "大成 (Dentons CN)", "desc": "Largest global coverage", "url": "https://www.dentons.com.cn"},
            {"name": "盈科 (Yingke)", "desc": "Global network firm", "url": "http://www.yingkelawyer.com"},
            {"name": "国浩 (Grandall)", "desc": "IPO/Securities focus", "url": "http://www.grandall.com.cn"},
            {"name": "天元 (Tian Yuan)", "desc": "Comprehensive practice", "url": "http://www.tylaw.com.cn"},
            {"name": "中银 (Zhong Yin)", "desc": "Banking & Finance", "url": "http://www.zhongyinlawyer.com"},
            {"name": "德恒 (DeHeng)", "desc": "Government & Infrastructure", "url": "http://www.dehenglaw.com"},
            {"name": "京师 (Jingsh)", "desc": "Large scale partnership", "url": "http://www.jingsh.com"},
            {"name": "隆安 (Long An)", "desc": "IP & Commercial", "url": "http://www.longanlaw.com"},
            {"name": "康达 (Kangda)", "desc": "Criminal Defense & Corp", "url": "http://www.kangdalawyers.com"},
            {"name": "泰和泰 (Tahota)", "desc": "Leading West China firm", "url": "http://www.tahota.com"},
            {"name": "建纬 (City Development)", "desc": "Construction & Real Estate", "url": "http://www.jianwei.com"},
            {"name": "广悦 (Guangyue)", "desc": "Guangzhou leading firm", "url": "http://www.guangyuelaw.com"},
            {"name": "炜衡 (Weiheng)", "desc": "Comprehensive litigation", "url": "http://www.weihenglaw.com"},
        ],
        "💎 Boutique & Specialist (精品/外资)": [
            {"name": "安杰世泽 (AnJie Broad)", "desc": "Insurance & Antitrust", "url": "http://www.anjielaw.com"},
            {"name": "汇业 (Hui Ye)", "desc": "Corporate & Compliance", "url": "http://www.huiyelaw.com"},
            {"name": "植德 (Merits & Tree)", "desc": "Asset Management", "url": "http://www.meritsandtree.com"},
            {"name": "天同 (Tiantong)", "desc": "Supreme Court Litigation", "url": "https://www.tiantonglaw.com"},
            {"name": "Llinks (通力)", "desc": "Financial services & Asset Mgt", "url": "http://www.llinkslaw.com"},
            {"name": "DaHui (达辉)", "desc": "TMT & Compliance", "url": "http://www.dahuilawyers.com"},
        ],
        "⚖️ Official & Judiciary (官方司法)": [
            {"name": "裁判文书网", "desc": "Supreme Court Judgments", "url": "https://wenshu.court.gov.cn"},
            {"name": "法律法规库", "desc": "Official Laws Database", "url": "https://flk.npc.gov.cn"},
            {"name": "执行信息网", "desc": "Enforcement Information", "url": "http://zxgk.court.gov.cn"},
            {"name": "庭审公开网", "desc": "Court Trial Live", "url": "http://tingshen.court.gov.cn"},
            {"name": "知识产权局", "desc": "CNIPA", "url": "https://www.cnipa.gov.cn"},
            {"name": "市监总局", "desc": "SAMR (Antitrust)", "url": "https://www.samr.gov.cn"},
            {"name": "网信办", "desc": "CAC (Cybersecurity)", "url": "http://www.cac.gov.cn"},
            {"name": "证监会", "desc": "CSRC", "url": "http://www.csrc.gov.cn"},
            {"name": "最高检", "desc": "SPP", "url": "https://www.spp.gov.cn"},
            {"name": "司法部", "desc": "Ministry of Justice", "url": "http://www.moj.gov.cn"},
        ],
        "🤖 LegalTech & Data (科技/数据)": [
            {"name": "北大法宝", "desc": "Leading Legal Database", "url": "https://www.pkulaw.com"},
            {"name": "威科先行", "desc": "Wolters Kluwer China", "url": "https://law.wkinfo.com.cn"},
            {"name": "无讼", "desc": "Litigation Data", "url": "https://www.itslaw.com"},
            {"name": "法大大", "desc": "E-Signature", "url": "https://www.fadada.com"},
            {"name": "e签宝", "desc": "Contract Mgmt", "url": "https://www.esign.cn"},
            {"name": "天眼查", "desc": "Business Data", "url": "https://www.tianyancha.com"},
            {"name": "企查查", "desc": "Credit Info", "url": "https://www.qcc.com"},
            {"name": "秘塔科技", "desc": "AI Translation", "url": "https://www.metaso.cn"},
            {"name": "幂律智能", "desc": "AI Contract Review", "url": "https://www.powerlaw.ai"},
            {"name": "理脉", "desc": "Legal Big Data", "url": "https://www.legalminer.com"},
            {"name": "Alpha (iCourt)", "desc": "Practice Management", "url": "https://www.icourt.cc"},
            {"name": "聚法案例", "desc": "Case Visualization", "url": "https://www.jufanli.com"},
            {"name": "法天使", "desc": "Contract Templates", "url": "https://www.fats.cn"},
        ]
    },
    "🇺🇸 US (USA)": {
        "🏛️ Am Law 100 Elite (顶级律所)": [
            {"name": "Kirkland & Ellis", "desc": "#1 Revenue, PE & Litigation", "url": "https://www.kirkland.com"},
            {"name": "Latham & Watkins", "desc": "Global Elite", "url": "https://www.lw.com"},
            {"name": "DLA Piper", "desc": "Global Reach", "url": "https://www.dlapiper.com"},
            {"name": "Baker McKenzie", "desc": "Cross-border specialist", "url": "https://www.bakermckenzie.com"},
            {"name": "Skadden", "desc": "M&A Powerhouse", "url": "https://www.skadden.com"},
            {"name": "Sidley Austin", "desc": "Regulatory & Corporate", "url": "https://www.sidley.com"},
            {"name": "White & Case", "desc": "Intl Arbitration", "url": "https://www.whitecase.com"},
            {"name": "Morgan Lewis", "desc": "Labor & Employment", "url": "https://www.morganlewis.com"},
            {"name": "Hogan Lovells", "desc": "Regulatory", "url": "https://www.hoganlovells.com"},
            {"name": "Jones Day", "desc": "Litigation", "url": "https://www.jonesday.com"},
            {"name": "Gibson Dunn", "desc": "High-stakes Litigation", "url": "https://www.gibsondunn.com"},
            {"name": "Ropes & Gray", "desc": "Private Equity", "url": "https://www.ropesgray.com"},
            {"name": "Sullivan & Cromwell", "desc": "Banking & Finance", "url": "https://www.sullcrom.com"},
            {"name": "Davis Polk", "desc": "Capital Markets", "url": "https://www.davispolk.com"},
            {"name": "Wachtell Lipton", "desc": "Most profitable M&A", "url": "https://www.wlrk.com"},
            {"name": "Paul Weiss", "desc": "Litigation elite", "url": "https://www.paulweiss.com"},
            {"name": "Cravath", "desc": "White shoe prestige", "url": "https://www.cravath.com"},
            {"name": "Simpson Thacher", "desc": "PE & Banking", "url": "https://www.stblaw.com"},
            {"name": "Cleary Gottlieb", "desc": "Intl Finance", "url": "https://www.clearygottlieb.com"},
            {"name": "Weil Gotshal", "desc": "Restructuring", "url": "https://www.weil.com"},
        ],
        "🦄 Tech & Boutique Firms (科技/精品所)": [
            {"name": "Cooley", "desc": "Tech & Life Sciences", "url": "https://www.cooley.com"},
            {"name": "Wilson Sonsini", "desc": "Silicon Valley Pioneer", "url": "https://www.wsgr.com"},
            {"name": "Fenwick & West", "desc": "Tech Transactions", "url": "https://www.fenwick.com"},
            {"name": "Quinn Emanuel", "desc": "Business Litigation Only", "url": "https://www.quinnemanuel.com"},
            {"name": "Fragomen", "desc": "Immigration Law", "url": "https://www.fragomen.com"},
            {"name": "Littler Mendelson", "desc": "Employment Law", "url": "https://www.littler.com"},
            {"name": "Perkins Coie", "desc": "Microsoft/Amazon Counsel", "url": "https://www.perkinscoie.com"},
            {"name": "Orrick", "desc": "Innovation focus", "url": "https://www.orrick.com"},
            {"name": "Goodwin", "desc": "Life Sciences & RE", "url": "https://www.goodwinlaw.com"},
            {"name": "WilmerHale", "desc": "IP & Appellate", "url": "https://www.wilmerhale.com"},
        ],
        "💻 LegalTech & Research (法律科技)": [
            {"name": "Westlaw", "desc": "Thomson Reuters", "url": "https://legal.thomsonreuters.com"},
            {"name": "LexisNexis", "desc": "Legal Research", "url": "https://www.lexisnexis.com"},
            {"name": "Bloomberg Law", "desc": "Integrated Data", "url": "https://pro.bloomberglaw.com"},
            {"name": "Casetext", "desc": "AI Research (CoCounsel)", "url": "https://casetext.com"},
            {"name": "Ironclad", "desc": "CLM Platform", "url": "https://ironcladapp.com"},
            {"name": "Clio", "desc": "Practice Management", "url": "https://www.clio.com"},
            {"name": "DocuSign", "desc": "E-Signatures", "url": "https://www.docusign.com"},
            {"name": "Relativity", "desc": "E-Discovery", "url": "https://www.relativity.com"},
            {"name": "Everlaw", "desc": "Cloud Litigation", "url": "https://www.everlaw.com"},
            {"name": "Harvey", "desc": "GenAI for Law", "url": "https://www.harvey.ai"},
            {"name": "LegalZoom", "desc": "Consumer Legal", "url": "https://www.legalzoom.com"},
            {"name": "Rocket Lawyer", "desc": "Docs & Advice", "url": "https://www.rocketlawyer.com"},
            {"name": "Fastcase", "desc": "Affordable Research", "url": "https://www.fastcase.com"},
            {"name": "Logikcull", "desc": "Instant Discovery", "url": "https://www.logikcull.com"},
        ],
        "🏛️ Government (政府机构)": [
            {"name": "USPTO", "desc": "Patents", "url": "https://www.uspto.gov"},
            {"name": "SEC Edgar", "desc": "Company Filings", "url": "https://www.sec.gov"},
            {"name": "Regulations.gov", "desc": "Federal Rules", "url": "https://www.regulations.gov"},
            {"name": "Copyright.gov", "desc": "US Copyright Office", "url": "https://www.copyright.gov"},
            {"name": "PACER", "desc": "Court Records", "url": "https://pacer.uscourts.gov"},
            {"name": "Supreme Court", "desc": "SCOTUS", "url": "https://www.supremecourt.gov"},
            {"name": "FTC", "desc": "Consumer Protection", "url": "https://www.ftc.gov"},
        ]
    },
    "🇬🇧 UK (United Kingdom)": {
        "🏰 Magic & Silver Circle (顶尖律所)": [
            {"name": "Allen & Overy", "desc": "Merged A&O Shearman", "url": "https://www.allenovery.com"},
            {"name": "Clifford Chance", "desc": "Global Finance", "url": "https://www.cliffordchance.com"},
            {"name": "Freshfields", "desc": "Corporate & M&A", "url": "https://www.freshfields.com"},
            {"name": "Linklaters", "desc": "Corporate Elite", "url": "https://www.linklaters.com"},
            {"name": "Slaughter and May", "desc": "Prestigious Blue-blood", "url": "https://www.slaughterandmay.com"},
            {"name": "Herbert Smith Freehills", "desc": "Litigation Powerhouse", "url": "https://www.herbertsmithfreehills.com"},
            {"name": "Ashurst", "desc": "Projects & Finance", "url": "https://www.ashurst.com"},
            {"name": "Bryan Cave (BCLP)", "desc": "Real Estate", "url": "https://www.bclplaw.com"},
            {"name": "CMS", "desc": "Largest in Europe", "url": "https://cms.law"},
            {"name": "Macfarlanes", "desc": "Private Client & Corp", "url": "https://www.macfarlanes.com"},
            {"name": "Travers Smith", "desc": "Corporate Boutique", "url": "https://www.traverssmith.com"},
        ],
        "🌍 International & City Firms (国际/城市所)": [
            {"name": "Eversheds Sutherland", "desc": "Transatlantic", "url": "https://www.eversheds-sutherland.com"},
            {"name": "Simmons & Simmons", "desc": "FinTech & Funds", "url": "https://www.simmons-simmons.com"},
            {"name": "Pinsent Masons", "desc": "Construction & Energy", "url": "https://www.pinsentmasons.com"},
            {"name": "Clyde & Co", "desc": "Insurance & Shipping", "url": "https://www.clydeco.com"},
            {"name": "Bird & Bird", "desc": "IP & Tech focus", "url": "https://www.twobirds.com"},
            {"name": "Addleshaw Goddard", "desc": "Corporate Commercial", "url": "https://www.addleshawgoddard.com"},
            {"name": "Taylor Wessing", "desc": "Tech & Life Sci", "url": "https://www.taylorwessing.com"},
            {"name": "Gowling WLG", "desc": "IP & Real Estate", "url": "https://gowlingwlg.com"},
            {"name": "Hogan Lovells UK", "desc": "Transatlantic", "url": "https://www.hoganlovells.com"},
            {"name": "Norton Rose Fulbright", "desc": "Global Practice", "url": "https://www.nortonrosefulbright.com"},
        ],
        "🎓 Barristers Chambers (大律师公会)": [
            {"name": "Essex Court", "desc": "Commercial Arbitration", "url": "https://essexcourt.com"},
            {"name": "Blackstone", "desc": "Public Law & Comm", "url": "https://www.blackstonechambers.com"},
            {"name": "Brick Court", "desc": "Competition & EU", "url": "https://www.brickcourt.co.uk"},
            {"name": "Fountain Court", "desc": "Banking & Fraud", "url": "https://www.fountaincourt.co.uk"},
            {"name": "One Essex Court", "desc": "Commercial Lit", "url": "https://www.oeclaw.co.uk"},
        ],
        "💡 Tech & Official (科技/官方)": [
            {"name": "legislation.gov.uk", "desc": "Official Laws", "url": "https://www.legislation.gov.uk"},
            {"name": "BAILII", "desc": "Case Law Database", "url": "https://www.bailii.org"},
            {"name": "Luminance", "desc": "AI Document Review", "url": "https://www.luminance.com"},
            {"name": "Juro", "desc": "Contract Platform", "url": "https://juro.com"},
            {"name": "Companies House", "desc": "Company Registry", "url": "https://www.gov.uk/government/organisations/companies-house"},
            {"name": "The Law Society", "desc": "Solicitors Body", "url": "https://www.lawsociety.org.uk"},
            {"name": "SRA", "desc": "Regulation Authority", "url": "https://www.sra.org.uk"},
            {"name": "Practical Law", "desc": "Thomson Reuters", "url": "https://uk.practicallaw.thomsonreuters.com"},
            {"name": "vLex Justis", "desc": "Legal Research", "url": "https://vlex.com"},
        ]
    },
    "🇭🇰 HK (Hong Kong)": {
        "⚖️ Leading Local Firms (本地大所)": [
            {"name": "Deacons (的近)", "desc": "Largest Independent HK Firm", "url": "https://www.deacons.com"},
            {"name": "Woo Kwan Lee & Lo", "desc": "Conveyancing & Corporate", "url": "https://www.wkll.com"},
            {"name": "Gall", "desc": "Dispute Resolution Specialist", "url": "https://www.gallhk.com"},
            {"name": "Tanner De Witt", "desc": "Insolvency & Restructuring", "url": "https://www.tannerdewitt.com"},
            {"name": "Wilkinson & Grist", "desc": "IP & Conveyancing", "url": "https://www.wilgrist.com"},
            {"name": "P.C. Woo & Co", "desc": "Established 1945", "url": "https://www.pcwoo.com"},
            {"name": "Oldham, Li & Nie", "desc": "Matrimonial & Corp", "url": "https://oln-law.com"},
            {"name": "Haldanes", "desc": "Criminal Defense", "url": "https://www.haldanes.com"},
            {"name": "Robertsons", "desc": "Commercial Law", "url": "https://www.robertsons-hk.com"},
            {"name": "Charltons", "desc": "Boutique Corporate", "url": "https://www.charltonslaw.com"},
            {"name": "Howse Williams", "desc": "Independent Firm", "url": "https://www.howsewilliams.com"},
        ],
        "🌏 International Heavyweights (国际大所)": [
            {"name": "Mayer Brown", "desc": "Massive HK Presence", "url": "https://www.mayerbrown.com"},
            {"name": "Clifford Chance HK", "desc": "Magic Circle", "url": "https://www.cliffordchance.com"},
            {"name": "Linklaters HK", "desc": "Capital Markets", "url": "https://www.linklaters.com"},
            {"name": "Allen & Overy HK", "desc": "Finance", "url": "https://www.allenovery.com"},
            {"name": "Kirkland & Ellis HK", "desc": "PE & Restructuring", "url": "https://www.kirkland.com"},
            {"name": "Skadden HK", "desc": "IPO & M&A", "url": "https://www.skadden.com"},
            {"name": "Davis Polk HK", "desc": "US Law in HK", "url": "https://www.davispolk.com"},
            {"name": "King & Wood HK", "desc": "KWM Hong Kong", "url": "https://www.kwm.com"},
            {"name": "Reed Smith", "desc": "Litigation & Shipping", "url": "https://www.reedsmith.com"},
            {"name": "Eversheds HK", "desc": "Full service", "url": "https://www.eversheds-sutherland.com"},
        ],
        "🏛️ Official & Arbitration (官方/仲裁)": [
            {"name": "HK Judiciary", "desc": "Courts System", "url": "https://www.judiciary.hk"},
            {"name": "HKLII", "desc": "Free Legal Info", "url": "https://www.hklii.org"},
            {"name": "Companies Registry", "desc": "ICRIS Search", "url": "https://www.cr.gov.hk"},
            {"name": "HKIAC", "desc": "Intl Arbitration Centre", "url": "https://www.hkiac.org"},
            {"name": "DoJ", "desc": "Dept of Justice", "url": "https://www.doj.gov.hk"},
            {"name": "Law Society of HK", "desc": "Solicitors Body", "url": "https://www.hklawsoc.org.hk"},
            {"name": "HK Bar Assoc", "desc": "Barristers Body", "url": "https://www.hkba.org"},
            {"name": "IPD", "desc": "Intellectual Property", "url": "https://www.ipd.gov.hk"},
            {"name": "SFC", "desc": "Securities Commission", "url": "https://www.sfc.hk"},
            {"name": "e-Bram", "desc": "Online Dispute Resolution", "url": "https://www.ebram.org"},
            {"name": "Zegal", "desc": "Legal SaaS", "url": "https://zegal.com"},
        ]
    },
    "🇯🇵 JP (Japan)": {
        "🌸 Big Four Firms (四大律所)": [
            {"name": "Nishimura & Asahi", "desc": "Largest in Japan", "url": "https://www.nishimura.com"},
            {"name": "Nagashima Ohno (NO&T)", "desc": "Corporate Elite", "url": "https://www.noandt.com"},
            {"name": "Mori Hamada (MHM)", "desc": "M&A and Finance", "url": "https://www.mhmjapan.com"},
            {"name": "Anderson Mori (AMT)", "desc": "International focus", "url": "https://www.amt-law.com"},
        ],
        "⚖️ Major & Intl Firms (大型/外资)": [
            {"name": "TMI Associates", "desc": "IP & Corporate mix", "url": "https://www.tmi.gr.jp"},
            {"name": "City-Yuwa", "desc": "Finance & Real Estate", "url": "https://www.city-yuwa.com"},
            {"name": "Atsumi & Sakai", "desc": "Fintech & Innovation", "url": "https://www.aplaw.jp"},
            {"name": "Oh-Ebashi", "desc": "Top in Osaka/Kansai", "url": "https://www.ohebashi.com"},
            {"name": "Ushijima & Partners", "desc": "Litigation & Crisis", "url": "https://www.ushijima-law.gr.jp"},
            {"name": "Baker McKenzie Tokyo", "desc": "Gaiben (Foreign Law)", "url": "https://www.bakermckenzie.co.jp"},
            {"name": "Morrison Foerster", "desc": "MoFo Tokyo (Tech)", "url": "https://www.mofo.com"},
            {"name": "Skadden Tokyo", "desc": "M&A", "url": "https://www.skadden.com"},
            {"name": "White & Case Tokyo", "desc": "Projects", "url": "https://www.whitecase.com"},
            {"name": "Jones Day Tokyo", "desc": "IP Litigation", "url": "https://www.jonesday.com"},
            {"name": "Hogan Lovells Tokyo", "desc": "Cross-border", "url": "https://www.hoganlovells.com"},
        ],
        "🤖 Tech, Gov & IP (科技/官方)": [
            {"name": "Bengo4.com", "desc": "Lawyer Portal", "url": "https://www.bengo4.com"},
            {"name": "LegalOn Cloud", "desc": "AI Contract Review", "url": "https://www.legalon-cloud.com"},
            {"name": "CloudSign", "desc": "E-Signature", "url": "https://www.cloudsign.jp"},
            {"name": "Holmes (Hubble)", "desc": "CLM", "url": "https://hubble-docs.com"},
            {"name": "MNTSQ", "desc": "Contract Database", "url": "https://www.mntsq.co.jp"},
            {"name": "GVA Tech", "desc": "AI Support", "url": "https://gvatech.co.jp"},
            {"name": "e-Gov Japan", "desc": "Laws Database", "url": "https://www.e-gov.go.jp"},
            {"name": "Courts in Japan", "desc": "Supreme Court", "url": "https://www.courts.go.jp"},
            {"name": "J-PlatPat", "desc": "IP Database", "url": "https://www.j-platpat.inpit.go.jp"},
            {"name": "MoJ", "desc": "Ministry of Justice", "url": "https://www.moj.go.jp"},
            {"name": "JFBA", "desc": "Bar Federation", "url": "https://www.nichibenren.or.jp"},
        ]
    },
    "🇩🇪 DE (Germany)": {
        "⚖️ Top Kanzleien (顶尖律所)": [
            {"name": "Hengeler Mueller", "desc": "Top Tier Corporate", "url": "https://www.hengeler.com"},
            {"name": "Gleiss Lutz", "desc": "Full Service Elite", "url": "https://www.gleisslutz.com"},
            {"name": "Noerr", "desc": "Leading Independent", "url": "https://www.noerr.com"},
            {"name": "Luther", "desc": "Mid-market specialist", "url": "https://www.luther-lawfirm.com"},
            {"name": "Heuking", "desc": "Large partnership", "url": "https://www.heuking.de"},
            {"name": "CMS Germany", "desc": "Largest Tech Practice", "url": "https://cms.law/en/deu"},
            {"name": "Taylor Wessing", "desc": "IP & Tech Focus", "url": "https://www.taylorwessing.com"},
            {"name": "Görg", "desc": "Insolvency & Restructuring", "url": "https://www.goerg.de"},
            {"name": "Flick Gocke Schaumburg", "desc": "Tax Heavyweight", "url": "https://www.fgs.de"},
            {"name": "GSK Stockmann", "desc": "Real Estate & Finance", "url": "https://www.gsk.de"},
            {"name": "Beiten Burkhardt", "desc": "Member of Advant", "url": "https://www.advant-beiten.com"},
            {"name": "Oppenhoff", "desc": "Cologne based elite", "url": "https://www.oppenhoff.eu"},
            {"name": "Redeker Sellner", "desc": "Public Law", "url": "https://www.redeker.de"},
            {"name": "Haver & Mailänder", "desc": "Stuttgart based", "url": "https://www.haver-mailaender.de"},
            {"name": "Pöllath", "desc": "PE & Tax", "url": "https://www.poellath.de"},
        ],
        "🌍 International in DE (国际所德国分所)": [
            {"name": "Freshfields DE", "desc": "Market Leader", "url": "https://www.freshfields.com"},
            {"name": "Linklaters DE", "desc": "Corporate", "url": "https://www.linklaters.com"},
            {"name": "Hogan Lovells DE", "desc": "Regulatory", "url": "https://www.hoganlovells.com"},
            {"name": "Clifford Chance DE", "desc": "Finance", "url": "https://www.cliffordchance.com"},
            {"name": "White & Case DE", "desc": "Insolvency", "url": "https://www.whitecase.com"},
        ],
        "📚 Tech & Official (科技/官方)": [
            {"name": "Juris", "desc": "Legal Database", "url": "https://www.juris.de"},
            {"name": "Beck-Online", "desc": "Legal Research", "url": "https://beck-online.beck.de"},
            {"name": "BRYTER", "desc": "Automation Platform", "url": "https://bryter.com"},
            {"name": "Gesetze-im-internet", "desc": "Federal Laws", "url": "https://www.gesetze-im-internet.de"},
            {"name": "BVerfG", "desc": "Constitutional Court", "url": "https://www.bundesverfassungsgericht.de"},
            {"name": "DPMA", "desc": "Patent Office", "url": "https://www.dpma.de"},
            {"name": "Bundesanzeiger", "desc": "Federal Gazette", "url": "https://www.bundesanzeiger.de"},
            {"name": "BRAK", "desc": "Bar Association", "url": "https://www.brak.de"},
            {"name": "Legalos", "desc": "Legal Platform", "url": "https://www.legalos.com"},
            {"name": "Jurafuchs", "desc": "Education App", "url": "https://jurafuchs.de"},
        ]
    },
    "🇫🇷 FR (France)": {
        "⚖️ Top Cabinets (顶尖律所)": [
            {"name": "Bredin Prat", "desc": "Corporate & Litigation", "url": "https://www.bredinprat.com"},
            {"name": "Darrois Villey", "desc": "M&A Prestige", "url": "https://www.darroisvilley.com"},
            {"name": "Gide Loyrette Nouel", "desc": "International French Firm", "url": "https://www.gide.com"},
            {"name": "Fidal", "desc": "Largest Business Firm", "url": "https://www.fidal.com"},
            {"name": "August Debouzy", "desc": "Modern Full Service", "url": "https://www.august-debouzy.com"},
            {"name": "DS Avocats", "desc": "International Network", "url": "https://www.dsavocats.com"},
            {"name": "De Pardieu Brocas", "desc": "Finance & Real Estate", "url": "https://www.de-pardieu.com"},
            {"name": "Jeantet", "desc": "Historical Business Firm", "url": "https://www.jeantet.fr"},
            {"name": "Altana", "desc": "Litigation & IP", "url": "https://www.altanalaw.com"},
            {"name": "Franklin", "desc": "Cross-border focus", "url": "https://www.franklin-avocats.com"},
            {"name": "Racine", "desc": "Business Law", "url": "https://www.racine.eu"},
            {"name": "Lacourte Raquin", "desc": "M&A and Real Estate", "url": "https://www.lacourte.com"},
            {"name": "UGGC Avocats", "desc": "Private Client & Corp", "url": "https://www.uggc.com"},
        ],
        "🌍 International in Paris (外资所)": [
            {"name": "White & Case Paris", "desc": "Project Finance", "url": "https://www.whitecase.com"},
            {"name": "Clifford Chance Paris", "desc": "Banking", "url": "https://www.cliffordchance.com"},
            {"name": "Linklaters Paris", "desc": "Corporate", "url": "https://www.linklaters.com"},
            {"name": "Allen & Overy Paris", "desc": "Finance", "url": "https://www.allenovery.com"},
            {"name": "Cleary Gottlieb Paris", "desc": "Competition", "url": "https://www.clearygottlieb.com"},
        ],
        "💡 Tech & Official (科技/官方)": [
            {"name": "Légifrance", "desc": "Official Laws", "url": "https://www.legifrance.gouv.fr"},
            {"name": "Doctrine", "desc": "Legal Intelligence", "url": "https://www.doctrine.fr"},
            {"name": "Jus Mundi", "desc": "Intl Arbitration Search", "url": "https://jusmundi.com"},
            {"name": "Hyperlex", "desc": "CLM", "url": "https://hyperlex.ai"},
            {"name": "Le Droit Pour Moi", "desc": "Legal Video", "url": "https://ledroitpourmoi.fr"},
            {"name": "LegalStart", "desc": "Company Formation", "url": "https://www.legalstart.fr"},
            {"name": "Captain Contrat", "desc": "Marketplace", "url": "https://www.captaincontrat.com"},
            {"name": "Service-Public", "desc": "Admin Portal", "url": "https://www.service-public.fr"},
            {"name": "Cour de cassation", "desc": "Supreme Court", "url": "https://www.courdecassation.fr"},
            {"name": "CNIL", "desc": "Data Protection", "url": "https://www.cnil.fr"},
            {"name": "INPI", "desc": "Patents", "url": "https://www.inpi.fr"},
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
        font-size: 1.1rem;
        font-weight: 700;
        color: #374151;
        margin-top: 32px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        border-bottom: 1px solid #E5E7EB;
        padding-bottom: 8px;
    }
    .category-header span {
        background-color: #E0E7FF;
        color: #4338CA;
        padding: 4px 10px;
        border-radius: 99px;
        font-size: 0.8rem;
        margin-left: 10px;
    }

    /* 卡片网格 */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 16px;
        margin-bottom: 20px;
    }

    /* 卡片设计 */
    .card {
        background: #FFFFFF;
        border: 1px solid #F3F4F6;
        border-radius: 10px;
        padding: 16px;
        text-decoration: none;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        height: 100%;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }

    /* 悬停微交互 */
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.08);
        border-color: #E5E7EB;
    }
    
    /* Logo 容器 */
    .icon-box {
        width: 40px;
        height: 40px;
        min-width: 40px;
        background: #FFFFFF;
        border: 1px solid #F3F4F6;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        margin-right: 12px;
        padding: 4px;
    }
    
    .icon-img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    /* 图标与内容 */
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
    }
    
    .card-name {
        font-size: 0.95rem;
        font-weight: 600;
        color: #111827;
        line-height: 1.2;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    .card-desc {
        font-size: 0.8rem;
        color: #6B7280;
        line-height: 1.4;
        flex-grow: 1;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    /* 搜索结果中的标签 */
    .search-tag {
        font-size: 0.7rem;
        color: #9CA3AF;
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* 去除链接样式 */
    a, a:hover, a:visited { text-decoration: none !important; }

    /* 组件样式微调 */
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

# 语言切换逻辑
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
# 8. 渲染逻辑 (Auto Logo)
# -------------------------------------------------------------

def render_grid(tools_list, show_tag=False, category_name=""):
    """渲染工具网格 (使用 Google Favicon API)"""
    html = '<div class="grid-container">'
    
    for tool in tools_list:
        tag_html = ""
        if show_tag:
            tag_html = f'<div class="search-tag">🏷️ {category_name}</div>'
            
        # 自动生成 Logo URL
        logo_url = f"https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url={tool['url']}&size=128"
        
        card = f"""
<a href="{tool['url']}" target="_blank" class="card">
    <div class="card-header">
        <div class="icon-box">
            <img src="{logo_url}" class="icon-img" loading="lazy" alt="{tool['name']}">
        </div>
        <div class="card-name">{tool['name']}</div>
    </div>
    <div class="card-desc">{tool['desc']}</div>
    {tag_html}
</a>
        """
        html += card
    html += '</div>'
    return html

final_html = ""
total_tools = 0

# --- 逻辑 A: 搜索 ---
if search_query:
    flat_results = []
    for cat, tools in region_data.items():
        if selected_cats and cat not in selected_cats:
            continue
        for tool in tools:
            q = search_query.lower()
            if q in tool['name'].lower() or q in tool['desc'].lower():
                tool_copy = tool.copy()
                tool_copy['cat'] = cat 
                flat_results.append(tool_copy)
    
    if flat_results:
        total_tools = len(flat_results)
        html_buffer = '<div class="grid-container">'
        for item in flat_results:
            # 搜索结果渲染逻辑 (含 Tag)
            logo_url = f"https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url={item['url']}&size=128"
            card = f"""
            <a href="{item['url']}" target="_blank" class="card">
                <div class="card-header">
                    <div class="icon-box">
                        <img src="{logo_url}" class="icon-img" loading="lazy">
                    </div>
                    <div class="card-name">{item['name']}</div>
                </div>
                <div class="card-desc">{item['desc']}</div>
                <div class="search-tag">🏷️ {item['cat']}</div>
            </a>
            """
            html_buffer += card
        html_buffer += '</div>'
        final_html = html_buffer
    else:
        st.info(t["no_result"])

# --- 逻辑 B: 分类展示 (默认) ---
else:
    cats_to_show = selected_cats if selected_cats else all_categories
    for cat in cats_to_show:
        tools = region_data[cat]
        count = len(tools)
        total_tools += count
        # 渲染分类标题
        final_html += f'<div class="category-header">{cat} <span>{count}</span></div>'
        # 渲染网格
        final_html += render_grid(tools)

# -------------------------------------------------------------
# 9. 输出结果
# -------------------------------------------------------------
if total_tools > 0:
    st.caption(t["showing"].format(total_tools))
    st.markdown(final_html, unsafe_allow_html=True)

# 页脚
st.markdown(f"""
<div style="margin-top: 60px; border-top: 1px solid #E5E7EB; padding-top: 20px; text-align: center; color: #9CA3AF; font-size: 0.8rem;">
    {t["footer"]}
</div>
""", unsafe_allow_html=True)
