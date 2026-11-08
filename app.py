import streamlit as st
from ai_logic import expert_system_inference, get_market_forecast

# Page Configuration
st.set_page_config(
    page_title="Krishi Mitra - Professional AI System",
    page_icon="🌾",
    layout="wide"
)

# Custom CSS for Professional Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🌾 Krishi Mitra: Professional Rule-Based Agricultural Expert System")
st.markdown("An advanced classical AI decision support framework designed for precision crop advisory, soil analysis, and disease diagnosis.")
st.markdown("---")

# Initialize Session State for History Logging
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar Input Panel
st.sidebar.header("🎛️ Field Parameters & Sensors")
st.sidebar.markdown("Configure environmental & soil metrics:")

soil_type = st.sidebar.selectbox("Soil Type", ["Loamy", "Sandy", "Clay"])
ph_level = st.sidebar.slider("Soil pH Level", 4.0, 9.0, 6.5)
nitrogen = st.sidebar.selectbox("Nitrogen Content", ["Low", "Medium", "High"])
temperature = st.sidebar.slider("Ambient Temperature (°C)", 15, 40, 28)
rainfall = st.sidebar.selectbox("Rainfall Level", ["Low", "Moderate", "High"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🩺 Diagnostic Input")
leaf_symptom = st.sidebar.selectbox(
    "Leaf Condition / Pathology",
    ["Healthy", "Brown Spots", "Yellowing Leaves", "Marginal Scorching"]
)

run_inference = st.sidebar.button("Execute AI Inference Engine", type="primary")

# Main Content Layout using Tabs
tab1, tab2, tab3 = st.tabs(["📊 Diagnostic Dashboard", "📈 Market & Economic Outlook", "📜 Execution Log & History"])

with tab1:
    if run_inference:
        # Run Rule-based Engine
        recs, ferts, diags, confidence = expert_system_inference(
            soil_type, ph_level, nitrogen, temperature, rainfall, leaf_symptom
        )
        
        # Save to Session History
        st.session_state.history.append({
            "soil": soil_type,
            "ph": ph_level,
            "symptom": leaf_symptom,
            "confidence": confidence
        })

        # Top Metrics Row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Inference Engine", value="Rule-Based (Symbolic AI)", delta="0% Black-Box")
        with col2:
            st.metric(label="Rule Confidence Score", value=f"{confidence}%", delta="High Precision")
        with col3:
            st.metric(label="System Status", value="Optimized", delta="Stable")

        st.markdown("---")
        
        # Results Display in Columns
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("🌾 Crop & Fertilizer Recommendations")
            for r in recs:
                st.success(r)
            for f in ferts:
                st.info(f)
                
        with c2:
            st.subheader("🩺 Pathological Diagnosis")
            for d in diags:
                st.warning(d)
                
    else:
        st.info("👈 Please set the parameters in the sidebar and click **'Execute AI Inference Engine'** to view the analytical breakdown.")

with tab2:
    st.subheader("📈 Economic & Market Demand Forecasting")
    st.write("Evaluating crop viability relative to regional demand metrics using symbolic rule tables.")
    
    selected_crop = st.selectbox("Select Crop for Market Insight", ["Rice", "Wheat", "Potatoes", "Maize", "Pulses", "Mustard", "Seasonal Vegetables"])
    market_data = get_market_forecast(selected_crop)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Market Demand", market_data["demand"])
    with m2:
        st.metric("Estimated Price Point", market_data["estimated_price"])
    with m3:
        st.metric("Price Trend", market_data["trend"])

with tab3:
    st.subheader("📜 Recent Inference Query Log")
    if len(st.session_state.history) > 0:
        for idx, entry in enumerate(reversed(st.session_state.history)):
            st.markdown(f"**Query #{len(st.session_state.history) - idx}** | Soil: `{entry['soil']}` | pH: `{entry['ph']}` | Symptom: `{entry['symptom']}` | Confidence: `{entry['confidence']}%`")
    else:
        st.write("No queries executed in the current session yet.")

# Footer note
st.markdown("---")
st.caption("Krishi Mitra Academic Project • Built with Streamlit & Classical AI Rule Engines")