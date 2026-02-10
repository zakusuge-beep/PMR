import streamlit as st

# ตั้งค่าหน้าจอ
st.set_page_config(layout="wide", page_title="Canteen Seat Booking - Premium")

# --- Custom CSS เพื่อปรับแต่ง UI ให้เหมือนโรงหนัง ---
st.markdown("""
<style>
    /* พื้นหลังสีดำแบบโรงหนัง */
    .stApp {
        background-color: #0f0f0f;
        color: #ffffff;
    }
    
    /* หัวข้อโซน */
    .zone-label {
        text-align: center;
        color: #ffd700;
        font-weight: bold;
        font-size: 20px;
        margin-bottom: 10px;
        border-bottom: 2px solid #333;
    }

    /* ตกแต่งปุ่มที่นั่ง */
    div.stButton > button {
        background-color: #333 !important; /* ที่นั่งว่างสีเทาเข้ม */
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 5px !important;
        width: 100% !important;
        height: 40px !important;
        transition: 0.3s;
    }
    
    /* ปุ่มที่ถูกจองแล้ว (สีแดงเมเจอร์) */
    div.stButton > button.booked {
        background-color: #e50914 !important; 
        border-color: #ff0000 !important;
    }

    div.stButton > button:hover {
        border-color: #ffd700 !important; /* Hover แล้วเป็นสีทอง */
        transform: scale(1.1);
    }

    /* ตัวโต๊ะ */
    .table-top {
        background: linear-gradient(90deg, #444, #666, #444);
        height: 60px;
        border-radius: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        color: #ccc;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- จัดการข้อมูลที่นั่ง ---
if 'seats' not in st.session_state:
    zones = ['A', 'B', 'C', 'D']
    st.session_state.seats = {
        zone: {f"T{t}": [False] * 6 for t in range(1, 19)} for zone in zones
    }

def toggle_seat(z, t, s):
    st.session_state.seats[z][t][s] = not st.session_state.seats[z][t][s]

# --- ส่วนแสดงผล ---
st.title("🎬 CANTEEN SEAT SELECTION")
st.markdown("<p style='color: #888;'>เลือกที่นั่งที่คุณต้องการจองภายในโรงอาหาร</p>", unsafe_allow_html=True)

# สัญลักษณ์บอกสถานะ
st.markdown("""
<div style='display: flex; gap: 20px; margin-bottom: 30px;'>
    <div><span style='background-color: #333; padding: 2px 10px; border-radius: 3px; border: 1px solid #444;'>🪑</span> ว่าง</div>
    <div><span style='background-color: #e50914; padding: 2px 10px; border-radius: 3px;'>❌</span> จองแล้ว</div>
</div>
""", unsafe_allow_html=True)

# ----------------- โซน D (แนวนอนด้านบน) -----------------
st.markdown("<div class='zone-label'>ZONE D (NORTH)</div>", unsafe_allow_html=True)
d_rows = [st.columns(6), st.columns(6), st.columns(6)] # 18 โต๊ะ แบ่งเป็น 3 แถว แถวละ 6

for i, t_id in enumerate(st.session_state.seats['D']):
    col_idx = i % 6
    row_idx = i // 6
    with d_rows[row_idx][col_idx]:
        seats = st.session_state.seats['D'][t_id]
        # ที่นั่งแถวบน
        c = st.columns(3)
        for s in range(3):
            is_booked = seats[s]
            label = "❌" if is_booked else " "
            if c[s].button(label, key=f"D-{t_id}-{s}"):
                toggle_seat('D', t_id, s)
                st.rerun()
        # โต๊ะ
        st.markdown(f"<div class='table-top'>D-{i+1}</div>", unsafe_allow_html=True)
        # ที่นั่งแถวล่าง
        c = st.columns(3)
        for s in range(3, 6):
            is_booked = seats[s]
            label = "❌" if is_booked else " "
            if c[s].button(label, key=f"D-{t_id}-{s}"):
                toggle_seat('D', t_id, s)
                st.rerun()

st.divider()

# ----------------- โซน A, B, C (แนวตั้ง) -----------------
col_a, col_b, col_c = st.columns(3)

def render_cine_zone(zone_name, container):
    with container:
        st.markdown(f"<div class='zone-label'>ZONE {zone_name}</div>", unsafe_allow_html=True)
        # 18 โต๊ะ เรียงลงมาแถวละ 2 โต๊ะ รวม 9 แถว
        for r in range(9):
            row_cols = st.columns(2)
            for side in range(2):
                t_idx = (r * 2) + side + 1
                t_id = f"T{t_idx}"
                with row_cols[side]:
                    seats = st.session_state.seats[zone_name][t_id]
                    st.caption(f"โต๊ะ {zone_name}-{t_idx}")
                    # แสดงผลที่นั่งแบบซ้าย-ขวา ล้อมโต๊ะแนวตั้ง
                    sc1, sc2, sc3 = st.columns([1, 2, 1]) # [ที่นั่งซ้าย, โต๊ะ, ที่นั่งขวา]
                    
                    with sc1: # ฝั่งซ้าย 3 ที่
                        for s in range(3):
                            label = "❌" if seats[s] else " "
                            if st.button(label, key=f"{zone_name}-{t_id}-{s}"):
                                toggle_seat(zone_name, t_id, s)
                                st.rerun()
                    with sc2: # ตัวโต๊ะแนวตั้ง
                        st.markdown(f"<div class='table-top' style='height: 140px; writing-mode: vertical-rl;'>TABLE</div>", unsafe_allow_html=True)
                    with sc3: # ฝั่งขวา 3 ที่
                        for s in range(3, 6):
                            label = "❌" if seats[s] else " "
                            if st.button(label, key=f"{zone_name}-{t_id}-{s}"):
                                toggle_seat(zone_name, t_id, s)
                                st.rerun()
            st.write("")

render_cine_zone("A", col_a)
render_cine_zone("B", col_b)
render_cine_zone("C", col_c)

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='color: #ffd700;'>MY BOOKING</h2>", unsafe_allow_html=True)
    booked_count = sum(s for z in st.session_state.seats.values() for t in z.values() for s in t)
    st.metric("Total Seats Selected", booked_count)
    if st.button("CONFIRM BOOKING"):
        st.success("จองที่นั่งสำเร็จ!")
    if st.button("RESET ALL"):
        del st.session_state.seats
        st.rerun()
