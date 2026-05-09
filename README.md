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

## Insights Stratégiques (Projections 2030)

L'analyse des données massives révèle des pôles de dépendance critique dans la zone CEDEAO :

### 🌾 Top Importateurs : Riz & Céréales
* **Bénin** : Se positionne comme le premier hub d'importation avec une projection dépassant les **7,5M de tonnes** de riz, confirmant son rôle de plateforme de réexportation régionale.
* **Sierra Leone & Ghana** : Présentent une croissance linéaire forte, signalant un besoin urgent de renforcement des politiques d'autosuffisance locale.

### Impact Budgétaire (Toutes denrées)
* **Facture Globale** : Le coût des importations pour le riz seul au Bénin pourrait atteindre **3,7 milliards USD** d'ici 2030.
* **Produits Transformés** : Pour le **Sucre** et les **Boissons**, le Togo et la Côte d'Ivoire affichent les trajectoires de dépenses les plus volatiles, nécessitant une surveillance accrue de l'inflation importée.

> **Note :** Les volumes à "0" pour certaines catégories (Sucre, Boissons) soulignent un manque de déclaration des poids par les douanes nationales, déplaçant l'indicateur de performance vers la **valeur monétaire (M$)** pour ces produits.