from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pickle
import pandas as pd
from schemaa.user_input import UserInput
from schemaa.prediction_responce import PredictionResponse
from model.predict import predict_output, MODEL_VERSION,model

app = FastAPI()

@app.get("/")
def home():
    return JSONResponse(content={"message": "Welcome to the Insurance Premium Category Predictor API!"})

@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "healthy",
                                 "model_version": MODEL_VERSION,
                                 "model_loaded": model is not None})


@app.post("/predict", response_model=PredictionResponse)
def predict_premium(data: UserInput):

    input_dict = data.model_dump()

    # 🔥 1. BMI
    input_dict["bmi"] = input_dict["weight"] / (input_dict["height"] ** 2)

    # 🔥 2. Age Group
    age = input_dict["age"]
    if age < 30:
        input_dict["age_group"] = "young"
    elif age < 50:
        input_dict["age_group"] = "adult"
    else:
        input_dict["age_group"] = "senior"

    # 🔥 3. Lifestyle Risk
    if input_dict["smoker"] and input_dict["bmi"] > 30:
        input_dict["lifestyle_risk"] = "high"
    elif input_dict["smoker"]:
        input_dict["lifestyle_risk"] = "medium"
    else:
        input_dict["lifestyle_risk"] = "low"

    # 🔥 4. City Tier (previous issue)
    def get_city_tier(city):
        tier_map = {
            "Mumbai": 1, "Delhi": 1, "Bangalore": 1,
            "Pune": 2, "Chennai": 2, "Kolkata": 2
        }
        return tier_map.get(city, 3)

    input_dict["City_Tier"] = get_city_tier(input_dict["city"])

    # 👉 Convert to DataFrame
    input_df = pd.DataFrame([input_dict])

    # ✅ Ensure correct column order (VERY IMPORTANT)
    input_df = input_df[
        [
            "age", "weight", "height", "income_lpa",
            "smoker", "city", "occupation",
            "City_Tier", "bmi", "age_group", "lifestyle_risk"
        ]
    ]

    try:
        # 🔥 5. Make Prediction
        prediction = predict_output(input_dict)

        return JSONResponse(content={"prediction": prediction})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)