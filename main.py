import os
import sys

# Importation des fonctions mises à jour
from src.fetch_data import fetch_west_africa_full
from src.analysis import run_economic_analysis
# Attention : le nom dans le nouveau script est predict_all_commodities_2030
from src.prediction import predict_all_commodities_2030 

def main():
    print("==================================================")
    print("🌍 OBSERVATOIRE DE SÉCURITÉ ALIMENTAIRE (CEDEAO)")
    print("         Analyse & Prédictions 2030")
    print("==================================================\n")

    # ÉTAPE 1 : Collecte des données (Multi-Produits)
    print("🟢 ÉTAPE 1 : Collecte des données sur UN Comtrade...")
    try:
        fetch_west_africa_full() 
    except Exception as e:
        print(f"❌ Erreur lors de la collecte : {e}")
        return

    # ÉTAPE 2 : Nettoyage et Analyse Économique
    print("\n🟢 ÉTAPE 2 : Nettoyage et Analyse des Coûts...")
    try:
        run_economic_analysis()
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse : {e}")
        return

    # ÉTAPE 3 : IA et Prédiction 2030
    print("\n🟢 ÉTAPE 3 : Modélisation IA et Projections 2030...")
    try:
        # Appel de la nouvelle fonction multi-produits
        predict_all_commodities_2030()
    except Exception as e:
        print(f"❌ Erreur lors de la prédiction : {e}")
        return

    print("\n==================================================")
    print("✅ PIPELINE EXÉCUTÉ AVEC SUCCÈS")
    print("🚀 Lancez le dashboard avec : streamlit run dashboard.py")
    print("==================================================")

if __name__ == "__main__":
    main()