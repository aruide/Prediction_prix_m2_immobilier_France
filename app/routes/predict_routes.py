from fastapi import APIRouter
from ..schemas.schemas_ville import *
from ..services.predict_services import *
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK

router = APIRouter()

@router.get("/", summary="route de base")
async def accueil():
    return JSONResponse(
            status_code=HTTP_200_OK,
            content= { "message":"Bienvenue sur l'api"}
        )


@router.post("/predict", summary="Prédit un prix m2")
async def predict(predict: Predict):
    predict_service = PredictService()
    if(predict_service.verify_ville(predict.ville)) :
        result = await predict_service.use_models(predict)
        return result
    return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content= { "message":"impossible de trouver la ville"}
        )


@router.post("/predict/{ville}", summary="Prédit un prix m2 pour une ville choisi")
async def predict_ville(ville: str, villeData: VilleData):
    predict_service = PredictService()
    if(predict_service.verify_ville(ville)) :
        result = await predict_service.use_models(villeData, ville)
        return result
    return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content= { "message":"impossible de trouver la ville"}
        )