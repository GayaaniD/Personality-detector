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

# ---------------- Clear Trigger ----------------
if "clear_triggered" not in st.session_state:
    st.session_state.clear_triggered = False

if st.session_state.clear_triggered:
    st.session_state.update({
        "time_spent_alone": "",
        "stage_fear": "Yes",
        "social_event_attendance": "",
        "going_outside": "",
        "drained_after_socializing": "Yes",
        "friends_circle_size": "",
        "post_frequency": "",
        "clear_triggered": False
    })
    st.rerun()

# ---------------- Page Title ----------------
st.title("✨ Predict Personality Type")
st.markdown("Use behavioral traits to determine if a person is an **Introvert** or **Extrovert**.")

# ---------------- Content Rendering ----------------
if mode == "Single Entry Form":
    st.header("🧍 Single Person Input")
    st.markdown("Enter the behavioral traits below to predict personality type.")

    # Inputs with session state
    time_spent_alone = st.text_input(
        "🕒 Time Spent Alone (hours/day)",
        placeholder="e.g., 5",
        help="Average number of hours spent alone per day.",
        key="time_spent_alone"
    )

    stage_fear = st.radio(
        "🎤 Stage Fear?",
        options=["Yes", "No"],
        help="Do you fear speaking or performing in public?",
        key="stage_fear"
    )

    social_event_attendance = st.text_input(
        "🎉 Social Event Attendance (per day)",
        placeholder="e.g., 8",
        help="How often do you attend social events?",
        key="social_event_attendance"
    )

    going_outside = st.text_input(
        "🌳 Enjoyment of Going Outside",
        placeholder="Rate it from 0-10, e.g., 7",
        help="Rate how much you enjoy spending time outside.",
        key="going_outside"
    )

    drained_after_socializing = st.radio(
        "😫 Feel Drained After Socializing?",
        options=["Yes", "No"],
        help="Do you feel mentally exhausted after socializing?",
        key="drained_after_socializing"
    )

    friends_circle_size = st.text_input(
        "👥 Size of Friends Circle",
        placeholder="e.g., 3",
        help="How many close friends do you have?",
        key="friends_circle_size"
    )

    post_frequency = st.text_input(
        "📱 Social Media Post Frequency (posts/day)",
        placeholder="e.g., 2",
        help="How many times per week do you post on social media?",
        key="post_frequency"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔎 Predict Personality"):
            try:
                payload = {
                    "Time_spent_Alone": float(st.session_state["time_spent_alone"]),
                    "Stage_fear": st.session_state["stage_fear"].capitalize(),
                    "Social_event_attendance": float(st.session_state["social_event_attendance"]),
                    "Going_outside": float(st.session_state["going_outside"]),
                    "Drained_after_socializing": st.session_state["drained_after_socializing"].capitalize(),
                    "Friends_circle_size": float(st.session_state["friends_circle_size"]),
                    "Post_frequency": float(st.session_state["post_frequency"])
                }
                response = requests.post(API_URL_SINGLE, json=payload)
                if response.status_code == 200:
                    st.success(f"🧠 Predicted Personality: **{response.json()['Personality']}**")
                else:
                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
            except ValueError:
                st.error("🚫 Ensure all numeric fields are filled correctly.")
            except Exception as e:
                st.error(f"❗ Request failed: {e}")

    with col2:
        if st.button("🧹 Clear Input Fields"):
            st.session_state.clear_triggered = True
            st.rerun()

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
