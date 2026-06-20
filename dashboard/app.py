import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime

# ---------------------------
# PAGE CONFIG
# ---------------------------

st.set_page_config(
    page_title="AirSense AI",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------
# LOAD MODEL
# ---------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

model_path = os.path.join(
    BASE_DIR,
    "models",
    "random_forest_model.pkl"
)

model = joblib.load(model_path)

# ---------------------------
# SIDEBAR NAVIGATION
# ---------------------------
city_mapping_path = os.path.join(
    BASE_DIR,
    "models",
    "city_mapping.pkl"
)

city_mapping = joblib.load(
    city_mapping_path
)
page = st.sidebar.selectbox(
    "Navigation",
    
        [
    "Home",
    "AQI Predictor",
    "Model Performance",
    "Feature Importance",
    "Explainability",
    "About"
]
    
)

# ---------------------------
# HOME PAGE
# ---------------------------

if page == "Home":
  
    st.title("🌍 AirSense AI")

    st.subheader(
        "AQI Forecasting & Health Advisory System"
    )

    st.write("""
    AirSense AI predicts Air Quality Index (AQI)
    using Machine Learning and provides health
    recommendations based on pollution levels.
    """)
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Best Model",
        "Random Forest"
    )

    col2.metric(
        "R² Score",
        "0.91"
    )

    col3.metric(
        "Dataset Size",
        "24,850"
    )

    st.markdown("### Features")

    st.write("✅ AQI Prediction")
    st.write("✅ Health Advisory")
    st.write("✅ Model Comparison")
    st.write("✅ Feature Importance")
    st.write("✅ Explainable AI (SHAP)")
# ---------------------------
# AQI PREDICTOR PAGE
# ---------------------------

elif page == "AQI Predictor":

    st.title("AQI Prediction")

    selected_city = st.sidebar.selectbox(
        "Select City",
        list(city_mapping.keys())
)

    city = city_mapping[selected_city]

    pm25 = st.sidebar.number_input("PM2.5", value=50.0)
    pm10 = st.sidebar.number_input("PM10", value=80.0)
    no = st.sidebar.number_input("NO", value=20.0)
    no2 = st.sidebar.number_input("NO2", value=30.0)
    nox = st.sidebar.number_input("NOx", value=40.0)
    nh3 = st.sidebar.number_input("NH3", value=20.0)
    co = st.sidebar.number_input("CO", value=1.0)
    so2 = st.sidebar.number_input("SO2", value=15.0)
    o3 = st.sidebar.number_input("O3", value=25.0)
    benzene = st.sidebar.number_input("Benzene", value=5.0)
    toluene = st.sidebar.number_input("Toluene", value=5.0)

    today = datetime.now()

    year = today.year
    month = today.month
    day = today.day
    weekday = today.weekday()

    if month in [12,1,2]:
        season = 3
    elif month in [3,4,5]:
        season = 2
    elif month in [6,7,8,9]:
        season = 0
    else:
        season = 1

    if st.button("Predict AQI"):

        input_data = pd.DataFrame({
            'City':[city],
            'PM2.5':[pm25],
            'PM10':[pm10],
            'NO':[no],
            'NO2':[no2],
            'NOx':[nox],
            'NH3':[nh3],
            'CO':[co],
            'SO2':[so2],
            'O3':[o3],
            'Benzene':[benzene],
            'Toluene':[toluene],
            'year':[year],
            'month':[month],
            'day':[day],
            'weekday':[weekday],
            'Season':[season]
        })

        prediction = model.predict(input_data)[0]

        st.success(
            f"Predicted AQI : {prediction:.2f}"
        )

        if prediction <= 50:
            category = "Good"
            advice = "Air quality is satisfactory."

        elif prediction <= 100:
            category = "Moderate"
            advice = "Sensitive people should limit outdoor activity."

        elif prediction <= 200:
            category = "Poor"
            advice = "Wear a mask outdoors."

        elif prediction <= 300:
            category = "Unhealthy"
            advice = "Avoid strenuous outdoor activities."

        elif prediction <= 400:
            category = "Very Unhealthy"
            advice = "Stay indoors whenever possible."

        else:
            category = "Hazardous"
            advice = "Avoid all outdoor exposure."

        st.subheader("AQI Category")
        st.info(category)

        st.subheader("Health Advisory")
        st.warning(advice)
elif page == "Model Performance":

    st.title("Model Performance")

    results = pd.DataFrame({
        "Model":[
            "Linear Regression",
            "Random Forest",
            "XGBoost"
        ],
        "R2":[
            0.808865,
            0.910646,
            0.903641
        ]
    })


    st.dataframe(results)
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8,4))

    ax.bar(
        results["Model"],
        results["R2"]
    )

    ax.set_title("Model Comparison (R² Score)")
    ax.set_ylabel("R² Score")

    st.pyplot(fig)
elif page == "Feature Importance":

    st.title("Feature Importance")

    feature_path = os.path.join(
         BASE_DIR,
        "data",
        "processed",
        "feature_importance.csv"
)

    feature_df = pd.read_csv(feature_path)


    st.dataframe(feature_df.head(10))
    import matplotlib.pyplot as plt

    top_features = feature_df.head(10)

    fig, ax = plt.subplots(figsize=(10,6))

    ax.barh(
    top_features["Feature"],
    top_features["Importance"]
)

    ax.set_title("Top 10 Important Features")

    st.pyplot(fig)



elif page == "Explainability":

    st.title("SHAP Explainability")

    st.write("""
    SHAP (SHapley Additive exPlanations)
    helps explain which features contribute
    most to AQI prediction.
    """)

    shap_path = os.path.join(
        BASE_DIR,
        "screenshots",
        "shap_summary.png"
    )

    st.image(
        shap_path,
        caption="SHAP Summary Plot"
    )



elif page == "About":

    st.title("About AirSense AI")

    st.write("""
    ### AirSense AI

    AirSense AI is an end-to-end Machine Learning based
    AQI Forecasting and Health Advisory System.

    ### Key Features

    ✅ AQI Prediction

    ✅ Health Advisory System

    ✅ Model Comparison

    ✅ Feature Importance Analysis

    ✅ SHAP Explainability

    ✅ Interactive Dashboard

    ### Technologies Used

    - Python
    - Pandas
    - NumPy
    - Scikit-Learn
    - Random Forest
    - XGBoost
    - SHAP
    - Streamlit

    ### Best Model

    Random Forest Regressor

    R² Score: 0.91
    """)