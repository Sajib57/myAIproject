if st.button("Run Diagnostic Engine", type="primary"):
        if "healthy" in selected_symptoms and len(selected_symptoms) == 1:
            st.success("🎉 **Crop Status:** Healthy condition detected! No disease diagnosis needed.")
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
            
            exact_match = None
            partial_matches = []
            
            if crop_key in knowledge_base:
                for rule in knowledge_base[crop_key]:
                    symptom_overlap = [s for s in selected_symptoms if s in rule["symptoms"]]
                    soil_match = rule["soil_type"] == soil_key
                    
                    # Exact or High-confidence Match
                    if symptom_overlap and soil_match:
                        exact_match = rule
                        break
                    # Partial Match (At least 1 symptom matched)
                    elif symptom_overlap:
                        partial_matches.append(rule)
            
            if exact_match:
                disease = exact_match['disease']
                rec = exact_match['recommendation']
                st.success(f"📌 **Diagnosed Condition:** {disease}")
                st.info(f"💡 **Recommended Management Strategy:** {rec}")
                
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
            
            elif partial_matches:
                st.info("ℹ️ **Closest Match Advisory:** No exact combination matched, but based on your symptoms, consider these likely possibilities:")
                for p_rule in partial_matches[:2]:  # Show top 2 partial matches
                    st.write(f"• **Possible Issue:** {p_rule['disease']} — *{p_rule['recommendation']}*")
                
                st.session_state.query_log.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Crop": crop,
                    "Soil": soil,
                    "Symptoms": ", ".join(selected_symptoms),
                    "pH": soil_ph,
                    "Temp_C": temperature,
                    "Moisture_%": soil_moisture,
                    "Diagnosis": f"Partial Match ({partial_matches[0]['disease']})"
                })
            
            else:
                # General Soil & Climate Advisory Fallback
                st.info("🌱 **General Advisory:** Specific disease rule was not triggered, but maintain optimal field telemetry:")
                st.write(f"• Check if pH ({soil_ph}) and Moisture ({soil_moisture}%) align with normal {crop} field standards.")
                st.write("• Inspect leaves regularly for pest or fungal escalation.")
                
                st.session_state.query_log.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Crop": crop,
                    "Soil": soil,
                    "Symptoms": ", ".join(selected_symptoms),
                    "pH": soil_ph,
                    "Temp_C": temperature,
                    "Moisture_%": soil_moisture,
                    "Diagnosis": "General Advisory Provided"
                })