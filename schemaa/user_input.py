from pydantic import BaseModel,computed_field,Field
from typing import Literal,Annotated,Dict
from config.city_tier import tier1_cities, tier2_cities


# pydantic model for input validation
class UserInput(BaseModel):
    age: int
    weight: float
    height: float
    income_lpa: float
    smoker: bool
    city: str
    occupation: str

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:    
        if self.smoker and self.bmi > 30:
            return 'High Risk'
        elif self.smoker or self.bmi > 27:
            return 'Moderate Risk'
        else:
            return 'Low Risk'
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return 'Young'
        elif self.age < 45:
            return 'adult'
        elif self.age < 60:
            return 'Middle-aged'
        else:
            return 'Senior'
        
    @computed_field
    @property
    def city_tier(self) -> int:
        
        if self.city in tier1_cities:
            return 1
        elif self.city in tier2_cities:
            return 2
        else:
            return 3
        
def get_city_tier(city: str) -> int:
    tier_map = {
        "Mumbai": 1, "Delhi": 1, "Bangalore": 1,
        "Pune": 2, "Chennai": 2, "Kolkata": 2,
        "Lucknow": 3
    }
    return tier_map.get(city, 3)  # default tier