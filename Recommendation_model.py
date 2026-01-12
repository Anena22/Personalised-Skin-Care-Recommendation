import joblib
import streamlit as st 
from PIL import Image

# --- Load Models/Encoders ---
model = joblib.load('model.pkl')
le1 = joblib.load('le1.pkl')   
le2 = joblib.load('le2.pkl')  
le3 = joblib.load('le3.pkl')   
le4 = joblib.load('le4.pkl')   
le5 = joblib.load('le5.pkl')   
le6 = joblib.load('le6.pkl')   
le7 = joblib.load('le7.pkl')   
Product_mappings = joblib.load('product_mappings.pkl')



# --- Page Config ---
st.set_page_config(page_title="Skin Care Recommender", layout="centered")

# --- Sidebar (global settings only) ---
st.sidebar.title("⚙️ Settings")

# Theme toggle
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark", "Skin Glow"])

# Clear inputs button
clear_inputs = st.sidebar.button("🧹 Clear Inputs")

# --- Apply Theme ---
if theme == "Light":
    st.markdown("""
        <style>
        .stApp { background-color: #ffffff; color: black; }
        </style>
    """, unsafe_allow_html=True)
elif theme == "Dark":
    st.markdown("""
        <style>
        .stApp { background-color: #1e1e1e; color: white; }
        </style>
    """, unsafe_allow_html=True)
elif theme == "Skin Glow":
    st.markdown("""
        <style>
        .stApp { background-color: #f8bbd0; color: black; }
        </style>
    """, unsafe_allow_html=True)

# --- Main Area ---
st.title("🧴 Personalized Skin Care Product Recommendation")
st.subheader("✨ Your Skin, Your Perfect Match")
st.write("We’ll recommend the best skincare routine for your needs — just tell us about your skin profile below.")

st.image(r"C:\Users\ANENA\OneDrive\ML Final PROJECT\AI Images for Skincare.jpeg", use_container_width=True)

# --- Input Widgets ---
if clear_inputs:
    st.session_state.skin_type = "skin_type"
    st.session_state.skin_tone = "skin_tone"
    st.session_state.gender = "gender"
    st.session_state.skin_concerns = "skin_concerns"
    st.session_state.preference= "preference"
    st.session_state.brand= "brand"
    st.session_state.active_compunds = "active_compounds"
    st.session_state.ratings = 5.0

skin_type = st.selectbox("Select your skin type *", ["Oily", "Dry", "Combination", "Sensitive"], key="skin_type")
skin_tone = st.selectbox("Select your skin tone *", ["Fair", "Medium", "Dark"], key="skin_tone")
gender = st.selectbox("Gender *", ["Female", "Male"], key="gender")
skin_concerns = st.selectbox("Main skin concern *", ["Aging", "Acne", "Dullness", "Pigmentation", "Redness"], key="skin_concerns")
preferences = st.selectbox("Product preference", ["Vegan", "Cruelty-Free", "Budget-Friendly"], key="preferences")
brand = st.selectbox("Preferred brand", ["Cetaphil", "Olay", "The Ordinary", "Neutrogena", "L’Oreal"], key="brand")
active_compounds = st.selectbox("Preferred active ingredient", ["", "Niacinamide", "Vitamin C", "Retinol", "Hyaluronic Acid", "Peptides", "Aloe Vera"], key="active")
ratings = st.slider("How important are product ratings? *", 1.0, 10.0, 5.0, key="ratings")

predict_btn = st.button("🔮 Get My Recommendation")

# --- Prediction with Validation ---
if predict_btn:
    if not skin_type or not skin_tone or not skin_concerns:
        st.warning("⚠️ Please fill in all required fields (marked with *).")
    else:
        try:
            # Encode categorical features
            skin_type_val = le1.transform([skin_type])[0]
            skin_tone_val = le2.transform([skin_tone])[0]
            gender_val = le3.transform([gender])[0]
            concerns_val = le4.transform([skin_concerns])[0]
            pref_val = le5.transform([preferences])[
                0] if preferences else le4.transform(["Budget-Friendly"])[0]
        
            brand_val = le6.transform([brand])[0] if brand else le6.transform(["Cetaphil"])[0]
            active_val = le7.transform([active_compounds])[0] if active_compounds else le7.transform(["Niacinamide"])[0]

            # Features
            features = [[skin_type_val, skin_tone_val, concerns_val,
                         pref_val, gender_val, brand_val, ratings, active_val]]

            prediction = model.predict(features)[0]
            # Show recommendations with images
            if prediction == 0:
                st.success("🌞 Your routine: **Serum + Sunscreen** → Perfect for daily protection and glow!")
            elif prediction == 1:
                st.success("💧 Your routine: **Toner + Serum + Sunscreen** → Hydration and defense in one.")
            elif prediction == 2:
                st.success("✨ Your routine: **Serum + Moisturizer** → Smooth and deeply nourishing.")
            elif prediction == 3:
                st.success("🌟 Your routine: **Serum + Moisturizer + Sunscreen** → Complete care for healthy skin!")
            elif prediction == 4:
                st.success("🧼 Your routine: **Cleanser + Toner + Serum + Moisturizer** → Full routine for best results!")

            

        except Exception as e:
            st.error(f"❌ Error in prediction: {e}")
else:
    st.info("👉 Fill in your details and click **Get My Recommendation** to see your personalized skincare routine.")
