import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import time

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="AgriLoop Ecosystem", layout="wide")

st.title("🚀 AgriLoop: Mô Hình Kết Nối & Vận Hành Hệ Thống")

# Sidebar để điều hướng
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2554/2554030.png", width=100)
app_mode = st.sidebar.radio("Chọn góc nhìn hệ thống:", 
    ["1. Luồng vận hành (Workflow)", "2. Khớp lệnh Cung - Cầu", "3. Bản đồ Tối ưu Vận chuyển"])

# 2. TÍNH NĂNG 1: LUỒNG VẬN HÀNH (WORKFLOW)
if app_mode == "1. Luồng vận hành (Workflow)":
    st.subheader("🧠 'Bộ não' AgriLoop kết nối các bên như thế nào?")
    
    # Vẽ sơ đồ bằng Graphviz
    st.graphviz_chart('''
        digraph {
            rankdir=LR;
            node [shape=box, style=filled, color="#E1F5FE", fontname="Arial"];
            
            subgraph cluster_0 {
                label = "ĐẦU VÀO (INPUT)";
                style=dashed;
                color=green;
                F [label="Nông dân\n(Đăng đơn hàng)", fillcolor="#C8E6C9"];
            }

            subgraph cluster_1 {
                label = "TRUNG TÂM XỬ LÝ (AGRILOOP ENGINE)";
                color=blue;
                M [label="Matching Algorithm\n(Khớp Cung-Cầu)", fillcolor="#BBDEFB"];
                P [label="Logistics Pooling\n(Ghép chuyến tối ưu)", fillcolor="#BBDEFB"];
            }

            subgraph cluster_2 {
                label = "ĐẦU RA (OUTPUT)";
                style=dashed;
                color=red;
                T [label="Tài xế\n(Nhận lộ trình GPS)", fillcolor="#FFF9C4"];
                B [label="Nhà máy\n(Nhận hàng & Thanh toán)", fillcolor="#FFCCBC"];
            }

            F -> M [label="Gửi dữ liệu GPS"];
            M -> P [label="Tạo chuyến hàng"];
            P -> T [label="Điều xe"];
            T -> B [label="Giao hàng"];
            B -> F [label="Số hóa hóa đơn", style=dotted];
        }
    ''')
    
    st.info("""
    **Giải thích cho Ban giám khảo:**
    - **Step 1:** Nông dân cung cấp dữ liệu thô (vị trí, khối lượng).
    - **Step 2:** AgriLoop xử lý 'khớp lệnh' để tìm nhà máy phù hợp nhất.
    - **Step 3:** Thuật toán 'ghép chuyến' gom các nông dân gần nhau để tối ưu chi phí vận chuyển.
    - **Step 4:** Tài xế chạy theo lộ trình đã tối ưu, đảm bảo không có xe chạy rỗng.
    """)

# 3. TÍNH NĂNG 2: KHỚP LỆNH (Dùng lại logic cũ nhưng làm đẹp hơn)
elif app_mode == "2. Khớp lệnh Cung - Cầu":
    st.subheader("🤝 Kết nối thời gian thực")
    col1, col2 = st.columns(2)
    # Giả lập data nông dân
    farmers = pd.DataFrame({
        'Nông dân': ['Hân', 'An', 'Bình', 'Chi'],
        'Phế phẩm': ['Vỏ trấu', 'Rơm rạ', 'Vỏ trấu', 'Bã mía'],
        'Khối lượng': [5, 10, 3, 15]
    })
    col1.write("**Nguồn cung (Farmers)**")
    col1.table(farmers)
    
    col2.write("**Nhu cầu (Factories)**")
    col2.table(pd.DataFrame({'Nhà máy': ['Bio-Fuel X'], 'Cần mua': ['Vỏ trấu'], 'Số lượng': [20]}))
    
    if st.button("Kích hoạt Matching"):
        st.success("Hệ thống đã khớp: Hân + Bình -> Cung cấp cho Bio-Fuel X (Tổng 8 tấn)")

# 4. TÍNH NĂNG 3: BẢN ĐỒ
elif app_mode == "3. Bản đồ Tối ưu Vận chuyển":
    st.subheader("📍 Mô phỏng lộ trình xe chạy (GPS Optimization)")
    # Code vẽ bản đồ ArcLayer như cũ của tớ
    view_state = pdk.ViewState(latitude=10.76, longitude=106.66, zoom=12, pitch=45)
    df = pd.DataFrame({'lon': [106.67, 106.65, 106.64], 'lat': [10.77, 10.75, 10.74]})
    layer = pdk.Layer("ArcLayer", df, get_source_position="[lon, lat]", get_target_position="[106.66, 10.76]", get_width=5, get_source_color=[0, 255, 0])
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
