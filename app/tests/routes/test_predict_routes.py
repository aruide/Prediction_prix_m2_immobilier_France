import pytest
from fastapi.testclient import TestClient
from app.main import app  # ou le fichier où l'instance FastAPI est définie (ex: "from app.api import app")
from unittest.mock import patch
from app.schemas.schemas_ville import Predict, VilleData

client = TestClient(app)

class TestPredictRoutes:
    
    def test_accueil(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Bienvenue sur l'api"}
        
    
    @patch("app.services.predict_services.PredictService.use_models")  # adapte le chemin réel
    @patch("app.services.predict_services.PredictService.verify_ville")
    def test_predict_route_valid(self, mock_verify_ville, mock_use_models):
        mock_verify_ville.return_value = True
        mock_use_models.return_value = {
            "prix_m2_estime": 3200.0,
            "ville_modele": "Lille",
            "model": "RandomForestRegressor"
        }

        data = {
            "ville": "Lille",
            "features": {
                "surface_bati": 90.0,
                "nombre_pieces": 4,
                "type_local": "maison",
                "surface_terrain": 150.0,
                "nombre_lots": 1
            }
        }

        response = client.post("/predict", json=data)
        assert response.status_code == 200
        assert response.json()["prix_m2_estime"] == 3200.0
    
    
    
    @patch("app.services.predict_services.PredictService.verify_ville")
    def test_predict_route_invalid_ville(self, mock_verify_ville):
        mock_verify_ville.return_value = False

        data = {
            "ville": "Atlantis",
            "features": {
                "surface_bati": 90.0,
                "nombre_pieces": 4,
                "type_local": "maison",
                "surface_terrain": 150.0,
                "nombre_lots": 1
            }
        }

        response = client.post("/predict", json=data)
        assert response.status_code == 200
        assert response.json() == {"message": "ville inconnue"}
        
    
    @patch("app.services.predict_services.PredictService.verify_ville")
    @patch("app.services.predict_services.PredictService.use_models")
    def test_predict_ville_valid(self, mock_use_models, mock_verify_ville):
        mock_verify_ville.return_value = True
        mock_use_models.return_value = {
            "prix_m2_estime": 3500.0,
            "ville_modele": "Lille",
            "model": "XGBRegressor"
        }

        data = {
            "surface_bati": 100.0,
            "nombre_pieces": 5,
            "type_local": "appartement",
            "surface_terrain": 0.0,
            "nombre_lots": 2
        }

        response = client.post("/predict/Lille", json=data)
        assert response.status_code == 200
        assert response.json()["prix_m2_estime"] == 3500.0
    
    
    @patch("app.services.predict_services.PredictService.verify_ville")
    def test_predict_ville_invalid(self, mock_verify_ville):
        mock_verify_ville.return_value = False

        data = {
            "surface_bati": 100.0,
            "nombre_pieces": 5,
            "type_local": "maison",
            "surface_terrain": 300.0,
            "nombre_lots": 1
        }

        response = client.post("/predict/Atlantis", json=data)
        assert response.status_code == 200
        assert response.json() == {"message": "ville inconnue"}
        
        
    def test_predict_validation_error(self):
        data = {
            "ville": "Lille",
            "features": {
                # manque surface_bati
                "nombre_pieces": 4,
                "type_local": "maison",
                "surface_terrain": 150.0,
                "nombre_lots": 1
            }
        }

        response = client.post("/predict", json=data)
        assert response.status_code == 422
        assert "surface_bati" in response.text