import streamlit as st
import requests
import pandas as pd
import json
import io

# API endpoints
API_URL_SINGLE = "https://personality-detector.onrender.com/predict"
API_URL_CSV = "https://personality-detector.onrender.com/predict-csv"

st.set_page_config(page_title="🧠 Personality Predictor", layout="centered")

# ---------------- Sidebar ----------------
st.sidebar.title("🧠 Personality Predictor")
mode = st.sidebar.radio("Choose Input Mode", ["-- Select --", "Single JSON Input", "CSV File Upload"])

# ---------------- Page Title ----------------
st.title("✨ Predict Personality Type")
st.markdown("Use behavioral traits to determine if a person is an **Introvert** or **Extrovert**.")

# ---------------- Content Rendering ----------------
if mode == "Single JSON Input":
    st.header("🔍 JSON Input Form")
    st.markdown("Paste a single person's data below in JSON format.")

    default_json = {
        "Time_spent_Alone": 5,
        "Stage_fear": "No",
        "Social_event_attendance": 8,
        "Going_outside": 7,
        "Drained_after_socializing": "Yes",
        "Friends_circle_size": 3,
        "Post_frequency": 2
    }

    input_json = st.text_area("Paste JSON input", value=json.dumps(default_json, indent=2), height=300)

    if st.button("🔎 Predict Personality"):
        try:
            data = json.loads(input_json)
            response = requests.post(API_URL_SINGLE, json=data)
            if response.status_code == 200:
                result = response.json()
                st.success(f"🧠 Predicted Personality: **{result['Personality']}**")
            else:
                st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
        except json.JSONDecodeError:
            st.error("🚫 Invalid JSON format. Please correct and try again.")
        except Exception as e:
            st.error(f"❗ Request failed: {e}")

elif mode == "CSV File Upload":
    st.header("📄 CSV File Upload")
    st.markdown("Upload a CSV file with **multiple people's data** and get predictions in bulk.")

    st.info("**Required columns:**\n\n"
            "`Time_spent_Alone`, `Stage_fear`, `Social_event_attendance`, `Going_outside`, "
            "`Drained_after_socializing`, `Friends_circle_size`, `Post_frequency`")

    uploaded_file = st.file_uploader("📤 Upload CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.markdown("### 👀 Preview of Uploaded Data")
        st.dataframe(df.head())

        if st.button("🔍 Get Predictions"):
            try:
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(API_URL_CSV, files=files)

                if response.status_code == 200:
                    st.success("✅ Prediction completed! Preview below and download your result.")

                    result_df = pd.read_csv(io.StringIO(response.content.decode("utf-8")))
                    st.markdown("### 📊 Predicted Results Preview")
                    st.dataframe(result_df.head())

                    st.download_button(
                        label="📥 Download Full Predicted CSV",
                        data=response.content,
                        file_name="predicted_personality.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(f"❌ Prediction failed: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"❗ Error processing CSV: {e}")
else:
    st.markdown("⬅️ Select an input mode from the sidebar to begin.")
