import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.routes import *
import os
from dotenv import load_dotenv
from api.models import *

load_dotenv()

client = TestClient(app)

def test_home():
    r = client.get("/")
    assert r.status_code == 200


def test_predict_ok():
    r = client.get("/predict")
    assert r.status_code == 200  

def test_predict_fail():
    r = client.get("/predict")
    assert r.status_code == 404 

def test_prix_m2_lille_ok():
    r = client.get("/predict/lille")
    assert r.status_code == 200

def test_prix_m2_lille_fail():
    r = client.get("/predict/lille")
    assert r.status_code == 404

def test_prix_m2_bordaux_ok():
    r = client.get("/predict/bordaux")
    assert r.status_code == 200

def test_prix_m2_bordaux_fail():
    r = client.get("/predict/bordaux")
    assert r.status_code == 404
