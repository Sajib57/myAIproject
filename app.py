import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Krishi Mitra Pro", page_icon="🌾", layout="wide")

st.title("🌾 Krishi Mitra: Comprehensive Agricultural Diagnostic & Market Intelligence System")
st.write("Advanced AI Advisory Engine supporting Structured Symptom Selection, Crop Diversity, and Market Forecasting.")

# Session State Setup
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

# Country Regional Insights
ASIAN_COUNTRY_DATA = {
    "Bangladesh": {"predominant_soil": "Alluvial / Clay Loam", "fertility_index": "High", "common_deficiency": "Nitrogen, Zinc, Boron"},
    "India": {"predominant_soil": "Alluvial, Black & Red Soils", "fertility_index": "Moderate-High", "common_deficiency": "Nitrogen, Organic Carbon, Zinc"},
    "Pakistan": {"predominant_soil": "Indus Alluvial Soil", "fertility_index": "Moderate", "common_deficiency": "Nitrogen, Phosphorus"},
    "Vietnam": {"predominant_soil": "Mekong Delta Alluvial", "fertility_index": "High", "common_deficiency": "Potassium, Soil Acidity"},
    "Thailand": {"predominant_soil": "Sandy Loam / Clay Basins", "fertility_index": "Moderate", "common_deficiency": "Organic Carbon, Nitrogen"},
    "Nepal": {"predominant_soil": "Himalayan Hill Soil", "fertility_index": "Moderate", "common_deficiency": "Nitrogen, Boron"}
}

# Sidebar Info & Log
with st.sidebar:
    st.header("🌏 Asian Regional Fertility Profile")
    selected_country = st.selectbox("Select Country:", list(ASIAN_COUNTRY_DATA.keys()))
    info = ASIAN_COUNTRY_DATA[selected_country]
    
    st.write(f"**Predominant Soil:** {info['predominant_soil']}")
    st.write(f"**Fertility Index:** {info['fertility_index']}")
    st.write(f"**Key Deficiencies:** {info['common_deficiency']}")
    st.markdown("---")
    
    st.header("📜 Diagnostic Query Log")
    if st.session_state.query_log:
        df_log = pd.DataFrame(st.session_state.query_log)
        st.dataframe(df_log[["Timestamp", "Crop", "Diagnosis"]], use_container_width=True)
        
        csv_bytes = df_log.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export History (CSV)", data=csv_bytes, file_name="krishi_mitra_logs.csv", mime="text/csv")
    else:
        st.info("No queries recorded in this session.")

# Main Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🩺 Diagnostics & IoT Sensors", "📈 Seasonal Market Trends & ROI", "📊 Analytics Dashboard"])

