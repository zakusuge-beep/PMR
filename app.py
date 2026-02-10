import streamlit as st

# ตั้งค่าหน้าจอ
st.set_page_config(page_title="Major Clone Booking", layout="centered")

# --- 1. ข้อมูลพื้นฐาน ---
SEAT_ROWS = ['E', 'D', 'C', 'B', 'A'] # เรียงจากหลังไปหน้า
SEAT_COLS = 10
PRICES = {
    'Normal': 200,
    'Honeymoon': 250
}

# จำลองสถานะที่นั่ง (ในระบบจริงควรดึงจาก Database)
if 'occupied_seats' not in st.session_state:
    st.session_state.occupied_seats = ['A5', 'A6', 'C1', 'C2']
if 'selected_seats' not in st.session_state:
    st.session_state.selected_seats = []

# --- 2. ส่วนแสดงผล UI ---
st.title("🎬 Major Cineplex - Booking System")

# หน้าจอ (Screen)
st.markdown("<div style='background-color: #444; color: white; text-align: center; margin-bottom: 30px;'>--- SCREEN ---</div>", unsafe_allow_html=True)

# สร้างผังที่นั่ง
for row in SEAT_ROWS:
    cols = st.columns(SEAT_COLS)
    for i in range(SEAT_COLS):
        seat_id = f"{row}{i+1}"
        
        # กำหนดประเภทที่นั่งและสี
        is_honeymoon = row in ['A', 'B']
        seat_type = 'Honeymoon' if is_honeymoon else 'Normal'
        
        # จัดการสถานะที่นั่ง
        if seat_id in st.session_state.occupied_seats:
            cols[i].button("❌", key=seat_id, disabled=True)
        elif seat_id in st.session_state.selected_seats:
            if cols[i].button("✅", key=seat_id):
                st.session_state.selected_seats.remove(seat_id)
                st.rerun()
        else:
            # ใช้สีต่างกันตามประเภทที่นั่ง
            btn_label = "🛋️" if is_honeymoon else "💺"
            if cols[i].button(btn_label, key=seat_id, help=f"{seat_type} - {PRICES[seat_type]} THB"):
                st.session_state.selected_seats.append(seat_id)
                st.rerun()

# --- 3. สรุปรายการคำสั่งซื้อ ---
st.divider()
st.subheader("สรุปรายการที่เลือก")

if st.session_state.selected_seats:
    total_price = sum([PRICES['Honeymoon'] if s[0] in ['A', 'B'] else PRICES['Normal'] for s in st.session_state.selected_seats])
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**ที่นั่ง:** {', '.join(st.session_state.selected_seats)}")
    with col2:
        st.write(f"**ราคารวมทั้งสิ้น:** {total_price:,} บาท")
    
    if st.button("ยืนยันการจอง (Confirm Booking)", type="primary", use_container_width=True):
        st.success("จองที่นั่งสำเร็จ! กรุณาชำระเงินภายใน 15 นาที")
        # Logic สำหรับบันทึกลง Database
        st.session_state.occupied_seats.extend(st.session_state.selected_seats)
        st.session_state.selected_seats = []
        st.rerun()
else:
    st.info("กรุณาเลือกที่นั่งที่คุณต้องการ")
