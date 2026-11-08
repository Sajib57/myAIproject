import json
import os

class KrishiMitraExpertSystem:
    def __init__(self, knowledge_base_file="rules.json"):
        self.kb_file = knowledge_base_file
        self.knowledge_base = self.load_knowledge_base()

    def load_knowledge_base(self):
        """নলেজ বেস ফাইল লোড করে"""
        if not os.path.exists(self.kb_file):
            print(f"Error: {self.kb_file} file not found!")
            return {}
        with open(self.kb_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def diagnose(self, crop_name, user_symptoms, soil_type):
        """Forward Chaining দিয়ে রুল ম্যাচ করে রোগ ও পরামর্শ বের করে"""
        crop_name = crop_name.lower().strip()
        soil_type = soil_type.lower().strip()
        user_symptoms = [s.lower().strip() for s in user_symptoms]

        if crop_name not in self.knowledge_base:
            return None, "Crop not found in knowledge base."

        crop_rules = self.knowledge_base[crop_name]
        
        for rule in crop_rules:
            # Check if all symptoms match and soil type matches
            symptom_match = all(symptom in user_symptoms for symptom in rule["symptoms"])
            soil_match = rule["soil_type"] == soil_type

            if symptom_match and soil_match:
                return rule["disease"], rule["recommendation"]

        return "Unknown Condition", "No specific rule matched. Please consult an expert physically."

def main():
    print("=" * 60)
    print("🌾 WELCOME TO KRISHI MITRA: AGRICULTURAL EXPERT SYSTEM 🌾")
    print("=" * 60)

    expert = KrishiMitraExpertSystem()

    print("\nAvailable Crops: Rice, Wheat, Potato")
    crop = input("Enter Crop Name: ").strip()

    print("\nEnter Symptoms (comma separated, e.g., yellow leaves, stunted growth):")
    symptoms_input = input("Symptoms: ").split(",")
    symptoms = [s.strip() for s in symptoms_input]

    print("\nEnter Soil Type (e.g., clay, loam, sandy):")
    soil = input("Soil Type: ").strip()

    print("\n" + "-" * 40)
    print("🤖 Analyzing Inference Engine...")
    print("-" * 40)

    disease, advice = expert.diagnose(crop, symptoms, soil)

    if disease:
        print(f"📌 Diagnosed Disease / Issue: {disease}")
        print(f"💡 Recommended Action      : {advice}")
    else:
        print(f"⚠️ {advice}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()