with tab1:
    st.subheader("Crop Selection, Environment & Leaf Conditions")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        crop_options = ["Rice", "Wheat", "Potato", "Tomato", "Brinjal", "Cabbage", "Chili", "Onion"]
        crop = st.selectbox("Select Crop / Vegetable:", crop_options)
        soil = st.selectbox("Select Soil Type:", ["Clay", "Loam", "Sandy"])
        season = st.selectbox("Growing Season:", ["Summer", "Rainy", "Autumn", "Winter", "Spring", "Year-round"])
    
    with col2:
        st.markdown("**📡 IoT Field Sensors**")
        soil_moisture = st.slider("Soil Moisture Content (%)", 0, 100, 45)
        soil_ph = st.slider("Soil pH Level", 3.0, 10.0, 6.5, step=0.1)
        temperature = st.slider("Ambient Temperature (°C)", 0, 50, 26)
    
    with col3:
        st.markdown("**🍃 Select Leaf Symptoms (Options)**")
        
        # Pre-defined symptom options list
        AVAILABLE_SYMPTOMS = [
            "healthy",
            "yellow leaves",
            "brown spot",
            "stunted growth",
            "wilted tips",
            "dark spots",
            "white mold"
        ]
        
        # Multiselect Option Box instead of Text Chat
        selected_symptoms = st.multiselect(
            "Select one or multiple symptoms from list:",
            options=AVAILABLE_SYMPTOMS,
            default=["yellow leaves"]
        )
    
    if st.button("Run Diagnostic Engine", type="primary"):
        if "healthy" in selected_symptoms and len(selected_symptoms) == 1:
            st.success("🎉 **Crop Status:** Healthy condition detected! No disease diagnosis needed. Continue standard crop maintenance.")
            st.session_state.query_log.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Crop": crop,
                "Soil": soil,
                "Symptoms": "healthy",
                "pH": soil_ph,
                "Temp_C": temperature,
                "Moisture_%": soil_moisture,
                "Diagnosis": "Healthy Crop"
            })
        elif not selected_symptoms:
            st.warning("Please select at least one symptom option from the list.")
        else:
            crop_key = crop.lower()
            soil_key = soil.lower()
            
            found = False
            if crop_key in knowledge_base:
                for rule in knowledge_base[crop_key]:
                    # Dynamic Symptom Overlap Matching Logic
                    symptom_match = any(s in selected_symptoms for s in rule["symptoms"])
                    soil_match = rule["soil_type"] == soil_key
                    
                    if symptom_match and soil_match:
                        found = True
                        disease = rule['disease']
                        rec = rule['recommendation']
                        m_demand = rule.get("market_demand", "N/A")
                        p_trend = rule.get("price_trend", "N/A")
                        
                        ph_min, ph_max = rule.get("ideal_ph_range", [5.0, 7.5])
                        temp_min, temp_max = rule.get("ideal_temp_range", [15, 35])
                        moisture_min = rule.get("min_moisture", 30)
                        
                        st.success(f"📌 **Diagnosed Disease / Issue:** {disease}")
                        st.info(f"💡 **Recommended Action:** {rec}")
                        
                        # Market Highlight Card
                        st.markdown(f"📊 **Market Intelligence:** Demand: **{m_demand}** | Price Trend: **{p_trend}**")
                        
                        # Sensor Warnings
                        if not (ph_min <= soil_ph <= ph_max):
                            st.warning(f"⚠️ **pH Anomaly:** Soil pH ({soil_ph}) is outside optimum range ({ph_min} - {ph_max}).")
                        if not (temp_min <= temperature <= temp_max):
                            st.warning(f"⚠️ **Temperature Warning:** Current Temp ({temperature}°C) is outside optimum range ({temp_min}°C - {temp_max}°C).")
                        if soil_moisture < moisture_min:
                            st.warning(f"⚠️ **Moisture Deficit:** Soil moisture ({soil_moisture}%) is below minimum requirement ({moisture_min}%).")
                        
                        # Log Record
                        st.session_state.query_log.append({
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Crop": crop,
                            "Soil": soil,
                            "Symptoms": ", ".join(selected_symptoms),
                            "pH": soil_ph,
                            "Temp_C": temperature,
                            "Moisture_%": soil_moisture,
                            "Diagnosis": disease
                        })
                        break
            
            if not found:
                st.error("⚠️ **Unknown Condition:** No matching rule found in knowledge repository. Please consult an expert physically.")
                st.session_state.query_log.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Crop": crop,
                    "Soil": soil,
                    "Symptoms": ", ".join(selected_symptoms),
                    "pH": soil_ph,
                    "Temp_C": temperature,
                    "Moisture_%": soil_moisture,
                    "Diagnosis": "Unknown Condition"
                })

with tab2:
    st.subheader("🌾 Crop & Seasonal Vegetable Market Forecast Calculator")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        land_area = st.number_input("Cultivation Area (Acres):", min_value=0.5, value=1.0, step=0.5)
        expected_yield = st.number_input("Expected Yield per Acre (Tons):", min_value=0.5, value=3.5, step=0.5)
    
    with col_m2:
        cost_per_acre = st.number_input("Production Cost per Acre ($):", min_value=50, value=400, step=25)
        market_price_per_ton = st.number_input("Current Market Price per Ton ($):", min_value=50, value=350, step=25)
    
    total_cost = land_area * cost_per_acre
    total_yield = land_area * expected_yield
    total_revenue = total_yield * market_price_per_ton
    net_profit = total_revenue - total_cost
    roi = (net_profit / total_cost) * 100 if total_cost > 0 else 0
    
    st.markdown("---")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Total Investment", f"${total_cost:,.2f}")
    m_col2.metric("Total Harvest", f"{total_yield:.2f} Tons")
    m_col3.metric("Projected Revenue", f"${total_revenue:,.2f}")
    m_col4.metric("Net Margin", f"${net_profit:,.2f}", delta=f"{roi:.1f}% ROI")

with tab3:
    st.subheader("📊 Session Diagnostic & Crop Distribution Analytics")
    if st.session_state.query_log:
        df_analytics = pd.DataFrame(st.session_state.query_log)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Diagnosed Conditions Breakdown**")
            st.bar_chart(df_analytics["Diagnosis"].value_counts())
        
        with c2:
            st.markdown("**Crop Inquiry Frequency**")
            st.bar_chart(df_analytics["Crop"].value_counts())
    else:
        st.info("Perform diagnostic checks in Tab 1 to generate visual telemetry distribution.")