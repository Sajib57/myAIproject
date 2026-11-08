import streamlit as st
import json
import os

# Page Configuration
st.set_page_config(page_title="Krishi Mitra", page_icon="🌾", layout="centered")

st.title("🌾 Krishi Mitra: Agricultural Expert System")
st.write("Diagnose crop diseases and get smart farming recommendations using forward chaining logic.")

# Load Rules
@st.cache_data
def load_rules():
    if os.path.exists("rules.json"):
        with open("rules.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

knowledge_base = load_rules()

# Sidebar Info
st.sidebar.header("About Project")
st.sidebar.info("Krishi Mitra is a rule-based expert system designed for agricultural decision support.")

# Input Layout
col1, col2 = st.columns(2)

with col1:
    crop = st.selectbox("Select Crop:", ["Rice", "Wheat", "Potato"])

with col2:
    soil = st.selectbox("Select Soil Type:", ["Clay", "Loam", "Sandy"])

symptoms_input = st.text_input(
    "Enter Symptoms (comma separated):",
    placeholder="e.g., yellow leaves, stunted growth"
)

# Decision Action
if st.button("Diagnose Issue", type="primary"):
    if not symptoms_input:
        st.warning("Please enter at least one symptom.")
    else:
        user_symptoms = [s.strip().lower() for s in symptoms_input.split(",")]
        crop_key = crop.lower()
        soil_key = soil.lower()
        
        found = False
        if crop_key in knowledge_base:
            for rule in knowledge_base[crop_key]:
                symptom_match = all(s in user_symptoms for s in rule["symptoms"])
                soil_match = rule["soil_type"] == soil_key
                
                if symptom_match and soil_match:
                    st.success(f"📌 **Diagnosed Disease / Issue:** {rule['disease']}")
                    st.info(f"💡 **Recommendation:** {rule['recommendation']}")
                    found = True
                    break
        
        if not found:
            st.error("⚠️ **Unknown Condition:** No matching rule found. Please consult an agricultural expert physically.")