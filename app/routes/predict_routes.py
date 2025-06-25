from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..schemas.schemas_ville import *
from ..services.predict_services import *
from fastapi.security import OAuth2PasswordRequestForm
import os

router = APIRouter()

@router.get("/", summary="Prédit un prix m2")
async def accueil():
    return "Bienvenue sur l'api"

@router.post("/predict", summary="Prédit un prix m2")
def predict(predict: Predict):
    predict_service = PredictService()
    if(predict_service.verify_ville(predict.ville)) :
        result = predict_service.use_models(predict)
        print(result)
        return result
    return "ville inconnue"

@router.post("/predict/{ville}", summary="Prédit un prix m2 pour une ville choisi")
async def predict_ville(ville: str, villeData: VilleData):
    predict_service = PredictService()
    if(predict_service.verify_ville(ville)) :
        predict_service.use_models(villeData)
    return "ville inconnue"