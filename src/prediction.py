import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_all_commodities_2030():
    # On pointe vers le fichier multi-produits généré par analysis.py
    input_path = "data/processed/denrees_afrique_ouest_clean.csv"
    if not os.path.exists(input_path): 
        print("❌ Fichier de données clean introuvable. Lancez d'abord analysis.py")
        return

    df = pd.read_csv(input_path)
    predictions = []

    # Liste des produits (Riz, Sucre, Céréales, etc.)
    products = df['commodity_name'].unique()

    for product in products:
        print(f"🔮 Calcul des prédictions pour : {product}")
        df_prod = df[df['commodity_name'] == product]
        
        for country in df_prod['reporterDesc'].unique():
            # Agrégation et tri chronologique strict
            data = df_prod[df_prod['reporterDesc'] == country].groupby('refYear').agg({
                'tonnes': 'sum', 
                'millions_usd': 'sum'
            }).reset_index().sort_values('refYear')
            
            # On ignore les pays avec moins de 3 points de données
            if len(data) < 3: continue

            # Préparation des données pour l'IA
            X = data['refYear'].values.reshape(-1, 1)
            y_vol = data['tonnes'].values
            y_val = data['millions_usd'].values

            # Entraînement des modèles linéaires
            model_vol = LinearRegression().fit(X, y_vol)
            model_val = LinearRegression().fit(X, y_val)

            # Calcul des prédictions théoriques pour 2030
            raw_vol_2030 = model_vol.predict([[2030]])[0]
            raw_val_2030 = model_val.predict([[2030]])[0]

            # --- LOGIQUE DE SÉCURITÉ CONTRE LE "0 TONNES" ---
            # On calcule la moyenne récente (3 dernières années) comme référence
            recent_avg_vol = y_vol[-3:].mean() if len(y_vol) >= 3 else y_vol.mean()
            recent_avg_val = y_val[-3:].mean() if len(y_val) >= 3 else y_val.mean()

            # Si la prédiction tombe sous 10% de la moyenne historique (risque de 0)
            # ou si elle est négative, on stabilise sur la moyenne récente
            if raw_vol_2030 < (y_vol.mean() * 0.1):
                vol_2030 = recent_avg_vol
                val_2030 = recent_avg_val
                tendance = "Stabilisation (Baisse Corrigée)"
            else:
                vol_2030 = raw_vol_2030
                val_2030 = raw_val_2030
                tendance = "Croissance Linéaire"

            predictions.append({
                'Pays': country,
                'Produit': product,
                'Volume_2030_Tonnes': round(max(0, vol_2030), 2),
                'Cout_2030_MUSD': round(max(0, val_2030), 2),
                'Tendance': tendance
            })
            
    # Exportation des résultats
    df_pred = pd.DataFrame(predictions)
    os.makedirs("outputs", exist_ok=True)
    df_pred.to_csv("outputs/predictions_2030_multi_produits.csv", index=False)
    
    print(f"✅ Terminé ! {len(df_pred)} prédictions générées.")

    # --- NOUVEL APERÇU MULTI-PRODUITS ---
    print("\n🚀 APERÇU DES PROJECTIONS 2030 PAR CATÉGORIE :")
    for prod in df_pred['Produit'].unique():
        print(f"\n--- Top 3 : {prod} ---")
        top_prod = df_pred[df_pred['Produit'] == prod].sort_values(by='Volume_2030_Tonnes', ascending=False).head(3)
        print(top_prod[['Pays', 'Volume_2030_Tonnes', 'Cout_2030_MUSD', 'Tendance']].to_string(index=False))
        
if __name__ == "__main__":
    predict_all_commodities_2030()