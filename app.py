import streamlit as st

# ตั้งค่าหน้ากระดาษ
st.set_page_config(layout="wide", page_title="Canteen Seat Booking")

# 1. จัดเตรียมข้อมูลที่นั่ง (จำลอง Database ด้วย Session State)
if 'seats' not in st.session_state:
    # สร้างโครงสร้าง: Zone -> Table -> Seat (18 โต๊ะ/โซน, 6 ที่นั่ง/โต๊ะ)
    zones = ['A', 'B', 'C', 'D']
    st.session_state.seats = {
        zone: {f"Table {t}": [False] * 6 for t in range(1, 19)} 
        for zone in zones
    }

def toggle_seat(zone, table, seat_idx):
    st.session_state.seats[zone][table][seat_idx] = not st.session_state.seats[zone][table][seat_idx]

# --- ส่วนของการแสดงผล UI ---
st.title("🍴 ระบบจองที่นั่งโรงอาหาร (Canteen Map)")

# ส่วนของโซน D (สี่เหลี่ยมผืนผ้าแนวนอน อยู่ด้านบน)
st.subheader("โซน D (ด้านเหนือ)")
zone_d_cols = st.columns(9) # แบ่ง 18 โต๊ะเป็น 2 แถว แถวละ 9
for i, table_name in enumerate(st.session_state.seats['D']):
    with zone_d_cols[i % 9]:
        st.caption(f"D-{table_name}")
        # วาดที่นั่ง 6 ที่ (บน 3 ล่าง 3)
        seats = st.session_state.seats['D'][table_name]
        
        # ที่นั่งแถวบน
        cols = st.columns(3)
        for s_idx in range(3):
            label = "🪑" if not seats[s_idx] else "❌"
            if cols[s_idx].button(label, key=f"D-{table_name}-{s_idx}"):
                toggle_seat('D', table_name, s_idx)
                st.rerun()
        
        # ตัวโต๊ะ (Visual)
        st.markdown("<div style='background-color: #8B4513; height: 10px; border-radius: 5px; margin: 2px 0;'></div>", unsafe_allow_html=True)
        
        # ที่นั่งแถวล่าง
        cols = st.columns(3)
        for s_idx in range(3, 6):
            label = "🪑" if not seats[s_idx] else "❌"
            if cols[s_idx].button(label, key=f"D-{table_name}-{s_idx}"):
                toggle_seat('D', table_name, s_idx)
                st.rerun()

st.divider()

# ส่วนของโซน A, B, C (แนวตั้ง)
col_a, col_b, col_c = st.columns(3)

def render_vertical_zone(zone_name, column_obj):
    with column_obj:
        st.subheader(f"โซน {zone_name}")
        # แสดงโต๊ะเรียงลงมาแนวตั้ง (แถวละ 2 โต๊ะ รวม 9 แถว = 18 โต๊ะ)
        for t_row in range(0, 18, 2):
            t_cols = st.columns(2)
            for t_idx in range(2):
                table_num = t_row + t_idx + 1
                table_name = f"Table {table_num}"
                with t_cols[t_idx]:
                    st.caption(f"{zone_name}-{table_num}")
                    seats = st.session_state.seats[zone_name][table_name]
                    
                    # ที่นั่งฝั่งซ้าย 3 ที่
                    s_cols = st.columns(2) # แบ่งซ้าย-ขวา
                    with s_cols[0]: # ฝั่งซ้าย
                        for s_idx in range(3):
                            label = "🪑" if not seats[s_idx] else "❌"
                            if st.button(label, key=f"{zone_name}-{table_num}-{s_idx}"):
                                toggle_seat(zone_name, table_name, s_idx)
                                st.rerun()
                    
                    with s_cols[1]: # ฝั่งขวา
                        for s_idx in range(3, 6):
                            label = "🪑" if not seats[s_idx] else "❌"
                            if st.button(label, key=f"{zone_name}-{table_num}-{s_idx}"):
                                toggle_seat(zone_name, table_name, s_idx)
                                st.rerun()
            st.write("---")

render_vertical_zone("A", col_a)
render_vertical_zone("B", col_b)
render_vertical_zone("C", col_c)

# สรุปการจองด้านข้าง
with st.sidebar:
    st.header("📊 สรุปการจอง")
    total_booked = 0
    for z in st.session_state.seats:
        for t in st.session_state.seats[z]:
            total_booked += sum(st.session_state.seats[z][t])
    
    st.metric("ที่นั่งที่ถูกจองแล้ว", f"{total_booked} ที่")
    if st.button("Clear All Bookings"):
        del st.session_state.seats
        st.rerun()
