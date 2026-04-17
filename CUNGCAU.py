import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import time

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="AgriLoop Management System", layout="wide")

st.title("🌱 AgriLoop: Hệ Thống Điều Phối & Khớp Lệnh Thông Minh")
st.sidebar.header("Bảng Điều Khiển")
app_mode = st.sidebar.selectbox("Chọn tính năng", ["Kết nối Cung - Cầu", "Tối ưu Vận chuyển (3D Map)"])

# GIẢ LẬP DỮ LIỆU CHUNG
CENTER_LAT, CENTER_LON = 10.7626, 106.6602
farmers = pd.DataFrame({
    'Farmer_ID': [f'Nông dân {i}' for i in range(1, 6)],
    'Sản phẩm': ['Vỏ cà phê', 'Vỏ trấu', 'Rơm rạ', 'Bã mía', 'Vỏ cà phê'],
    'Số lượng (Tấn)': [5, 12, 8, 15, 7],
    'lat': [10.77, 10.75, 10.78, 10.74, 10.79],
    'lon': [106.67, 106.65, 106.68, 106.64, 106.69]
})

factories = pd.DataFrame({
    'Factory_ID': ['Nhà máy Bio-Fuel A', 'Nhà máy Phân bón B'],
    'Nhu cầu mua': ['Vỏ cà phê', 'Bã mía'],
    'Số lượng cần (Tấn)': [20, 15]
})

# --- TÍNH NĂNG 1: KẾT NỐI CUNG - CẦU ---
if app_mode == "Kết nối Cung - Cầu":
    st.subheader("🤝 Thuật toán Khớp lệnh Tự động (Matching Algorithm)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Nguồn cung hiện có (Farmers):**")
        st.dataframe(farmers[['Farmer_ID', 'Sản phẩm', 'Số lượng (Tấn)']], use_container_width=True)
    with col2:
        st.write("**Nhu cầu thị trường (Factories):**")
        st.dataframe(factories, use_container_width=True)

    if st.button("CHẠY THUẬT TOÁN KẾT NỐI"):
        with st.spinner('Hệ thống đang quét các đơn hàng phù hợp...'):
            time.sleep(1.5)
            
            # Logic khớp lệnh đơn giản: Tìm sản phẩm trùng nhau
            matches = []
            for _, f in farmers.iterrows():
                for _, b in factories.iterrows():
                    if f['Sản phẩm'] == b['Nhu cầu mua']:
                        matches.append({
                            "Bên bán": f['Farmer_ID'],
                            "Bên mua": b['Factory_ID'],
                            "Sản phẩm": f['Sản phẩm'],
                            "Khối lượng": f['Số lượng (Tấn)'],
                            "Trạng thái": "✅ Đã khớp lệnh"
                        })
            
            if matches:
                st.success(f"Tìm thấy {len(matches)} kết nối phù hợp!")
                st.table(pd.DataFrame(matches))
                st.info("💡 Hệ thống đã gửi thông báo đến tài xế để chuẩn bị lấy hàng.")
            else:
                st.warning("Hiện chưa có đơn hàng nào trùng khớp.")

# --- TÍNH NĂNG 2: TỐI ƯU VẬN CHUYỂN ---
elif app_mode == "Tối ưu Vận chuyển (3D Map)":
    st.subheader("🚚 Mô phỏng Lộ trình thu gom tối ưu")
    
    # Vẽ bản đồ (Dùng lại code cũ của tớ nhưng làm gọn lại)
    view_state = pdk.ViewState(latitude=10.76, longitude=106.66, zoom=12, pitch=45)
    layer = pdk.Layer(
        "ArcLayer",
        farmers,
        get_source_position="[lon, lat]",
        get_target_position="[106.6602, 10.7626]",
        get_source_color="[0, 255, 0]",
        get_target_color="[255, 0, 0]",
        get_width=5,
    )
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
    st.write("Đường kẻ xanh biểu thị lộ trình gom hàng đang được tối ưu để tiết kiệm xăng xe.")