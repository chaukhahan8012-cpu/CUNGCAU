import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import time

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="AgriLoop Ecosystem", layout="wide")

# CSS để làm giao diện đẹp hơn
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🌱 AgriLoop: Dashboard Quản Trị Hệ Sinh Thái")

# SIDEBAR ĐIỀU HƯỚNG
st.sidebar.header("DANH MỤC")
app_mode = st.sidebar.radio("Chọn tính năng muốn trình bày:", 
    ["1. Luồng vận hành (Workflow)", "2. Khớp lệnh Cung - Cầu Pro", "3. Bản đồ Tối ưu Vận chuyển"])

# --- TAB 1: LUỒNG VẬN HÀNH ---
if app_mode == "1. Luồng vận hành (Workflow)":
    st.subheader("🧠 Sơ đồ luồng kết nối dữ liệu")
    st.graphviz_chart('''
        digraph {
            rankdir=LR;
            node [shape=box, style=filled, color="#E1F5FE", fontname="Arial"];
            F [label="Nông dân", fillcolor="#C8E6C9"];
            M [label="Matching Engine", fillcolor="#BBDEFB"];
            P [label="Pooling Logistics", fillcolor="#BBDEFB"];
            T [label="Tài xế", fillcolor="#FFF9C4"];
            B [label="Nhà máy", fillcolor="#FFCCBC"];
            F -> M -> P -> T -> B;
            B -> F [label="Thanh toán", style=dotted];
        }
    ''')
    st.info("Minh họa cách AgriLoop xử lý dữ liệu từ Nông dân đến Nhà máy.")

# --- TAB 2: KHỚP LỆNH PRO ---
elif app_mode == "2. Khớp lệnh Cung - Cầu Pro":
    st.subheader("🤖 Thuật toán Khớp lệnh & Tối ưu lợi ích")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**📦 Nguồn cung (Nông dân)**")
        farmers_df = pd.DataFrame({
            'Nông dân': ['Thúy', 'An', 'Bình', 'Chi'],
            'Sản phẩm': ['Rơm rạ', 'Rơm rạ', 'Rơm rạ', 'Rơm rạ'],
            'Khối lượng (Tấn)': [5, 10, 3, 7]
        })
        st.table(farmers_df)
    
    with col2:
        st.write("**🏭 Nhu cầu (Nhà máy)**")
        factory_df = pd.DataFrame({
            'Nhà máy': ['Bio-Fuel X'],
            'Cần mua': ['Rơm rạ'],
            'Số lượng': [20]
        })
        st.table(factory_df)

    if st.button("KÍCH HOẠT MATCHING"):
        with st.spinner('Đang tính toán phương án tối ưu...'):
            time.sleep(1)
            st.success("🎉 Đã tìm thấy phương án tối ưu: Ghép 3 đơn hàng rơm rạ!")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Tổng gom", "15 Tấn", "Rơm rạ")
            m2.metric("Chi phí vận chuyển", "-25%", "Tiết kiệm")
            m3.metric("Matching Score", "98/100", "Tối ưu")
            
            st.code("Lộ trình đề xuất: Farm Thúy -> Farm Bình -> Farm Chi -> Nhà máy Bio-Fuel X", language="text")

# --- TAB 3: BẢN ĐỒ ---
elif app_mode == "3. Bản đồ Tối ưu Vận chuyển":
    st.subheader("📍 Mô phỏng lộ trình xe chạy thời gian thực")
    view_state = pdk.ViewState(latitude=10.76, longitude=106.66, zoom=12, pitch=45)
    
    # Tạo dữ liệu đường cong ảo
    arc_data = pd.DataFrame({
        's_lon': [106.67, 106.65, 106.64],
        's_lat': [10.77, 10.75, 10.74],
        't_lon': [106.66, 106.66, 106.66],
        't_lat': [10.76, 10.76, 10.76]
    })
    
    layer = pdk.Layer(
        "ArcLayer",
        arc_data,
        get_source_position="[s_lon, s_lat]",
        get_target_position="[t_lon, t_lat]",
        get_source_color=[40, 167, 69],
        get_target_color=[220, 53, 69],
        get_width=5,
    )
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
