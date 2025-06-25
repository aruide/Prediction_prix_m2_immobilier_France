from app.services.predict_services import PredictService
import pytest
from unittest.mock import patch, MagicMock
from app.schemas.schemas_ville import Predict, VilleData

predict_service = PredictService()

class TestPredictService:
    
    # ---------- Tests simples ----------

    def test_verify_ville_valid(self):
        service = PredictService()
        result = service.verify_ville("Lille")
        assert type(result) == bool
        assert result is True

    def test_verify_ville_invalid(self):
        service = PredictService()
        result = service.verify_ville("Marseille")
        assert type(result) == bool
        assert result  is False

    def test_verify_type_local_valid(self):
        service = PredictService()
        result = service.verify_type_local("maison")
        assert type(result) == bool
        assert result is True

    def test_verify_type_local_invalid(self):
        service = PredictService()
        result = service.verify_type_local("villa")
        assert type(result) == bool
        assert result is False
        
# ---------- Mock du modèle ----------

@patch("app.services.predict_services.joblib.load")
def test_choice_models_maison(mock_joblib_load):
    mock_model = MagicMock()
    mock_model.predict.return_value = [3000]
    mock_model.named_steps = {"regressor": MagicMock(__class__=type("RandomForestRegressor", (), {}))}
    mock_joblib_load.return_value = mock_model

    service = PredictService()
    data = VilleData(
        surface_bati=100.0,
        nombre_pieces=4,
        type_local="maison",
        surface_terrain=200.0,
        nombre_lots=1
    )

    result = service.choice_models("Lille", data)
    assert result["prix_m2_estime"] == 3000.0
    assert result["ville_modele"] == "Lille"
    assert result["model"] == "RandomForestRegressor"

@patch("app.services.predict_services.joblib.load")
def test_choice_models_appartement(mock_joblib_load):
    mock_model = MagicMock()
    mock_model.predict.return_value = [5000]
    mock_model.named_steps = {"regressor": MagicMock(__class__=type("XGBRegressor", (), {}))}
    mock_joblib_load.return_value = mock_model

    service = PredictService()
    data = VilleData(
        surface_bati=80.0,
        nombre_pieces=3,
        type_local="appartement",
        surface_terrain=0.0,
        nombre_lots=2
    )

    result = service.choice_models("Bordaux", data)
    assert result["prix_m2_estime"] == 5000.0
    assert result["ville_modele"] == "Bordaux"
    assert result["model"] == "XGBRegressor"

# ---------- use_models ----------

@patch("app.services.predict_services.PredictService.choice_models")
def test_use_models_predict_object(mock_choice_models):
    mock_choice_models.return_value = {"prix_m2_estime": 4000, "ville_modele": "Lille", "model": "RandomForestRegressor"}

    service = PredictService()
    data = Predict(
        ville="Lille",
        features=VilleData(
            surface_bati=90.0,
            nombre_pieces=3,
            type_local="maison",
            surface_terrain=120.0,
            nombre_lots=1
        )
    )
    result = service.use_models(data)
    assert result["prix_m2_estime"] == 4000
    assert result["ville_modele"] == "Lille"

@patch("app.services.predict_services.PredictService.choice_models")
def test_use_models_villedata_object(mock_choice_models):
    mock_choice_models.return_value = {"prix_m2_estime": 3200, "ville_modele": "Lille", "model": "XGBRegressor"}

    service = PredictService()
    data = VilleData(
        surface_bati=70.0,
        nombre_pieces=2,
        type_local="appartement",
        surface_terrain=0.0,
        nombre_lots=1
    )
    result = service.use_models(data, ville="Lille")
    assert result["model"] == "XGBRegressor"

def test_use_models_invalid_type():
    service = PredictService()
    result = service.use_models("invalid_type")
    assert result is None

def test_use_models_invalid_type_local():
    service = PredictService()
    data = VilleData(
        surface_bati=70.0,
        nombre_pieces=2,
        type_local="château",
        surface_terrain=500.0,
        nombre_lots=1
    )
    result = service.use_models(data, ville="Lille")
    assert result == {"message": "type de logement inconnue"}