"""
Point d'entrée de l'application FastAPI.

Cette application charge des utilisateurs GitHub filtrés à partir d'un fichier JSON
et expose une API REST pour interroger ces utilisateurs, avec authentification JWT.
"""

from fastapi import FastAPI
from .routes.routes import router
from models import *
import json
import os

# Instanciation de l'application FastAPI avec titre, description et version
app = FastAPI(
    title="GitHub Users API",
    description="API pour gérer les utilisateurs GitHub filtrés",
    version="1.0"
)


# Inclusion des routes définies dans le routeur principal
app.include_router(router)