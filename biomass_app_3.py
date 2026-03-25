import streamlit as st
import pandas as pd
import math

# Initialize storage
if "data" not in st.session_state:
    st.session_state.data = []

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

# 📍 Location
st.subheader("📍 Location Data")
lat = st.number_input("Latitude", value=0.0, format="%.6f")
lon = st.number_input("Longitude", value=0.0, format="%.6f")

# 🗂 Plot Info
st.subheader("🗂 Plot Information")
plot_id = st.text_input("Plot ID (e.g., P1, Plot_A)")
tree_no = st.number_input("Tree Number", min_value=1, step=1)

# 🌿 Species
species = st.selectbox("Species", species_list)

if species == "Other":
    species_final = st.text_input("Enter Species Name")
    rho = st.number_input("Enter Wood Density (ρ)", value=0.35)
else:
    species_final = species
    rho = wood_density[species]

# 🌳 Tree Measurements
D30 = st.number_input("D30 (cm)", value=2.0)
H = st.number_input("Total Height (cm)", value=100.0)

cw = st.number_input("Canopy Width (cm)", value=50.0)
cl = st.number_input("Canopy Length (cm)", value=50.0)
ch = st.number_input("Canopy Height (cm)", value=50.0)

# -----------------------------
# DERIVED VARIABLES
# -----------------------------
CA = ((cw * cl) / 2) ** 2 * math.pi
canopy_depth = H - ch
CV = CA * canopy_depth

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
        return 0.0521 * (D30**0.827) * (H**0.869) * (CA**0.227)

# -----------------------------
# CALCULATE + SAVE BUTTON
# -----------------------------
if st.button("🌿 Calculate & Save AGB"):

    # Prevent empty species in "Other"
    if species == "Other" and species_final.strip() == "":
        st.warning("⚠️ Please enter species name for 'Other'")
    else:
        agb = calculate_agb(species, D30, H, CA, CV, rho)

        st.success(f"AGB per tree: {agb:.2f} gm")

        # Save record
        record = {
            "Plot ID": plot_id,
            "Tree No": tree_no,
            "Latitude": lat,
            "Longitude": lon,
            "Species": species_final,
            "D30 (cm)": D30,
            "Height (cm)": H,
            "Canopy Width": cw,
            "Canopy Length": cl,
            "Canopy Height": ch,
            "Wood Density": rho,
            "Canopy Area": CA,
            "Canopy Volume": CV,
            "AGB (gm)": agb
        }

        st.session_state.data.append(record)

        st.write("### Derived Values")
        st.write(f"Canopy Area: {CA:.2f} cm²")
        st.write(f"Canopy Volume: {CV:.2f} cm³")

# -----------------------------
# DISPLAY DATA
# -----------------------------
if st.session_state.data:

    df = pd.DataFrame(st.session_state.data)

    st.write("## 📊 Collected Data")
    st.dataframe(df)

    # 📥 Download CSV
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name='mangrove_biomass.csv',
        mime='text/csv',
    )

# -----------------------------
# CLEAR DATA BUTTON
# -----------------------------
if st.button("🗑 Clear All Data"):
    st.session_state.data = []
    st.success("All data cleared!")
