# 🏡 Prédiction du prix au m² en immobilier – Lille & Bordeaux

## 🎯 Objectif
Développer un prototype complet permettant de prédire automatiquement le prix au m² de biens immobiliers à partir des données publiques DVF (Demandes de Valeurs Foncières) pour les villes de Lille et Bordeaux.

Le projet inclut :
- Des modèles de machine learning entraînés sur les ventes immobilières de 2022,
- Une API REST sécurisée avec FastAPI pour exposer les prédictions,
- Une architecture de projet claire, modulaire et testée.

## 🗂️ Structure du projet

```bash
immoprice-api/
│
├── app/                              # API FastAPI
│   ├── models/ 
│   │    ├── Bordeaux/
│   │    │    ├── models_appartement_Bordeaux.pkl
│   │    │    └── models_maison_Bordeaux.pkl
│   │    └── Lille/
│   │         ├── models_appartement_Lille.pkl
│   │         └── models_maison_Lille.pkl
│   │
│   ├── routes/ 
│   │    └── predict_routes.py
│   │
│   ├── schemas/  
│   │    └── schemas_ville.py        
│   │
│   ├── services/
│   │    └── predict_services.py        
│   │
│   │
│   │
│   └── main.py                       # Lancement et routes de l’API
│ 
├── tests/
│       ├── routes/
│       │    └── models_maison_Bordeaux.pkl
│       └── services/
│            └── models_maison_Lille.pkl
│ 
├── data/                             # Données sources (non versionnées)
│   ├── clean/
│   │    ├── bordeaux_2022.csv
│   │    ├── bordeaux_2022.parquet
│   │    ├── lille_2022.csv
│   │    └── lille_2022.parquet
│   └── raw/
│        └── ValeursFoncieres-2022.txt
│
│
├── models/                           # Modèles ML sauvegardés
│   ├── pipeline_appartement_models.pkl
│   └── pipeline_maison_models.pkl
│
├── notebooks/                        # Analyse exploratoire & modélisation
│   ├── test_generalisation_bordeaux.ipynb
│   └── test_model_lille.ipynb
│
├── .gitignore                        # Fichiers à exclure (ex: /data/)
├── filtrage_donnees.py               # Dépendances Python
├── LICENCE                        
├── pytest.ini    
├── README.md                         # Ce fichier   
└── requirements.txt
```

## 📦 Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/aruide/Prediction_prix_m2_immobilier_France.git
cd Prediction_prix_m2_immobilier_France
```

2. Créer un environnement virtuel (Python 3.10 recommandé) :
```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. lancer le filtrage des données:
```bash
python filtrage_donnees.py
```
> rajouter `--csv` pour générer également les fichiers filtrés en .csv (lecture humaine).

5. lancer les notebooks dans l'ordre:
    1. test_model_lille.ipynb
    2. test_generalisation_bordeaux.ipynb 

## 🚀 Lancer l’API FastAPI

Démarrer le serveur de développement :
```bash
uvicorn app.main:app --reload
```

Accès :
- Interface : [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Documentation Swagger : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 📬 Endpoints disponibles
|Méthode|	Endpoint|	Description
|---|---|---
|GET|	/|	Message de bienvenue|
|POST|	/predict|	Prédiction du prix au m² à partir d’un JSON incluant la ville|
|POST|	/predict/`{ville}`|	Prédiction du prix au m² pour une ville donnée directement|

## Format du Json attendu
pour la route `/preditct`:

```json
{
    "ville": "bordeaux",
    "features": {
                    "surface_bati": 110,
                    "nombre_pieces": 4,
                    "type_local": "Maison",
                    "surface_terrain": 300,
                    "nombre_lots": 2
                }
}
```

pour la route `/predict/{ville}`:
```json
{
    "surface_bati": 100,
    "nombre_pieces": 4,
    "type_local": "Appartement",
    "surface_terrain": 0,
    "nombre_lots": 1
}
```

## 🧠 Modélisation
- Objectif : prédire automatiquement le prix au m² à partir des caractéristiques de biens immobiliers de 4 pièces.
- Types de biens étudiés : Maison et Appartement.
- Modèles testés :
    - LinearRegression
    - DecisionTreeRegressor
    - RandomForestRegressor
    - XGBRegressor
    - VotingRegressor (agrégation des 4 modèles précédents)
- Approche :
    - Tous les modèles ont été évalués individuellement sur Lille (données d'entraînement).
    - Le meilleur modèle (selon les performances) a été retenu pour chaque type de bien.
- Optimisation :
    - Recherche d'hyperparamètres avec GridSearchCV
- Évaluation :
    - Métriques utilisées : MSE, RMSE, MAE
    - Test de généralisation effectué sur les données de Bordeaux

## 🔬 Tests
Des tests unitaires sont fournis pour les services et routes.

pour lancer les tests:
```bash
pytest
```

## 🧪 Données utilisées

- Demandes de valeurs foncières – DVF 2022 

    → [https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/)
- Données filtrées : **Lille** et **Bordeaux**, **maisons/appartements 4 pièces uniquement**

## 📜 Licence
Projet éducatif réalisé dans le cadre d’un exercice individuel. Données publiques et modèle librement réutilisables.