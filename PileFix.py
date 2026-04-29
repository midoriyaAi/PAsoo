import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Pile Foundation (Eccentric)", layout="centered")

st.title("🏗️ Pile Foundation - Eccentric Load Analysis")

st.markdown("### 🔹 Input")

# จำนวนเสา
n = st.number_input("Number of piles", min_value=2, value=2)

Q = st.number_input("Total Load Q (kN)", value=1000.0)

st.markdown("### 📍 Pile Coordinates (after eccentricity)")

# สร้าง input table
data = []
for i in range(int(n)):
    col1, col2 = st.columns(2)
    with col1:
        x = st.number_input(f"x{i+1} (cm)", key=f"x{i}")
    with col2:
        y = st.number_input(f"y{i+1} (cm)", key=f"y{i}")
    data.append([x, y])

df = pd.DataFrame(data, columns=["x", "y"])

# ---------------------
# CALCULATE
# ---------------------
if st.button("🧮 Calculate"):

    x = df["x"].values
    y = df["y"].values

    # 1) Centroid
    X = np.mean(x)
    Y = np.mean(y)

    # 2) Moment
    Mx = Q * Y
    My = Q * X

    # 3) New coordinates
    x_new = x - X
    y_new = y - Y

    # 4) Summations
    sum_x2 = np.sum(x_new**2)
    sum_y2 = np.sum(y_new**2)
    sum_xy = np.sum(x_new * y_new)

    denom = (sum_x2 * sum_y2 - sum_xy**2)

    # กันหาร 0
    if denom == 0:
        st.error("❌ Geometry invalid (denominator = 0)")
    else:
        m = (My * sum_y2 - Mx * sum_xy) / denom
        n_coef = (Mx * sum_x2 - My * sum_xy) / denom

        # 5) Force each pile
        P = Q / n + m * x_new + n_coef * y_new

        # ---------------------
        # OUTPUT
        # ---------------------
        st.success("✅ Calculation Complete")

        st.markdown("### 📊 Results")

        st.write(f"Centroid: X = {X:.2f} cm , Y = {Y:.2f} cm")
        st.write(f"Mx = {Mx:.2f} kN-cm")
        st.write(f"My = {My:.2f} kN-cm")

        result_df = pd.DataFrame({
            "Pile": [f"P{i+1}" for i in range(int(n))],
            "Load (kN)": P
        })

        st.dataframe(result_df)

        st.markdown("### 🔍 Check")
        st.write(f"Sum of P = {np.sum(P):.2f} kN")

# Reset
if st.button("🔄 Clear"):
    st.experimental_rerun()
