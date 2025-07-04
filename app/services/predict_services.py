from ..schemas.schemas_ville import *
import joblib
import pandas as pd
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_200_OK

liste_logement = {
    "maison": 1,
    "appartement": 2
}

liste_ville = ["Lille","Bordeaux"]

class PredictService:
    def verify_ville(self, ville: str) -> bool:
        return ville.lower().capitalize() in liste_ville
    
    def verify_type_local(self, type_local: str) -> bool:
        return type_local.lower() in liste_logement.keys()
    
    def choice_models(self, ville: str, data):
        ville = ville.lower().capitalize()
        type_local = data.type_local.lower()

        if type_local == "maison":
            df = pd.DataFrame([{
                "Surface terrain": data.surface_terrain,
                "Surface reelle bati": data.surface_bati
            }])
        else:
            df = pd.DataFrame([{
                "Nombre de lots": data.nombre_lots,
                "Surface reelle bati": data.surface_bati
            }])

        model = joblib.load(f"app/models/{ville}/models_{type_local}_{ville}.pkl")
        prediction = model.predict(df)[0]
        final_model = list(model.named_steps.values())[-1]
        model_name = final_model.__class__.__name__
        return JSONResponse(
                            status_code=HTTP_200_OK,
                            content= {
                                        "prix_m2_estime": float(prediction),
                                        "ville_modele": ville,
                                        "model": model_name
                                    } 
                           )
       
    async def use_models(self, data, ville = None):
        if type(data) == Predict:
            if(self.verify_type_local(data.features.type_local.lower())):
                return self.choice_models(data.ville, data.features)
            else:
                return JSONResponse(
                            status_code=HTTP_404_NOT_FOUND,
                            content= { "message":"type de logement inconnue"}
                        )
        elif type(data) == VilleData:
            if(self.verify_type_local(data.type_local.lower())):
                return self.choice_models(ville, data)
            else:
                return JSONResponse(
                            status_code=HTTP_404_NOT_FOUND,
                            content= { "message":"type de logement inconnue"}
                        )
        else:
            return JSONResponse(
                            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                            content= { "message":"modele de données non reconnu"}
                        )
    