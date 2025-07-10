from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import pandas as pd
import joblib
import io

router = APIRouter()

# Load the model
model = joblib.load("personality_model.pkl")

# Personality mapping
label_map = {'Introvert': 0, 'Extrovert': 1}
reverse_map = {v: k for k, v in label_map.items()}

binary_fields = ['Stage_fear', 'Drained_after_socializing']

class PersonalityInput(BaseModel):
    Time_spent_Alone: float
    Stage_fear: str
    Social_event_attendance: float
    Going_outside: float
    Drained_after_socializing: str 
    Friends_circle_size: float
    Post_frequency: float

def preprocess(df: pd.DataFrame):
    df[binary_fields] = df[binary_fields].apply(lambda x: x.map({'Yes': 1, 'No': 0}))
    return df

@router.post("/predict")
async def predict(input_data:PersonalityInput ):
    try:
        data = pd.DataFrame([input_data.dict()])
        data = preprocess(data)
        pred = model.predict(data)[0]
        result = reverse_map[pred]
        return {"code": 200, "message": "Prediction successful", "Personality": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

@router.post("/predict-csv")
async def predict_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        df_original = df.copy()
        df = preprocess(df)
        predictions = model.predict(df)
        df_original["Predicted_Personality"] = [reverse_map[p] for p in predictions]

        stream = io.StringIO()
        df_original.to_csv(stream, index=False)
        stream.seek(0)
        return StreamingResponse(stream, media_type="text/csv", headers={
            "Content-Disposition": "attachment; filename=predictions.csv"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV prediction failed: {e}")
