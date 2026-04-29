import streamlit as st
import numpy as np
import pandas as pd

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Pile Eccentricity", layout="wide")

# -------------------------
# STYLE
# -------------------------
st.markdown("""
<style>
.main {background-color:#0f172a;}
.card {
    background:#1e293b;
    padding:20px;
    border-radius:14px;
    margin-bottom:15px;
    color:white;
}
.title {
    font-size:26px;
    font-weight:bold;
    color:#22d3ee;
}
.safe {color:#22c55e; font-weight:bold;}
.danger {color:#ef4444; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown("""
<div class="card">
<div class="title">เสาเข็มเยื้องศูนย์ – Pile Eccentricity Analysis</div>
คำนวณแรงในเสาเข็มตามสูตรมาตรฐาน (ตรงตามตัวอย่าง)
</div>
""", unsafe_allow_html=True)

# -------------------------
# LAYOUT
# -------------------------
left, right = st.columns([2,1])

# =========================
# INPUT
# =========================
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    mode = st.radio(
        "🔹 เลือกประเภท",
        ["แบบสมมาตร (2 เสา)", "แบบไม่สมมาตร (3 เสาขึ้นไป)"]
    )

    if "2 เสา" in mode:
        n = 2
    else:
        n = st.number_input("จำนวนเสา", min_value=3, value=3)

    Q = st.number_input("Q (ตัน)", value=50.0)
    Q_safe = st.number_input("Q_safe (ตัน/ต้น)", value=40.0)

    st.markdown("### 📍 พิกัดเสาเข็ม (cm)")
    data = []
    for i in range(int(n)):
        c1, c2 = st.columns(2)
        with c1:
            x = st.number_input(f"x{i+1}", key=f"x{i}")
        with c2:
            y = st.number_input(f"y{i+1}", key=f"y{i}")
        data.append([x,y])

    df = pd.DataFrame(data, columns=["x","y"])

    colA, colB = st.columns(2)
    calc = colA.button("⚡ คำนวณ")
    clear = colB.button("🔄 ล้างค่า")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# RESULT
# =========================
with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 ผลลัพธ์")

    if calc:

        x = df["x"].values
        y = df["y"].values

        # -------------------------
        # CASE 1: 2 เสา (ใช้สูตรในรูป)
        # -------------------------
        if n == 2:

            # ❗ ใช้ค่า x,y ตรง ๆ (ห้าม shift)
            x_use = x
            y_use = y

            # Moment
            # (ในตัวอย่าง centroid = 0 → ใช้ X,Y จาก input ได้เลย)
            X = np.mean(x_use)
            Y = np.mean(y_use)

            Mx = Q * Y
            My = Q * X

            sum_x2 = np.sum(x_use**2)
            sum_y2 = np.sum(y_use**2)

            P = (Q/n) + (My*x_use)/sum_x2 + (Mx*y_use)/sum_y2

            st.write(f"Centroid ≈ ({X:.2f}, {Y:.2f})")
            st.write(f"Mx = {Mx:.2f}, My = {My:.2f}")

        # -------------------------
        # CASE 2: ≥3 เสา (general)
        # -------------------------
        else:

            X = np.mean(x)
            Y = np.mean(y)

            x_use = x - X
            y_use = y - Y

            Mx = Q * Y
            My = Q * X

            sum_x2 = np.sum(x_use**2)
            sum_y2 = np.sum(y_use**2)
            sum_xy = np.sum(x_use*y_use)

            denom = sum_x2*sum_y2 - sum_xy**2
            if denom == 0:
                st.markdown('<div class="danger">❌ Geometry Error</div>', unsafe_allow_html=True)
                st.stop()

            m = (My*sum_y2 - Mx*sum_xy)/denom
            n_coef = (Mx*sum_x2 - My*sum_xy)/denom

            P = Q/n + m*x_use + n_coef*y_use

            st.write(f"Centroid = ({X:.2f}, {Y:.2f})")
            st.write(f"Mx = {Mx:.2f}, My = {My:.2f}")

        # -------------------------
        # OUTPUT
        # -------------------------
        st.markdown("---")

        max_ratio = 0
        for i, p in enumerate(P):
            ratio = p / Q_safe
            max_ratio = max(max_ratio, ratio)

            if p <= Q_safe:
                st.markdown(f'<div class="safe">P{i+1} = {p:.2f} ตัน ✔</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="danger">P{i+1} = {p:.2f} ตัน ❌</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.write(f"Utilization = {max_ratio:.2f}")

        if max_ratio <= 1:
            st.markdown('<div class="safe">✔ โครงสร้างปลอดภัย</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="danger">❌ ไม่ปลอดภัย</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# CLEAR
# -------------------------
if clear:
    st.experimental_rerun()
