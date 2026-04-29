import streamlit as st
import pandas as pd
import numpy as np

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Pile Eccentricity", layout="wide")

# -------------------------
# CUSTOM CSS (ทำ UI แบบในรูป)
# -------------------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.main {
    background-color: #0f172a;
}
.block-container {
    padding-top: 2rem;
}

.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    color: white;
}

.title {
    font-size: 28px;
    font-weight: bold;
    color: #22d3ee;
}

.subtitle {
    font-size: 16px;
    color: #94a3b8;
}

.result-box {
    background: #111827;
    padding: 20px;
    border-radius: 12px;
    color: #22c55e;
    font-size: 18px;
}

.danger {
    color: #ef4444;
    font-weight: bold;
}

.safe {
    color: #22c55e;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown("""
<div class="card">
<div class="title">เสาเข็มเยื้องศูนย์ – Pile Eccentricity Analysis</div>
<div class="subtitle">คำนวณแรงในเสาเข็มจากแรงเยื้องศูนย์ พร้อมตรวจสอบความปลอดภัย</div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# LAYOUT
# -------------------------
left, right = st.columns([2, 1])

# =========================
# LEFT SIDE (INPUT)
# =========================
with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 🔹 เลือกประเภทการคำนวณ")
    mode = st.radio(
        "",
        ["แบบสมมาตร (2 เสา)", "แบบไม่สมมาตร (3 เสาขึ้นไป)"]
    )

    if "2 เสา" in mode:
        n = 2
    else:
        n = st.number_input("จำนวนเสาเข็ม", min_value=3, value=3)

    st.markdown("### 🔹 แรงกระทำ")
    Q = st.number_input("Q (ตัน)", value=50.0)
    Q_safe = st.number_input("Q_safe (ตัน/ต้น)", value=40.0)

    st.markdown("### 🔹 พิกัดเสาเข็ม (cm)")

    data = []
    for i in range(int(n)):
        col1, col2 = st.columns(2)
        with col1:
            x = st.number_input(f"x{i+1}", key=f"x{i}")
        with col2:
            y = st.number_input(f"y{i+1}", key=f"y{i}")
        data.append([x, y])

    df = pd.DataFrame(data, columns=["x", "y"])

    colA, colB = st.columns(2)
    calc = colA.button("⚡ คำนวณ")
    clear = colB.button("🔄 ล้างค่า")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# RIGHT SIDE (RESULT)
# =========================
with right:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 ผลลัพธ์")

    if calc:

        x = df["x"].values
        y = df["y"].values

        # centroid
        X = np.mean(x)
        Y = np.mean(y)

        # moment
        Mx = Q * Y
        My = Q * X

        x_new = x - X
        y_new = y - Y

        if n == 2:
            sum_x2 = np.sum(x_new**2)
            sum_y2 = np.sum(y_new**2)

            P = Q/2 + (Mx * y_new)/sum_y2 + (My * x_new)/sum_x2

        else:
            sum_x2 = np.sum(x_new**2)
            sum_y2 = np.sum(y_new**2)
            sum_xy = np.sum(x_new*y_new)

            denom = sum_x2*sum_y2 - sum_xy**2

            if denom == 0:
                st.markdown('<div class="danger">❌ Geometry Error</div>', unsafe_allow_html=True)
                st.stop()

            m = (My*sum_y2 - Mx*sum_xy)/denom
            n_coef = (Mx*sum_x2 - My*sum_xy)/denom

            P = Q/n + m*x_new + n_coef*y_new

        # show results
        st.markdown(f"Centroid: ({X:.2f}, {Y:.2f})")
        st.markdown(f"Mx = {Mx:.2f}")
        st.markdown(f"My = {My:.2f}")

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

        st.markdown(f"Utilization = {max_ratio:.2f}")

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
