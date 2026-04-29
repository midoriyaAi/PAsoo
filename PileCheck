import streamlit as st
import numpy as np
import pandas as pd

# -----------------------
# ตั้งค่า
# -----------------------
st.set_page_config(page_title="Pile Eccentricity", layout="wide")

st.title("🏗️ โปรแกรมคำนวณแรงในเสาเข็ม (เยื้องศูนย์)")

# -----------------------
# Layout
# -----------------------
col1, col2 = st.columns([2,1])

# =======================
# INPUT
# =======================
with col1:
    st.subheader("🔹 ข้อมูลนำเข้า")

    mode = st.radio(
        "เลือกประเภท",
        ["แบบสมมาตร (2 เสา)", "แบบไม่สมมาตร (3 เสาขึ้นไป)"]
    )

    if "2 เสา" in mode:
        n = 2
        st.write("จำนวนเสาเข็ม = 2")
    else:
        n = st.number_input("จำนวนเสาเข็ม", min_value=3, value=3)

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
    calc = colA.button("🧮 คำนวณ")
    clear = colB.button("🔄 ล้างค่า")

# =======================
# RESULT
# =======================
with col2:
    st.subheader("📊 ผลลัพธ์")

    if calc:

        x = df["x"].values
        y = df["y"].values

        # -----------------------
        # CASE 1: 2 เสา (สูตรในรูป)
        # -----------------------
        if n == 2:

            # ใช้ค่าเดิม (ห้าม shift)
            x_use = x
            y_use = y

            X = np.mean(x_use)
            Y = np.mean(y_use)

            Mx = Q * Y
            My = Q * X

            sum_x2 = np.sum(x_use**2)
            sum_y2 = np.sum(y_use**2)

            P = (Q/2) + (My * x_use)/sum_x2 + (Mx * y_use)/sum_y2

        # -----------------------
        # CASE 2: ≥3 เสา
        # -----------------------
        else:

            X = np.mean(x)
            Y = np.mean(y)

            x_use = x - X
            y_use = y - Y

            Mx = Q * Y
            My = Q * X

            sum_x2 = np.sum(x_use**2)
            sum_y2 = np.sum(y_use**2)
            sum_xy = np.sum(x_use * y_use)

            denom = sum_x2 * sum_y2 - sum_xy**2

            if denom == 0:
                st.error("รูปแบบเสาเข็มไม่ถูกต้อง (หารศูนย์)")
                st.stop()

            m = (My * sum_y2 - Mx * sum_xy) / denom
            n_coef = (Mx * sum_x2 - My * sum_xy) / denom

            P = Q/n + m*x_use + n_coef*y_use

        # -----------------------
        # แสดงผล
        # -----------------------
        st.markdown("---")

        result = []
        max_ratio = 0

        for i, p in enumerate(P):
            ratio = p / Q_safe
            max_ratio = max(max_ratio, ratio)

            status = "✅ ปลอดภัย" if p <= Q_safe else "❌ เกินกำลัง"

            result.append([f"P{i+1}", p, ratio, status])

        result_df = pd.DataFrame(result, columns=[
            "เสาเข็ม", "แรง (ตัน)", "Utilization", "สถานะ"
        ])

        st.dataframe(result_df, use_container_width=True)

        st.markdown("---")

        st.write(f"Utilization สูงสุด = {max_ratio:.2f}")

        if max_ratio <= 1:
            st.success("✔️ โครงสร้างปลอดภัย")
        else:
            st.error("❌ โครงสร้างไม่ปลอดภัย")

# -----------------------
# RESET
# -----------------------
if clear:
    st.experimental_rerun()
