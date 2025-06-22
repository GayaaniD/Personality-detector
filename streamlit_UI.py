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
mode = st.sidebar.radio("Choose Input Mode", ["-- Select --", "Single Entry Form", "CSV File Upload"])

# ---------------- Page Title ----------------
st.title("✨ Predict Personality Type")
st.markdown("Use behavioral traits to determine if a person is an **Introvert** or **Extrovert**.")

# ---------------- Content Rendering ----------------
if mode == "Single Entry Form":
    st.header("🧍 Single Person Input")
    st.markdown("Enter the behavioral traits below to predict personality type.")

    time_spent_alone = st.number_input(
        "🕒 Time Spent Alone (hours/day)",
        help="Average number of hours spent alone per day. (e.g., 5)"
    )

    stage_fear = st.text_input(
        "🎤 Stage Fear (Yes/No)",
        help="Do you fear speaking or performing in public?"
    )

    social_event_attendance = st.number_input(
        "🎉 Social Event Attendance",
        help="How frequently do you attend social events? (Numeric scale or event count)"
    )

    going_outside = st.number_input(
        "🌳 Enjoyment of Going Outside",
        help="How much do you enjoy spending time outside? (Rate numerically, e.g., 0 to 10)"
    )

    drained_after_socializing = st.text_input(
        "😫 Feel Drained After Socializing (Yes/No)",
        help="Do you feel mentally exhausted after socializing?"
    )

    friends_circle_size = st.number_input(
        "👥 Size of Friends Circle",
        help="How many close friends do you have?"
    )

    post_frequency = st.number_input(
        "📱 Social Media Post Frequency (posts/week)",
        help="How many times do you post on social media in a week?"
    )

    if st.button("🔎 Predict Personality"):
        json_payload = {
            "Time_spent_Alone": time_spent_alone,
            "Stage_fear": stage_fear.strip(),
            "Social_event_attendance": social_event_attendance,
            "Going_outside": going_outside,
            "Drained_after_socializing": drained_after_socializing.strip(),
            "Friends_circle_size": friends_circle_size,
            "Post_frequency": post_frequency
        }

        try:
            response = requests.post(API_URL_SINGLE, json=json_payload)
            if response.status_code == 200:
                result = response.json()
                st.success(f"🧠 Predicted Personality: **{result['Personality']}**")
            else:
                st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
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
