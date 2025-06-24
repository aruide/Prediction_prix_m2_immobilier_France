from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models import *
from ..schemas.schemas_ville import *
from fastapi.security import OAuth2PasswordRequestForm
import os

router = APIRouter()
access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

@router.post("/predict", summary="Prédit un prix m2")
async def predict(predict: Predict):
    return None

@router.post("/predict/{ville}", summary="Prédit un prix m2 pour une ville choisi")
async def predict_ville(ville: str, villeData: VilleData):
    return None