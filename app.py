import streamlit as st

# --- 1. 設定頁面 ---
st.set_page_config(page_title="一森家居報價單", page_icon="💎", layout="centered")

# --- 2. 美化樣式 ---
st.markdown("""
    <style>
    .stApp {background-color: #f8fafc;}
    .main-header {font-size:30px; font-weight:bold; color:#1a237e; text-align:center;}
    .total-box {background:#fff; padding:20px; border-radius:10px; border:2px solid #f5b041; text-align:center;}
    .big-price {font-size:40px; font-weight:bold; color:#1a237e;}
    </style>
""", unsafe_allow_html=True)

# --- 3. 標題 ---
st.markdown('<div class="main-header">💎 一森家居 ONE FOREST</div>', unsafe_allow_html=True)

# --- 4. 輸入介面 ---
st.write("### 🏠 單位資料")
area = st.slider("實用面積 (呎)", 100, 1500, 450)
p_type = st.selectbox("單位類型", ["私人屋苑", "公屋/居屋", "村屋"])
grade = st.radio("工藝級別", ["標準實惠", "尊尚設計"], horizontal=True)

st.write("---")
st.write("### 🔨 工程選項")
col1, col2 = st.columns(2)
with col1:
    opt_demo = st.checkbox("全屋清拆", value=True)
    opt_masonry = st.checkbox("泥水地台", value=True)
    opt_plumb = st.checkbox("水喉工程", value=True)
with col2:
    opt_elec = st.checkbox("電力工程", value=True)
    opt_paint = st.checkbox("油漆工程", value=True)
    opt_furn = st.checkbox("訂造傢俬", value=True)

# --- 5. 計算邏輯 ---
total = 0
factor = 1.0
if p_type == "公屋/居屋": factor = 0.9
if p_type == "村屋": factor = 1.15
if grade == "尊尚設計": factor *= 1.3

# 簡單估算基數
base_cost = 2700 + (area * 7) # 保險保護
if opt_demo: base_cost += area * 40
if opt_masonry: base_cost += area * 110
if opt_plumb: base_cost += 25000
if opt_elec: base_cost += 13500 + (area/10 * 760)
if opt_paint: base_cost += area * 3.5 * 14
if opt_furn: base_cost += (24 * 1350) # 假設24呎櫃

total = base_cost * factor

# --- 6. 顯示結果 ---
st.write("---")
st.markdown(f"""
    <div class="total-box">
        <div>預算總額</div>
        <div class="big-price">${total:,.0f}</div>
    </div>
""", unsafe_allow_html=True)

msg = f"你好，查詢報價。面積{area}呎，預算約${total:,.0f}"
st.link_button("📲 WhatsApp 預約", f"https://wa.me/85244883183?text={msg}", use_container_width=True)