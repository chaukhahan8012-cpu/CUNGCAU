import streamlit as st
import pandas as pd
import time

def run_pro_matching():
    st.subheader("🤖 Hệ Thống Khớp Lệnh Thông Minh (Smart Matching Engine)")
    
    # Giả lập dữ liệu có thêm chỉ số "Giá" và "Khoảng cách"
    farmers_data = {
        'Nông dân': ['Hân', 'An', 'Bình', 'Chi'],
        'Sản phẩm': ['Vỏ trấu', 'Rơm rạ', 'Vỏ trấu', 'Vỏ trấu'],
        'Khối lượng (Tấn)': [5, 10, 3, 7],
        'Khoảng cách (km)': [12, 45, 8, 20],
        'Giá kỳ vọng (đ/kg)': [500, 300, 520, 480]
    }
    df_farmers = pd.DataFrame(farmers_data)

    st.write("### 📋 Nguồn cung đang chờ xử lý")
    st.dataframe(df_farmers.style.highlight_max(axis=0, subset=['Khối lượng (Tấn)'], color='#e1f5fe'))

    if st.button("🚀 KÍCH HOẠT THUẬT TOÁN TỐI ƯU"):
        with st.status("Đang quét tọa độ và tối ưu chi phí...", expanded=True) as status:
            time.sleep(1)
            st.write("🔍 Đang tìm nhà máy có nhu cầu phù hợp...")
            time.sleep(1)
            st.write("📉 Đang tính toán lộ trình gom hàng (Pooling)...")
            status.update(label="Khớp lệnh hoàn tất!", state="complete", expanded=False)

        # Kết quả khớp lệnh "Xịn"
        st.success("🎉 Đã tìm thấy phương án tối ưu nhất!")
        
        # Hiển thị dưới dạng Dashboard kết quả
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Tổng khối lượng gom", "15 Tấn", "Vỏ trấu")
        res_col2.metric("Chi phí vận chuyển", "-25%", "Tiết kiệm")
        res_col3.metric("Matching Score", "98/100", "Rất cao")

        st.write("### 🚛 Kế hoạch vận chuyển đề xuất (Pooling)")
        match_res = pd.DataFrame({
            'Lộ trình': ['Hân -> Bình -> Chi -> Nhà máy X'],
            'Xe tải điều động': ['Xe 15 tấn - Đội xe số 04'],
            'Tổng quãng đường': ['28 km (Tiết kiệm 15km so với đi lẻ)'],
            'Trạng thái': ['🔥 Đang điều xe']
        })
        st.table(match_res)

# Gọi hàm này trong app_mode của bạn
