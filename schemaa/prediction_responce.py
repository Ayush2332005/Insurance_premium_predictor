from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):
    prediction_category: str = Field(..., description="Predicted insurance premium category",example="High")
    confidence: float = Field(..., description="Confidence score of the prediction", example=0.85)
    class_probabilities: Dict[str, float] = Field(..., description="Probabilities for each premium category", example={"Low": 0.1, "Medium": 0.05, "High": 0.85})
    
