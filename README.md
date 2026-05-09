# Observatoire de Sécurité Alimentaire - CEDEAO 2030

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)
![IA](https://img.shields.io/badge/Machine_Learning-Scikit--Learn-orange.svg)

## Présentation du Projet
Ce projet est un **Observatoire de données massives** dédié à l'analyse et à la prédiction des flux d'importations alimentaires dans la zone CEDEAO (plus Mauritanie). 

L'outil automatise la collecte de données sur l'API **UN Comtrade**, traite les anomalies douanières et utilise l'**Intelligence Artificielle** (Régression Linéaire) pour projeter les besoins alimentaires et l'impact budgétaire des pays membres à l'horizon **2030**.

### Denrées suivies :
* **Riz** (Code SH 1006)
* **Céréales** (Code SH 10)
* **Produits Halieutiques** (Code SH 03)
* **Sucre** (Code SH 17)
* **Boissons** (Code SH 22)

---

## Fonctionnalités Clés
- **Collecte Automatisée** : Script robuste gérant les limites de taux (Rate Limiting) de l'API UN Comtrade.
- **Data Cleaning Avancé** : Harmonisation des unités de mesure et gestion des déclarations douanières incomplètes.
- **Moteur de Prédiction IA** : Modèle de régression avec système de "Stabilisation" pour corriger les tendances historiques erronées.
- **Dashboard Interactif** : Visualisation professionnelle avec Streamlit permettant de basculer entre analyse volumétrique et impact financier.

---

## Architecture Technique

```text
PROJET_RIZ_AFRIQUE/
├── data/
│   ├── raw/             # Données brutes issues de l'API
│   └── processed/       # Données nettoyées et prêtes pour l'IA
├── src/
│   ├── fetch_data.py    # Collecte via API UN Comtrade
│   ├── analysis.py      # Nettoyage et analyse économique
│   └── prediction.py    # Modèles IA et projections 2030
├── outputs/             # Graphiques exports et fichiers de prédiction
├── main.py              # Orchestrateur du pipeline complet
├── dashboard.py         # Interface utilisateur Streamlit
├── .env                 # Clés API (non inclus dans Git)
└── requirements.txt     # Dépendances du projet
```