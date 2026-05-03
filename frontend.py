import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000//predict"

st.title("Insurance Premium Category Predictor")
st.markdown("Enter your details to predict your insurance premium category.")

age = st.number_input("Age", min_value=0, max_value=120, value=30)
weight = st.number_input("Weight (kg)", min_value=0.0, value=70.0)
height = st.number_input("Height (m)", min_value=0.0, value=1.75)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.0, value=5.0)    
smoker = st.selectbox("Smoker", options=[True, False])
city = st.selectbox("City", options=["Mumbai", "Delhi", "Bangalore", "Pune", "Chennai", "Kolkata", "Lucknow"])
occupation = st.selectbox("Occupation", options=['private_job','student','business_owner','retired','government_job','unemployed'])

if st.button("Predict Premium Category"):
    user_input = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    response = requests.post(API_URL, json=user_input)
    
    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Premium Category: {result['prediction']}")
    else:
        st.error("Error in prediction. Please try again.")