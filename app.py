import joblib
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Bank Marketing Subscription Predictor",
    page_icon="🏦",
    layout="centered",
)

MODEL_PATH = Path("best_bank_marketing_model.pkl")

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model file not found. Place best_bank_marketing_model.pkl "
            "in the same folder as app.py."
        )
    return joblib.load(MODEL_PATH)

st.title("Bank Marketing Subscription Predictor")
st.write(
    "Enter the customer and campaign details below to estimate whether "
    "the customer is likely to subscribe to a term deposit."
)

with st.form("prediction_form"):
    age = st.number_input("Age", min_value=18, max_value=100, value=35)
    job = st.selectbox(
        "Job",
        [
            "admin.", "blue-collar", "entrepreneur", "housemaid",
            "management", "retired", "self-employed", "services",
            "student", "technician", "unemployed", "unknown"
        ]
    )
    marital = st.selectbox("Marital status", ["divorced", "married", "single"])
    education = st.selectbox(
        "Education",
        ["primary", "secondary", "tertiary", "unknown"]
    )
    default = st.selectbox("Credit in default", ["no", "yes"])
    balance = st.number_input("Average yearly balance", value=1500)
    housing = st.selectbox("Housing loan", ["no", "yes"])
    loan = st.selectbox("Personal loan", ["no", "yes"])
    contact = st.selectbox("Contact type", ["cellular", "telephone", "unknown"])
    day = st.number_input("Last contact day of month", min_value=1, max_value=31, value=15)
    month = st.selectbox(
        "Last contact month",
        ["jan", "feb", "mar", "apr", "may", "jun",
         "jul", "aug", "sep", "oct", "nov", "dec"]
    )
    duration = st.number_input(
        "Last contact duration in seconds",
        min_value=0,
        value=300
    )
    campaign = st.number_input(
        "Number of contacts in current campaign",
        min_value=1,
        value=2
    )
    pdays = st.number_input(
        "Days since previous contact (-1 if never contacted)",
        min_value=-1,
        value=-1
    )
    previous = st.number_input(
        "Number of contacts before current campaign",
        min_value=0,
        value=0
    )
    poutcome = st.selectbox(
        "Previous campaign outcome",
        ["failure", "other", "success", "unknown"]
    )

    submitted = st.form_submit_button("Predict")

if submitted:
    try:
        model = load_model()

        contacted_before = int(pdays != -1)
        previous_success = int(poutcome == "success")
        balance_per_age = balance / age if age else 0
        has_any_loan = int(housing == "yes" or loan == "yes")

        customer = pd.DataFrame([{
            "age": age,
            "job": job,
            "marital": marital,
            "education": education,
            "default": default,
            "balance": balance,
            "housing": housing,
            "loan": loan,
            "contact": contact,
            "day": day,
            "month": month,
            "duration": duration,
            "campaign": campaign,
            "pdays": pdays,
            "previous": previous,
            "poutcome": poutcome,
            "contacted_before": contacted_before,
            "previous_success": previous_success,
            "balance_per_age": balance_per_age,
            "has_any_loan": has_any_loan
        }])

        prediction = int(model.predict(customer)[0])

        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(customer)[0, 1])
        else:
            probability = None

        if prediction == 1:
            st.success("Prediction: Likely to subscribe")
        else:
            st.warning("Prediction: Unlikely to subscribe")

        if probability is not None:
            st.metric("Estimated subscription probability", f"{probability:.1%}")

        with st.expander("View submitted customer data"):
            st.dataframe(customer)

    except Exception as exc:
        st.error(f"Prediction could not be completed: {exc}")

st.caption(
    "Academic demonstration for MSN5207C Data Processing Methods. "
    "The model should support, not replace, human decision-making."
)
