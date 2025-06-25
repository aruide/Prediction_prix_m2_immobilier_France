from app.services.predict_services import PredictService

predict_service = PredictService()

class TestPredictService:
    
    def test_verify_ville(self):
        result = predict_service.verify_ville("Lille")
        assert type(result) == bool
        assert result == True
        
    def test_verify_type_local(self):
        result = predict_service.verify_type_local("maison")
        assert result == True