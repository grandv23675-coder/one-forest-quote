import streamlit as st
import urllib.parse
import math
import datetime

# --- 1. 頁面設定 ---
st.set_page_config(
    page_title="一森家居 One Forest Design",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. 狀態管理 ---
if 'page' not in st.session_state:
    st.session_state.page = 'reno'

def set_page(page_name):
    st.session_state.page = page_name

# --- 3. CSS 視覺核心 (白霧背景 + 強力按鈕) ---
# 背景圖：選用一張光猛、有空間感的室內設計圖
BG_URL = "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?q=80&w=2000&auto=format&fit=crop"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+HK:wght@400;500;700;900&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Noto Sans HK', sans-serif;
    }}

    /* 1. 隱藏 Streamlit 頂部 */
    header[data-testid="stHeader"] {{ display: none !important; }}
    
    /* 2. 背景：圖片 + 92% 白色霧面遮罩 (關鍵技術) 
       這令背景有質感，但又像一張白紙一樣清楚 */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.92)), url("{BG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* 3. 輸入框強制樣式 (白底黑字，確保清晰) */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #cbd5e1 !important;
        font-weight: bold !important;
        border-radius: 6px;
    }}
    /* 下拉選單內的文字 */
    div[data-baseweb="popover"] li {{ color: #000000 !important; }}
    .stSelectbox div[data-baseweb="select"] > div {{ color: #000000 !important; }}

    /* 4. 按鈕 (深藍底 + 純白字) - 你的品牌色 */
    div.stButton > button {{
        background-color: #1e3a8a !important; /* 一森深藍 */
        color: #ffffff !important;             /* 強制純白字 */
        -webkit-text-fill-color: #ffffff !important;
        border: none !important;
        padding: 15px 20px;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(30, 58, 138, 0.3); /* 藍色陰影 */
        width: 100%;
        margin-top: 10px;
    }}
    div.stButton > button:hover {{
        background-color: #172554 !important; /* Hover 變更深 */
        box-shadow: 0 6px 15px rgba(30, 58, 138, 0.4);
        transform: translateY(-2px);
    }}
    div.stButton > button p {{ color: #ffffff !important; }}

    /* 5. 標題顏色 */
    h1, h2, h3 {{ color: #1e3a8a !important; font-weight: 900 !important; }}
    h4, h5 {{ color: #334155 !important; font-weight: bold !important; }}
    p, label, li, .stMarkdown {{ color: #333333 !important; font-size: 15px !important; }}
    
    /* 6. 卡片樣式 (讓內容浮起) */
    .forest-card {{
        background: rgba(255, 255, 255, 0.95); /* 輕微透白 */
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-top: 5px solid #1e3a8a;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }}
    
    /* 7. 右側資訊欄樣式 */
    .info-box {{
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }}
    .info-header {{
        color: #b45309;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 10px;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 5px;
    }}
    
    /* 8. 價錢大字 */
    .price-box {{
        background: #1e3a8a;
        color: #fbbf24 !important;
        padding: 25px;
        text-align: center;
        border-radius: 8px;
        margin-top: 20px;
        border: 2px solid #fbbf24;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }}
    .price-val {{
        font-size: 42px;
        font-weight: 900;
        color: #fbbf24 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. 頂部 Header ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
        <div style="padding: 10px 0;">
            <h1 style="margin:0; font-size: 32px; color:#1e3a8a;">一森家居 ONE FOREST</h1>
            <p style="margin:0; color:#64748b; font-weight:bold; letter-spacing:1px;">PROFESSIONAL INTERIOR DESIGN & ENGINEERING</p>
        </div>
    """, unsafe_allow_html=True)
with col_h2:
    st.markdown("""
        <div style="text-align:right; font-size:14px; color:#334155; padding-top:15px; border-left:3px solid #1e3a8a; padding-left:15px;">
            <b>📞 4488 3183</b><br>
            📍 火炭富騰工業大廈<br>
            🌐 ctspacehk.com
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 5. 導航欄 (高對比按鈕) ---
nav1, nav2, nav3 = st.columns(3)
with nav1:
    if st.button("🏠 全屋裝修報價", key="nav_reno", type="primary" if st.session_state.page=='reno' else "secondary", use_container_width=True):
        set_page('reno')
        st.rerun()
with nav2:
    if st.button("🔨 專業清拆還原", key="nav_demo", type="primary" if st.session_state.page=='demo' else "secondary", use_container_width=True):
        set_page('demo')
        st.rerun()
with nav3:
    if st.button("✨ 清潔及除甲醛", key="nav_clean", type="primary" if st.session_state.page=='clean' else "secondary", use_container_width=True):
        set_page('clean')
        st.rerun()

st.write("") 

# --- 6. 核心佈局 (左欄：計算 / 右欄：公司資訊) ---
left_col, right_col = st.columns([2, 1]) 

# ==========================================
# 左欄：報價計算機
# ==========================================
with left_col:
    # === 客戶資料 ===
    st.markdown('<div class="forest-card">', unsafe_allow_html=True)
    st.markdown("### 📋 建立工程檔案")
    c1, c2, c3 = st.columns(3)
    with c1: client_name = st.text_input("聯絡人稱呼", placeholder="陳先生")
    with c2: client_area = st.text_input("地區/屋苑", placeholder="例如：沙田第一城")
    with c3: client_phone = st.text_input("聯絡電話", placeholder="用於接收報價單")
    st.markdown('</div>', unsafe_allow_html=True)

    # === 功能頁面內容 ===
    if st.session_state.page == 'reno':
        st.markdown('<div class="forest-card">', unsafe_allow_html=True)
        st.markdown("### 🏠 裝修規格設定")
        st.info("💡 系統依據本月市價及過往案例數據，即時生成初步預算。")
        
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            area = st.number_input("實用面積 (平方呎)", 100, 5000, 450, step=10)
            p_type = st.selectbox("物業類型", ["私人屋苑", "公屋/居屋", "村屋 (需搬運)"])
        with col_r2:
            style = st.multiselect("心儀風格", ["現代簡約", "輕奢華", "日式無印", "北歐風", "工業風"])

        st.markdown("---")
        st.markdown("#### 🔸 重點工程")
        
        wc1, wc2 = st.columns(2)
        with wc1:
            st.markdown("**泥水及結構**")
            do_demo = st.checkbox("全屋清拆及泥頭處理", value=True)
            do_masonry = st.checkbox("泥水工程 (地台/廚廁)", value=True)
            if do_masonry:
                mat_floor = st.radio("地台飾面", ["高溫磚", "木紋磚 / SPC"], horizontal=True)
            do_paint = st.checkbox("油漆工程 (剷底批灰)", value=True)
        with wc2:
            st.markdown("**水電及設備**")
            do_plumb = st.checkbox("水喉 (全屋更換銅喉)", value=True)
            do_elec = st.checkbox("電力 (新造電箱及電位)", value=True)
            e_cnt = 40
            if do_elec:
                e_cnt = st.slider("預計電位數量", 20, 100, 40)
            do_win = st.checkbox("更換鋁窗 (50料)", value=False)
            w_cnt = 0
            if do_win:
                w_cnt = st.number_input("窗戶數量", 1, 30, 6)

        st.markdown("---")
        st.markdown("#### 🔸 訂造傢俬 (E0 生態板)")
        do_furn = st.checkbox("需要一森訂造傢俬", value=True)
        furn_cost = 0
        if do_furn:
            fc1, fc2 = st.columns(2)
            with fc1:
                f_ward = st.number_input("衣櫃 / 高櫃 (直呎)", 0, 50, 8)
                f_kit = st.number_input("廚櫃組合 (直呎)", 0, 40, 8)
            with fc2:
                f_tv = st.number_input("電視地櫃 (直呎)", 0, 30, 6)
                f_bed = st.number_input("地台 / 油壓床 (平方呎)", 0, 500, 0)
            
            factor = 1.2 if "村屋" in p_type else (0.9 if "公屋" in p_type else 1.0)
            furn_cost = (f_ward*1450 + f_kit*1950 + f_tv*900 + f_bed*350) * factor

        # 計算
        factor = 1.2 if "村屋" in p_type else (0.9 if "公屋" in p_type else 1.0)
        base = 3500 + area * 8
        if do_demo: base += area * 45
        if do_masonry: base += area * 115
        if do_paint: base += area * 58
        if do_plumb: base += 23000
        if do_elec: base += 15000 + e_cnt * 780
        if do_win: base += 3500 + w_cnt * 3800
        total = (base + furn_cost) * factor
        
        # WhatsApp 內容
        wa_msg = f"你好 One Forest，我剛在網站填寫了資料。\n\n📋 *裝修報價單*\n------------------\n👤 客戶：{client_name} ({client_phone})\n📍 地區：{client_area}\n🏠 面積：{area}呎 ({p_type})\n🎨 風格：{', '.join(style)}\n------------------\n💰 *系統初估：HK${total:,.0f}*\n\n請聯絡我跟進詳細報價，謝謝。"

    elif st.session_state.page == 'demo':
        st.markdown('<div class="forest-card">', unsafe_allow_html=True)
        st.markdown("### 🔨 清拆規格")
        
        d1, d2 = st.columns(2)
        with d1:
            d_area = st.number_input("清拆面積 (實用呎)", 100, 5000, 450, step=10)
            d_type = st.radio("大廈設施", ["有電梯直達", "需行樓梯"], horizontal=True)
        with d2:
            d_floor = st.selectbox("原有地台", ["普通磚 / 木地板", "雲石 / 麻石 (附加費)"])

        st.markdown("---")
        st.markdown("#### 🔸 清拆範圍")
        chk1, chk2 = st.columns(2)
        with chk1:
            rm_floor = st.checkbox("起全屋地台及腳線", value=True)
            rm_wall = st.checkbox("打拆廚廁牆身磁磚", value=True)
            rm_part = st.checkbox("拆除間隔牆 (非主力牆)", value=False)
        with chk2:
            rm_k_t = st.checkbox("拆除廚廁櫃及潔具", value=True)
            rm_door = st.checkbox("拆除房門及門框", value=True)
            rm_furn = st.checkbox("拆除全屋傢俬/木器", value=False)

        # 計算
        d_base = 3500
        d_sqft = 0
        if rm_floor: d_sqft += 20 if "雲石" not in d_floor else 38
        d_fix = 0
        if rm_wall: d_fix += 5500
        if rm_part: d_fix += 3500
        if rm_k_t: d_fix += 3000
        if rm_door: d_fix += 1500
        if rm_furn: d_fix += 3500
        d_total = d_base + (d_area * d_sqft) + d_fix
        if d_type == "需行樓梯": d_total *= 1.35
        total = d_total
        
        # WhatsApp 內容
        wa_msg = f"你好 One Forest，我剛在網站填寫了資料。\n\n🔨 *清拆報價單*\n------------------\n👤 客戶：{client_name} ({client_phone})\n📍 地區：{client_area}\n🏠 面積：{d_area}呎\n🏗️ 設施：{d_type}\n------------------\n💰 *系統初估：HK${total:,.0f}*\n\n請聯絡我跟進，謝謝。"

    elif st.session_state.page == 'clean':
        st.markdown('<div class="forest-card">', unsafe_allow_html=True)
        st.markdown("### ✨ 清潔規格")
        
        c1, c2 = st.columns(2)
        with c1:
            c_area = st.number_input("實用面積 (呎)", 100, 5000, 550, step=10)
            c_dist = st.selectbox("地區", ["九龍區", "新界區", "香港島 (+$150)"])
        with c2:
            c_pkg = st.radio("服務套餐", ["基礎深層清潔", "清潔 + 除甲醛雙效 (推薦)"])

        st.markdown("---")
        st.markdown("#### 🔸 附加項目")
        ce1, ce2 = st.columns(2)
        with ce1:
            is_vill = st.checkbox("村屋 / 偏遠地區 (+$200)")
            has_str = st.checkbox("需行樓梯搬運")
            str_cnt = st.number_input("樓梯層數", 1, 10, 1) if has_str else 0
        with ce2:
            do_ac = st.checkbox("冷氣機高溫蒸洗 (+$500/部)")
            ac_cnt = st.number_input("冷氣數量", 0, 10, 0) if do_ac else 0
            do_mold = st.checkbox("全屋防霉/去霉菌 (+$600)")

        # 計算
        cl_base = 3280 if "雙效" in c_pkg else 1980
        rate = 6.5 if "雙效" in c_pkg else 4.2
        if c_area > 400: cl_base += (c_area - 400) * rate
        cl_base = math.ceil(cl_base/10)*10
        extra = 0
        if "香港島" in c_dist: extra += 150
        if is_vill: extra += 200
        if has_str: extra += str_cnt * 150
        if do_ac: extra += ac_cnt * 500
        if do_mold: extra += 600
        total = cl_base + extra
        
        # WhatsApp 內容
        wa_msg = f"你好 One Forest，我剛在網站填寫了資料。\n\n✨ *清潔報價單*\n------------------\n👤 客戶：{client_name} ({client_phone})\n📍 地區：{client_area}\n🏠 面積：{c_area}呎\n📦 套餐：{c_pkg}\n------------------\n💰 *系統初估：HK${total:,.0f}*\n\n請聯絡我跟進，謝謝。"
        
    st.markdown('</div>', unsafe_allow_html=True)

    # === 結果及強力按鈕區 (更新了文字) ===
    st.markdown(f"""
        <div class="price-box">
            <div style="color:white; font-size:16px; font-weight:bold; letter-spacing:1px;">ESTIMATED TOTAL 初步預算</div>
            <div class="price-val">HK${total:,.0f}</div>
            <div style="margin-top:10px; color:#fbbf24; font-size:13px;">* 價錢僅供參考，最終以師傅現場視察為準</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    # 這裡就是你要的按鈕修改：著眼於「傳送資料」
    if st.button("📤 傳送單位資料給一森 (WhatsApp)", use_container_width=True):
         import webbrowser
         webbrowser.open(f"https://wa.me/85244883183?text={urllib.parse.quote(wa_msg)}")

# ==========================================
# 右欄：公司專業資訊 (取代假圖/對話)
# ==========================================
with right_col:
    
    # 1. 服務流程 (Workflow)
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown('<div class="info-header">📅 服務流程 (Workflow)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:13px; color:#333;">
        <b>1. 初步諮詢</b><br>
        <span style="color:#666">了解客戶需求，提供初步報價。</span><br><br>
        <b>2. 上門度尺</b><br>
        <span style="color:#666">師傅現場視察，確認實際尺寸。</span><br><br>
        <b>3. 正式報價</b><br>
        <span style="color:#666">列明細項及用料，簽署合約。</span><br><br>
        <b>4. 完工驗收</b><br>
        <span style="color:#666">客戶驗收滿意後，才支付尾數。</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. 用料標準 (Material Spec)
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown('<div class="info-header">🏆 用料標準 (Standard)</div>', unsafe_allow_html=True)
    st.markdown("""
    <ul class="info-list">
        <li><b>油漆</b>：立邦 Nippon Paint 五合一</li>
        <li><b>水喉</b>：澳洲/英國標準紅銅喉</li>
        <li><b>電力</b>：施耐德 Schneider 電掣/電箱</li>
        <li><b>木器</b>：E0 級低甲醛生態板</li>
        <li><b>泥水</b>：英泥沙底，高溫磚標準</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. 服務保證 (Warranty)
    st.markdown('<div class="info-box" style="background:#f0fdf4; border-color:#bbf7d0;">', unsafe_allow_html=True)
    st.markdown('<div class="info-header" style="color:#15803d; border-color:#bbf7d0;">✅ 一森承諾</div>', unsafe_allow_html=True)
    st.markdown("""
    <ul class="info-list">
        <li><b>明碼實價</b>：絕無隱藏收費</li>
        <li><b>結構保養</b>：12 個月免費執漏</li>
        <li><b>準時起貨</b>：延誤設有賠償機制</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. 度尺 CTA
    st.markdown("""
    <div style="background:#1e3a8a; padding:15px; border-radius:8px; text-align:center; color:white;">
        <div style="font-weight:bold; font-size:15px; margin-bottom:5px;">📏 免費上門度尺</div>
        <div style="font-size:12px; opacity:0.8; margin-bottom:10px;">工程部專人跟進，即場解答疑難。</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📅 按此預約", key="side_book", use_container_width=True):
         wa_fast = f"你好，我是{client_name}，想預約師傅上門度尺。"
         import webbrowser
         webbrowser.open(f"https://wa.me/85244883183?text={urllib.parse.quote(wa_fast)}")

# --- Footer ---
st.markdown("""
    <div style="text-align: center; color: #94a3b8; font-size: 12px; margin-top: 50px;">
        © 2025 One Forest Design. All Rights Reserved.
    </div>
""", unsafe_allow_html=True)