import streamlit as st
import math

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Shallow Foundation Calculator",
    page_icon="🏗️",
    layout="centered"
)

# -------------------------
# Title
# -------------------------
st.title("🏗️ Shallow Foundation Bearing Capacity")
st.markdown("### (Terzaghi Method)")

st.markdown("---")

# -------------------------
# Input Section
# -------------------------
st.subheader("🔹 Input Parameters")

col1, col2 = st.columns(2)

with col1:
    B = st.number_input("Width, B (m)", min_value=0.0, value=2.0)
    D = st.number_input("Depth, D (m)", min_value=0.0, value=1.0)
    c = st.number_input("Cohesion, c (kPa)", min_value=0.0, value=25.0)
    gamma = st.number_input("Unit weight, γ (kN/m³)", min_value=0.0, value=18.0)

with col2:
    L = st.number_input("Length, L (m)", min_value=0.0, value=2.0)
    phi = st.number_input("Friction angle, φ (deg)", min_value=0.0, value=30.0)
    FS = st.number_input("Factor of Safety (FS)", min_value=1.0, value=3.0)

st.markdown("---")

# -------------------------
# Functions
# -------------------------
def bearing_factors(phi):
    phi_rad = math.radians(phi)
    
    Nq = math.exp(math.pi * math.tan(phi_rad)) * (math.tan(math.radians(45) + phi_rad/2))**2
    
    if phi == 0:
        Nc = 5.7
        Ngamma = 0
    else:
        Nc = (Nq - 1) / math.tan(phi_rad)
        Ngamma = 2 * (Nq + 1) * math.tan(phi_rad)
    
    return Nc, Nq, Ngamma


def terzaghi_qult(c, gamma, D, B, phi):
    Nc, Nq, Ngamma = bearing_factors(phi)
    
    qult = c * Nc + gamma * D * Nq + 0.5 * gamma * B * Ngamma
    
    return qult


# -------------------------
# Buttons
# -------------------------
col3, col4 = st.columns(2)

with col3:
    calculate = st.button("🧮 Calculate")

with col4:
    clear = st.button("🔄 Clear")

# -------------------------
# Logic
# -------------------------
if calculate:
    qult = terzaghi_qult(c, gamma, D, B, phi)
    qall = qult / FS

    st.success("✅ Calculation Complete")

    st.markdown("### 📊 Results")
    st.metric("Ultimate Bearing Capacity (q_ult)", f"{qult:,.2f} kPa")
    st.metric("Allowable Bearing Capacity (q_allow)", f"{qall:,.2f} kPa")

    st.markdown("---")
    st.markdown("### 📘 Bearing Capacity Factors")
    Nc, Nq, Ngamma = bearing_factors(phi)
    st.write(f"Nc = {Nc:.2f}")
    st.write(f"Nq = {Nq:.2f}")
    st.write(f"Nγ = {Ngamma:.2f}")

# Clear (รีเฟรชหน้า)
if clear:
    st.experimental_rerun()


# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.caption("Developed for Civil Engineering | Terzaghi Bearing Capacity Theory")
