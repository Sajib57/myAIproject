import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# Page Layout & Config
st.set_page_config(page_title="Krishi Mitra Pro", page_icon="🌾", layout="wide")

st.title("🌾 Krishi Mitra: Smart Agricultural Diagnostic & Advisory Platform")
st.write("Advanced AI Decision Support System with IoT Sensors, Market Intelligence, and Query Logging.")

# Session State for Query History
if "query_log" not in st.session_state:
    st.session_state.query_log = []

# Load Rules
@st.cache_data
def load_rules():
    if os.path.exists("rules.json"):
        with open("rules.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

knowledge_base = load_rules()

# Country Regional Data
COUNTRY_FERTILITY_DATA = {
    "Bangladesh": {"predominant_soil": "Alluvial / Clay Loam", "fertility_index": "High", "common_deficiency": "Nitrogen, Zinc"},
    "India": {"predominant_soil": "Alluvial / Black / Red Soil", "fertility_index": "Moderate-High", "common_deficiency": "Nitrogen, Organic Carbon"},
    "USA": {"predominant_soil": "Mollisols / Loam", "fertility_index": "Very High", "common_deficiency": "Potassium, Phosphorus"}
}

# Sidebar: Country Insights & Query Logs
with st.sidebar:
    st.header("🌍 Regional Fertility Profile")
    selected_country = st.selectbox("Select Country / Region:", list(COUNTRY_FERTILITY_DATA.keys()))
    country_info = COUNTRY_FERTILITY_DATA[selected_country]
    
    st.write(f"**Predominant Soil:** {country_info['predominant_soil']}")
    st.write(f"**Fertility Index:** {country_info['fertility_index']}")
    st.write(f"**Common Deficiencies:** {country_info['common_deficiency']}")
    st.markdown("---")
    
    st.header("📜 Recent Query History")
    if st.session_state.query_log:
        history_df = pd.DataFrame(st.session_state.query_log)
        st.dataframe(history_df[["Timestamp", "Crop", "Diagnosis"]], use_container_width=True)
        
        # Download History Log
        csv_data = history_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Log CSV", data=csv_data, file_name="krishi_mitra_logs.csv", mime="text/csv")
    else:
        st.info("No queries logged yet.")

# Main Interface Tabs
tab1, tab2, tab3 = st.tabs(["🩺 Diagnostics & IoT Sensors", "📈 Market & Economic Forecast", "📊 Analytics Dashboard"])

with tab1:
    st.subheader("Field Inputs & Real-Time Sensors")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        crop = st.selectbox("Select Crop:", ["Rice", "Potato", "Wheat"])
        soil = st.selectbox("Select Soil Type:", ["Clay", "Loam", "Sandy"])
    
    with col2:
        st.markdown("**📡 Simulated IoT Field Sensors**")
        soil_moisture = st.slider("Soil Moisture (%)", 0, 100, 45)
        soil_ph = st.slider("Soil pH Level", 3.0, 9.0, 6.0, step=0.1)
    
    with col3:
        st.markdown("**🍃 Leaf & Field Symptoms**")
        symptoms_input = st.text_input(
            "Enter Symptoms (comma separated):",
            placeholder="e.g., yellow leaves, stunted growth"
        )
    
    if st.button("Run Diagnostic Engine", type="primary"):
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
                        found = True
                        disease = rule['disease']
                        rec = rule['recommendation']
                        
                        # Sensor checks
                        ph_min, ph_max = rule.get("ideal_ph_range", [5.0, 7.0])
                        moisture_min = rule.get("min_moisture", 30)
                        
                        st.success(f"📌 **Diagnosed Condition:** {disease}")
                        st.info(f"💡 **Recommended Action:** {rec}")
                        
                        # Sensor Feedback Warnings
                        if not (ph_min <= soil_ph <= ph_max):
                            st.warning(f"⚠️ **Sensor Warning (pH):** Current pH ({soil_ph}) is outside ideal range ({ph_min} - {ph_max}). Consider soil conditioning.")
                        if soil_moisture < moisture_min:
                            st.warning(f"⚠️ **Sensor Warning (Moisture):** Low moisture levels ({soil_moisture}%). Additional irrigation recommended.")
                        
                        # Log to session state
                        st.session_state.query_log.append({
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Crop": crop,
                            "Soil": soil,
                            "Symptoms": symptoms_input,
                            "pH": soil_ph,
                            "Moisture": soil_moisture,
                            "Diagnosis": disease
                        })
                        break
            
            if not found:
                st.error("⚠️ **Unknown Condition:** No matching rule found. Please consult an agricultural extension officer.")
                st.session_state.query_log.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Crop": crop,
                    "Soil": soil,
                    "Symptoms": symptoms_input,
                    "pH": soil_ph,
                    "Moisture": soil_moisture,
                    "Diagnosis": "Unknown Condition"
                })

with tab2:
    st.subheader("🌾 Crop Market Intelligence & ROI Calculator")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        land_area = st.number_input("Enter Land Area (in Acres):", min_value=0.5, value=1.0, step=0.5)
        expected_yield = st.number_input("Expected Yield per Acre (Tons):", min_value=0.5, value=2.5, step=0.5)
    
    with col_m2:
        cost_per_acre = st.number_input("Estimated Production Cost per Acre ($):", min_value=100, value=500, step=50)
        market_price_per_ton = st.number_input("Current Market Price per Ton ($):", min_value=50, value=350, step=25)
    
    total_cost = land_area * cost_per_acre
    total_yield = land_area * expected_yield
    total_revenue = total_yield * market_price_per_ton
    net_profit = total_revenue - total_cost
    roi = (net_profit / total_cost) * 100 if total_cost > 0 else 0
    
    st.markdown("---")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Total Investment", f"${total_cost:,.2f}")
    m_col2.metric("Total Production", f"{total_yield:.2f} Tons")
    m_col3.metric("Projected Revenue", f"${total_revenue:,.2f}")
    m_col4.metric("Estimated Net Profit", f"${net_profit:,.2f}", delta=f"{roi:.1f}% ROI")

with tab3:
    st.subheader("📊 Diagnostic Summary & Platform Metrics")
    if st.session_state.query_log:
        df_logs = pd.DataFrame(st.session_state.query_log)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Diagnoses Distribution**")
            st.bar_chart(df_logs["Diagnosis"].value_counts())
        
        with c2:
            st.markdown("**Crop Query Frequency**")
            st.bar_chart(df_logs["Crop"].value_counts())
    else:
        st.info("Run diagnostics to see visual graphs and analytics dashboard.")