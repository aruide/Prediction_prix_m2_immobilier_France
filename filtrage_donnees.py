import pandas as pd
import os
import argparse

def nettoyer_et_exporter(df_ville: pd.DataFrame, nom_ville: str, export_csv=False):
    colonnes_virgule = ["Valeur fonciere", "Surface reelle bati", "Surface terrain"]
    for col in colonnes_virgule:
        df_ville[col] = df_ville[col].astype(str).str.replace(',', '.').astype(float)

    # Calcul du prix au m2 (à refaire ici après conversion)
    df_ville["prix_m2"] = df_ville["Valeur fonciere"] / df_ville["Surface reelle bati"]

    type_mapping = {
        "Valeur fonciere": "float",
        "Surface reelle bati": "float",
        "Nombre pieces principales": "Int64",
        "Surface terrain": "float",
        "Commune": "string",
        "Code postal": "string",
        "Code type local": "Int64",
        "Type local": "string",
        "Nombre de lots": "Int64",
        "prix_m2": "float"
    }

    df_ville = df_ville.astype(type_mapping)

    # Export
    nom_fichier_base = f"data/clean/{nom_ville.lower()}_2022"
    df_ville.to_parquet(f"{nom_fichier_base}.parquet", index=False)
    if export_csv:
        df_ville.to_csv(f"{nom_fichier_base}.csv", index=False)

    print(f"✅ Export terminé pour {nom_ville}.")

def clean(export_csv=False):
    # Lecture brute
    df = pd.read_csv("data/raw/ValeursFoncieres-2022.txt", sep='|', low_memory=False)

    colonnes_a_garder = [
        "Valeur fonciere",
        "Surface reelle bati",
        "Nombre pieces principales",
        "Surface terrain",
        "Commune",
        "Code postal",
        "Code type local",
        "Type local",
        "Nombre de lots"
        # On n'ajoute PAS encore prix_m2 ici — il sera créé après filtrage
    ]

    df["Commune"] = df["Commune"].str.upper()

    # Préparation dossier
    os.makedirs("data/clean", exist_ok=True)

    for ville in ["LILLE", "BORDEAUX"]:
        df_ville = df[
            (df["Commune"] == ville) &
            (df["Nature mutation"] == "Vente") &
            (df["Surface reelle bati"].notna()) &
            (df["Valeur fonciere"].notna()) &
            (df["Type local"].isin(["Appartement", "Maison"]))
        ][colonnes_a_garder].copy()

        nettoyer_et_exporter(df_ville, ville, export_csv=export_csv)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", action="store_true", help="Exporter aussi au format CSV")
    args = parser.parse_args()

    clean(export_csv=args.csv)
