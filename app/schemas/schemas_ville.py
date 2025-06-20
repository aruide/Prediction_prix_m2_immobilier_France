from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal, Optional

class VilleData(BaseModel):
    surface_bati: Optional[float]
    nombre_pieces: Optional[float] = Field(0, ge=0)
    type_local: str
    surface_terrain: Optional[float]
    nombre_lots: Optional[int] = Field(0, ge=0)

    @field_validator("type_local")
    def type_local_to_lower(cls, v):
        v_lower = v.lower()
        if v_lower not in ["appartement", "maison"]:
            raise ValueError(f"type local doit être 'maison' ou 'appartement', reçu {v}")
        return v_lower
    
    @model_validator(mode='after')
    def check_required_fields(cls, values):
        type_local = values.type_local
        if type_local == "maison":
            # surface_bati et surface_terrain doivent être > 0
            if not values.surface_bati or values.surface_bati <= 0:
                raise ValueError("Pour type_local='maison', surface_bati doit être > 0")
            if not values.surface_terrain or values.surface_terrain <= 0:
                raise ValueError("Pour type_local='maison', surface_terrain doit être > 0")
        elif type_local == "appartement":
            # nombre_lots et surface_bati doivent être > 0
            if not values.nombre_lots or values.nombre_lots <= 0:
                raise ValueError("Pour type_local='appartement', nombre_lots doit être > 0")
            if not values.surface_bati or values.surface_bati <= 0:
                raise ValueError("Pour type_local='appartement', surface_bati doit être > 0")
        return values

class Predict(BaseModel):
    ville: str
    features: VilleData
    
    @field_validator("ville")
    def ville_to_lower(cls, v):
        v_lower = v.lower()
        if v_lower not in ["lille", "bordeaux"]:
            raise ValueError(f"ville doit être 'lille' ou 'bordeaux', reçu {v}")
        return v_lower
        