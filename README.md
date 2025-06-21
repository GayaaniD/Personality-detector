# 🧠 Personality Detector

A web application to predict whether a person is an **Introvert** or **Extrovert** based on behavioral traits.

Built using **FastAPI** for the backend and **Streamlit** for the frontend.  
Supports both single JSON input and batch predictions via CSV upload.

---

## ✨ Features

- Predict personality type using a trained ML model (`personality_model.pkl`)
- REST API endpoints with FastAPI
- User-friendly frontend built in Streamlit
- Accepts:
  - 🧾 Single prediction via JSON
  - 📁 Bulk prediction via CSV file
- Preview and download predicted results in the UI

---

## 🧰 Tech Stack

- **Python**
- **FastAPI** – API framework
- **Streamlit** – Web UI
- **Scikit-learn** – ML model
- **Pandas** – Data handling
- **Joblib** – Model serialization

---

## ⚙️ Setup Instructions
### 1. Clone the Repository

```bash
git clone https://github.com/GayaaniD/Personality-detector.git
cd Personality-detector
```
### 2. Create a Virtual Environment & Install Dependencies

```bash
poetry install
```

---

## 🚀 Run the Applications
### ▶️ Start FastAPI Backend
```
python main.py
```
The backend will run at: http://localhost:8000

### 🖥️ Launch Streamlit Frontend
```
streamlit run streamlit_UI.py
```
The UI will be available at: http://localhost:8501

---

## 📡 API Endpoints
### 🔹 POST /predict
- Make a personality prediction using JSON data.
- ✅ Request Format:
  ```
  {
  "Time_spent_Alone": 5,
  "Stage_fear": "No",
  "Social_event_attendance": 8,
  "Going_outside": 7,
  "Drained_after_socializing": "Yes",
  "Friends_circle_size": 3,
  "Post_frequency": 2
  }
  ```
### 🔹 POST /predict-csv
- Upload a CSV file containing multiple records.
  - Returns a CSV file with an additional Predicted_Personality column.
  - ✅ Required Columns: Time_spent_Alone, Stage_fear, Social_event_attendance,Going_outside, Drained_after_socializing,Friends_circle_size, Post_frequency

---

## 🧠 About the Model
- The model is trained using behavioral data to classify individuals as Introvert or Extrovert.
- Simple classification model trained via scikit-learn using RandomForest algorithm.
- Uses features such as time spent alone, fear of public speaking, social habits, etc.

---

## 📌 Notes
- JSON keys and CSV headers must exactly match the expected names.
- Categorical fields must contain Yes or No values only.
- The Streamlit UI provides both manual and CSV upload options.







