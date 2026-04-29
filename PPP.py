import streamlit as st
import pandas as pd
import numpy as np

# -------------------------
# PAGE
# -------------------------
st.set_page_config(page_title="ฐานรากเสาเข็มเยื้องศูนย์", page_icon="🏗️")

st.title("🏗️ การออกแบบฐานรากเสาเข็ม (เยื้องศูนย์)")
st.markdown("---")

# -------------------------
# TYPE SELECT
# -------------------------
type_calc = st.radio(
    "🔹 เลือกประเภทการคำนวณ",
    ["แบบสมมาตร (เสาเข็ม 2 ต้น)", "แบบไม่สมมาตร (3 ต้นขึ้นไป)"]
)

# -------------------------
# INPUT
# -------------------------
st.subheader("🔹 ข้อมูลนำเข้า")

col1, col2 = st.columns(2)

with col1:
    if "2 ต้น" in type_calc:
        n = 2
        st.write("จำนวนเสาเข็ม = 2")
    else:
        n = st.number_input("จำนวนเสาเข็ม", min_value=3, value=3)

with col2:
    Q = st.number_input("แรงกระทำรวม Q (kN)", value=1000.0)

capacity = st.number_input("กำลังรับน้ำหนักต่อเสา (kN)", value=500.0)

st.markdown("### 📍 พิกัดเสาเข็ม (cm)")

data = []
for i in range(int(n)):
    col1, col2 = st.columns(2)
    with col1:
        x = st.number_input(f"x{i+1}", key=f"x{i}")
    with col2:
        y = st.number_input(f"y{i+1}", key=f"y{i}")
    data.append([x, y])

df = pd.DataFrame(data, columns=["x", "y"])

# -------------------------
# BUTTON
# -------------------------
col3, col4 = st.columns(2)
calculate = col3.button("🧮 คำนวณ")
clear = col4.button("🔄 ล้างค่า")

# -------------------------
# CALCULATE
# -------------------------
if calculate:

    x = df["x"].values
    y = df["y"].values

    # 1) Centroid ใหม่
    X = np.mean(x)
    Y = np.mean(y)

    # 2) Moment จาก eccentricity
    Mx = Q * Y
    My = Q * X

    # 3) พิกัดใหม่
    x_new = x - X
    y_new = y - Y

    # -------------------------
    # CASE 1: สมมาตร (2 เสา)
    # -------------------------
    if n == 2:

        sum_x2 = np.sum(x_new**2)
        sum_y2 = np.sum(y_new**2)

        P = Q/2 + (Mx * y_new)/(sum_y2) + (My * x_new)/(sum_x2)

    # -------------------------
    # CASE 2: ไม่สมมาตร
    # -------------------------
    else:

        sum_x2 = np.sum(x_new**2)
        sum_y2 = np.sum(y_new**2)
        sum_xy = np.sum(x_new * y_new)

        denom = sum_x2 * sum_y2 - sum_xy**2

        if denom == 0:
            st.error("❌ รูปแบบเสาเข็มไม่ถูกต้อง")
            st.stop()

        m = (My * sum_y2 - Mx * sum_xy) / denom
        n_coef = (Mx * sum_x2 - My * sum_xy) / denom

        P = Q/n + m * x_new + n_coef * y_new

    # -------------------------
    # OUTPUT
    # -------------------------
    st.success("✅ คำนวณเสร็จ")

    st.markdown("### 📊 ผลลัพธ์")

    col5, col6 = st.columns(2)
    with col5:
        st.metric("Centroid X (cm)", f"{X:.2f}")
        st.metric("Mx (kN·cm)", f"{Mx:.2f}")

    with col6:
        st.metric("Centroid Y (cm)", f"{Y:.2f}")
        st.metric("My (kN·cm)", f"{My:.2f}")

    result_df = pd.DataFrame({
        "เสาเข็ม": [f"P{i+1}" for i in range(int(n))],
        "แรง (kN)": P,
        "สถานะ": ["✅ ปลอดภัย" if p <= capacity else "❌ เกินกำลัง" for p in P]
    })

    st.markdown("### 🔹 แรงในเสาเข็ม")
    st.dataframe(result_df, use_container_width=True)

    st.markdown("### 🔍 ตรวจสอบ")
    st.info(f"ผลรวมแรง = {np.sum(P):.2f} kN")

    # Highlight เสาอันตราย
    if any(P > capacity):
        st.error("⚠️ มีเสาเข็มที่รับแรงเกินกำลัง")
    else:
        st.success("✔️ ทุกเสาปลอดภัย")

# -------------------------
# CLEAR
# -------------------------
if clear:
    st.experimental_rerun()

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("อ้างอิง: วิธีคำนวณจากเอกสารการออกแบบเสาเข็มเยื้องศูนย์")
