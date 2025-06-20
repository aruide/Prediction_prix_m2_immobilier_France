import pandas as pd
import os

def clean():
    # Chargement
    df = pd.read_csv("data/raw/ValeursFoncieres-2022.txt", sep='|', low_memory=False)

    # Harmonisation
    df['Commune'] = df['Commune'].str.upper()

    # Filtrage LILLE
    df_lille = df[
        (df['Commune'] == 'LILLE') & 
        (df['Nature mutation'] == 'Vente') & 
        (df['Surface reelle bati'].notna()) & 
        (df['Valeur fonciere'].notna())
    ].copy()

    # Filtrage BORDEAUX
    df_bordeaux = df[
        (df['Commune'] == 'BORDEAUX') & 
        (df['Nature mutation'] == 'Vente') & 
        (df['Surface reelle bati'].notna()) & 
        (df['Valeur fonciere'].notna())
    ].copy()

    # Conversion en float
    for df_city in [df_lille, df_bordeaux]:
        df_city['Valeur fonciere'] = (
            df_city['Valeur fonciere']
            .astype(str)
            .str.replace(',', '.')
            .str.replace(' ', '')
            .astype(float)
        )
        df_city['Surface reelle bati'] = (
            df_city['Surface reelle bati']
            .astype(str)
            .str.replace(',', '.')
            .str.replace(' ', '')
            .astype(float)
        )

    # Calcul du prix au m²
    df_lille['prix_m2'] = df_lille['Valeur fonciere'] / df_lille['Surface reelle bati']
    df_bordeaux['prix_m2'] = df_bordeaux['Valeur fonciere'] / df_bordeaux['Surface reelle bati']

    # Export en .parquet
    os.makedirs("data", exist_ok=True)
    df_lille.to_parquet("data/clean/lille_2022.parquet", index=False)
    df_bordeaux.to_parquet("data/clean/bordeaux_2022.parquet", index=False)

    print("Export Parquet terminé.")

if __name__ == "__main__":
    clean()
