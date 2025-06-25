from fastapi import FastAPI
from .routes.predict_routes import router
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from models import *
import json
import os

# Instanciation de l'application FastAPI avec titre, description et version
app = FastAPI(
    title="GitHub Users API",
    description="API pour gérer les utilisateurs GitHub filtrés",
    version="1.0"
)

@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    route_path = request.scope["path"]

    # Erreur personnalisée pour /predict
    if route_path.startswith("/predict"):
        missing_fields = []
        for error in exc.errors():
            field_path = ".".join(str(loc) for loc in error["loc"] if loc != "body")
            reason = error["msg"]
            missing_fields.append(f"{field_path} ({reason})")

        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Erreur dans la requête de prédiction.",
                "champs_problèmes": missing_fields,
                "exemple_attendu": {
                        "ville": "bordeaux",
                        "features": {
                            "surface_bati": 110,
                            "nombre_pieces": 4,
                            "type_local": "Maison",
                            "surface_terrain": 300,
                            "nombre_lots": 2
                        }
                    }
            },
        )
    elif route_path.startswith("/preditct/{ville}"):
        for error in exc.errors():
            field_path = ".".join(str(loc) for loc in error["loc"] if loc != "body")
            reason = error["msg"]
            missing_fields.append(f"{field_path} ({reason})")
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "surface_bati": 100,
                "nombre_pieces": 4,
                "type_local": "Appartement",
                "surface_terrain": 0,
                "nombre_lots": 1
                }
            )    
            
    # Erreur par défaut pour les autres routes
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Requête invalide.",
            "details": exc.errors()
        },
    )

# Inclusion des routes définies dans le routeur principal
app.include_router(router)