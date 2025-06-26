from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from .routes.predict_routes import router

# Instanciation de l'application FastAPI
app = FastAPI(
    title="API Estimation Prix au m²",
    description="API FastAPI pour prédire le prix au m² à partir de modèles ML (Lille et Bordeaux)",
    version="1.0.0"
)

# Handler d’erreur pour la validation (Pydantic)
@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    route_path = request.scope["path"]
    missing_fields = []

    for error in exc.errors():
        field_path = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        reason = error["msg"]
        missing_fields.append(f"{field_path} ({reason})")

    # Personnalisation pour les routes de prédiction
    if route_path.startswith("/predict"):
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

    # Par défaut pour les autres routes
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Requête invalide.",
            "details": exc.errors()
        },
    )

# Inclusion des routes
app.include_router(router)
