import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(page_title="Employee Attrition Predictor", layout="wide")

# Title and description
st.title("🔮 Employee Attrition Prediction")
st.markdown("Predict whether an employee is likely to leave the company based on their characteristics.")

# Load the trained model
try:
    model = joblib.load('logistic_regression_model.pkl')
except FileNotFoundError:
    st.error("❌ Model file 'logistic_regression_model.pkl' not found. Please train the model first.")
    st.stop()

# Create sidebar for input
st.sidebar.header("📋 Employee Information")

# Get user inputs
age = st.sidebar.number_input("Age", min_value=18, max_value=70, value=35, step=1)
years_at_company = st.sidebar.number_input("Years at Company", min_value=0, max_value=40, value=5, step=1)
job_satisfaction = st.sidebar.number_input("Job Satisfaction", min_value=1, max_value=4, value=2, step=1)
overtime = st.sidebar.selectbox("OverTime", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
department = st.sidebar.selectbox("Department", options=["Sales", "Research & Development", "Human Resources"])

# Create a prediction button
if st.sidebar.button("🔍 Predict Attrition", use_container_width=True):
    # Prepare input data
    input_data = pd.DataFrame({
        'Department': [department],
        'OverTime': [overtime],
        'YearsAtCompany': [years_at_company],
        'JobSatisfaction': [job_satisfaction],
        'Age': [age]
    })
    
    # Make prediction
    prediction = model.predict(input_data)[0]
    prediction_proba = model.predict_proba(input_data)[0]
    
    # Display results
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Prediction Result")
        if prediction == 1:
            st.warning("⚠️ High Risk of Attrition")
            attrition_text = "This employee is likely to leave"
            attrition_prob = prediction_proba[1]
        else:
            st.success("✅ Low Risk of Attrition")
            attrition_text = "This employee is likely to stay"
            attrition_prob = prediction_proba[0]
        
        st.markdown(f"**Prediction:** {attrition_text}")
        st.markdown(f"**Confidence:** {attrition_prob*100:.2f}%")
    
    with col2:
        st.subheader("📋 Employee Summary")
        st.write(f"**Age:** {age} years")
        st.write(f"**Years at Company:** {years_at_company} years")
        st.write(f"**Job Satisfaction:** {job_satisfaction}/4")
        st.write(f"**OverTime:** {'Yes' if overtime == 1 else 'No'}")
        st.write(f"**Department:** {department}")
    
    # Show probability distribution
    st.divider()
    st.subheader("📈 Prediction Confidence")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Will Stay", f"{prediction_proba[0]*100:.2f}%")
    with col2:
        st.metric("Will Leave", f"{prediction_proba[1]*100:.2f}%")
    
    # Progress bar
    st.progress(prediction_proba[1])
