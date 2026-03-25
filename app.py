import streamlit as st
import pandas as pd
import math

st.title("🌱 Mangrove Biomass Estimation System")

# -----------------------------
# WOOD DENSITY DATABASE
# -----------------------------
wood_density = {
    "Avicennia marina": 0.36,
    "Avicennia officinalis": 0.37,
    "Aegialitis rotundifolia": 0.27,
    "Acanthus ilicifolius": 0.32,
    "Bruguiera gymnorhiza": 0.28
}

species_list = list(wood_density.keys()) + ["Other"]

# -----------------------------
# INPUT SECTION
# -----------------------------
st.header("📥 Tree Input Data")

species = st.selectbox("Species", species_list)

D30 = st.number_input("D30 (cm)", value=2.0)
H = st.number_input("Total Height (cm)", value=100.0)

cw = st.number_input("Canopy Width (cm)", value=50.0)
cl = st.number_input("Canopy Length (cm)", value=50.0)
ch = st.number_input("Canopy Height (cm)", value=50.0)

# -----------------------------
# DERIVED VARIABLES
# -----------------------------
CA = ((cw * cl) / 2) ** 2 * math.pi   # your formula
canopy_depth = H - ch
CV = CA * canopy_depth

rho = wood_density.get(species, 0.35)  # default if unknown

# -----------------------------
# BIOMASS FUNCTION
# -----------------------------
def calculate_agb(species, D30, H, CA, CV, rho):

    if species == "Avicennia marina":
        return 0.633 * (D30**1.36) * (H**1.17) * (rho**0.37)

    elif species == "Avicennia officinalis":
        return 0.676 * (D30**0.19823) * (H**1.69) * (rho**2.56)

    elif species == "Aegialitis rotundifolia":
        return 4.931 * (D30**1.465) * (CV**0.11)

    elif species == "Acanthus ilicifolius":
        return 0.00033 * (H**2.34)

    elif species == "Bruguiera gymnorhiza":
        return 20.25 * ((rho * (D30**2) * H)**0.53)

    else:
        # Common equation
        return 0.0521 * (D30**0.827) * (H**0.869) * (CA**0.227)

# -----------------------------
# CALCULATE BUTTON
# -----------------------------
if st.button("🌿 Calculate AGB"):

    agb = calculate_agb(species, D30, H, CA, CV, rho)

    st.success(f"AGB per tree: {agb:.2f} gm")

    st.write("### Derived Values")
    st.write(f"Canopy Area: {CA:.2f} cm²")
    st.write(f"Canopy Volume: {CV:.2f} cm³")

# -----------------------------
# MULTIPLE TREE DATA ENTRY
# -----------------------------
st.markdown("---")
st.header("🌳 Plot Level Calculation")

n_trees = st.number_input("Number of Trees", min_value=1, value=5)

tree_data = []

for i in range(n_trees):
    st.subheader(f"Tree {i+1}")
    
    sp = st.selectbox(f"Species {i}", species_list, key=f"sp{i}")
    d = st.number_input(f"D30 {i} (cm)", key=f"d{i}")
    h = st.number_input(f"Height {i} (cm)", key=f"h{i}")
    cw_i = st.number_input(f"CW {i}", key=f"cw{i}")
    cl_i = st.number_input(f"CL {i}", key=f"cl{i}")
    ch_i = st.number_input(f"CH {i}", key=f"ch{i}")

    CA_i = ((cw_i * cl_i) / 2) ** 2 * math.pi
    depth_i = h - ch_i
    CV_i = CA_i * depth_i
    rho_i = wood_density.get(sp, 0.35)

    agb_i = calculate_agb(sp, d, h, CA_i, CV_i, rho_i)

    tree_data.append(agb_i)

# -----------------------------
# PLOT AREA INPUT
# -----------------------------
plot_radius = st.number_input("Plot Radius (m)", value=2.0)

if st.button("📊 Calculate Plot Biomass"):

    total_agb_gm = sum(tree_data)

    # convert to tons
    total_agb_ton = total_agb_gm / 1e6

    plot_area_m2 = math.pi * (plot_radius ** 2)

    biomass_t_ha = (total_agb_ton / plot_area_m2) * 10000

    st.success(f"Total AGB: {total_agb_ton:.4f} ton")
    st.success(f"Biomass Density: {biomass_t_ha:.2f} t/ha")