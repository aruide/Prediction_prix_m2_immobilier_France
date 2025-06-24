from pydantic import BaseModel, EmailStr
from typing import Optional

class VilleData(BaseModel):
    surface_bati: float
    nombre_pieces: int
    type_local: str
    surface_terrain: float
    nombre_lots: int

    
class Predict(BaseModel):
    ville: str
    features: VilleData