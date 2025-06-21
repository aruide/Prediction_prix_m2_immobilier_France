# Pr-diction_prix_m2_immobilier_France
Prédiction du prix au m² en immobilier en France


✅ Variables utiles pour la prédiction du prix (fort potentiel explicatif)
|Champ|	Utilité	Explication
|---|---
|Valeur fonciere|	✅ (utile pour créer la cible prix_m2)	Sert à calculer le prix total ou prix/m²
|Surface reelle bati|	✅	Sert à calculer prix_m2, corrélé au prix
|Nombre pieces principales|	✅	Reflète le type/volume du logement
|Surface terrain|	✅	Particulièrement utile pour les maisons
|Code postal / Commune|	✅✅	Localisation = un des facteurs majeurs du prix
|Code type local / Type local|	✅	Distingue maisons / appartements / locaux commerciaux
|Nombre de lots	✅|	Peut refléter un immeuble, une copropriété...

⚠️ Variables à considérer éventuellement (à tester selon le contexte)
|Champ|	Utilité potentielle	Pourquoi
|---|---
|Nature mutation|	⚠️ Moyenne	Vente classique ou succession peuvent impacter le prix
|Date mutation|	⚠️ Moyenne	Peut être transformée en année ou trimestre (tendance du marché)
|Code departement|	⚠️ Si tu ne prends pas Code postal	Redondant mais peut être utile si on simplifie la zone
|Section / No plan|	⚠️ Faible	Sert au cadastre, mais rarement utilisé pour le ML brut
|Nature culture / Nature culture speciale|	⚠️ (si terrains nus)	Peu utile sauf si tu analyses des terrains agricoles
|Surface Carrez du X lot|	⚠️ Moyenne	Redondant avec Surface reelle bati, à agréger éventuellement
|No voie, Voie, Code voie, Type de voie|	⚠️ Faible	Trop granulaire ou textuel → à encoder si tu veux de la géolocalisation fine
|Prefixe de section|	❓ Rarement utile	Cadastre, peu exploité sauf cas spécifiques
|No disposition, No Volume|	❌ Identifiants → à supprimer	

❌ Variables à supprimer directement
Champ	Raison
No disposition	Identifiant transaction inutile pour la modélisation
No voie, Code voie, No plan, No Volume	Trop spécifiques / identifiants / bruit
prix_m2	❌ uniquement en cible, pas en entrée
