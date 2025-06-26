from app.services.predict_services import PredictService
import pytest
from unittest.mock import patch, MagicMock
from app.schemas.schemas_ville import Predict, VilleData
import json
from pydantic import ValidationError

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
    payload = json.loads(result.body.decode("utf-8"))
    
    assert payload["prix_m2_estime"] == 3000.0
    assert payload["ville_modele"] == "Lille"
    assert payload["model"] == "RandomForestRegressor"

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
    payload = json.loads(result.body.decode("utf-8"))
    
    assert payload["prix_m2_estime"] == 5000.0
    assert payload["ville_modele"] == "Bordaux"
    assert payload["model"] == "XGBRegressor"

# ---------- use_models ----------

@pytest.mark.asyncio
@patch("app.services.predict_services.PredictService.choice_models")
async def test_use_models_predict_object(mock_choice_models):
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
    result = await service.use_models(data)
    #payload = json.loads(result.body.decode("utf-8"))
    assert result["prix_m2_estime"] == 4000
    assert result["ville_modele"] == "Lille"

@pytest.mark.asyncio
@patch("app.services.predict_services.PredictService.choice_models")
async def test_use_models_villedata_object(mock_choice_models):
    mock_choice_models.return_value = {"prix_m2_estime": 3200, "ville_modele": "Lille", "model": "XGBRegressor"}

    service = PredictService()
    data = VilleData(
        surface_bati=70.0,
        nombre_pieces=2,
        type_local="appartement",
        surface_terrain=0.0,
        nombre_lots=1
    )
    result = await service.use_models(data, ville="Lille")
    assert result["model"] == "XGBRegressor"

@pytest.mark.asyncio
async def test_use_models_invalid_type():
    service = PredictService()
    result = await service.use_models("invalid_type")
    content = json.loads(result.body)
    assert result.status_code == 422
    assert content["message"] == "modele de données non reconnu"

def test_use_models_invalid_type_local():
    with pytest.raises(ValidationError) as exc_info:
        VilleData(
            surface_bati=70.0,
            nombre_pieces=2,
            type_local="château", # valeur invalide
            surface_terrain=500.0,
            nombre_lots=1
        )
    
    errors = exc_info.value.errors()
    assert any("type_local" in e["loc"] and "doit être" in e["msg"] for e in errors)