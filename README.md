# 🏛️ SIPRE : Système Intégré de Pilotage et Résilience
**Solution souveraine de suivi macro-financier pour la République de Guinée.**

![Status](https://img.shields.io/badge/Status-Prototype-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B)

---

## 📋 Présentation
Le **SIPRE** (Système Intégré de Pilotage et Résilience) est un cockpit décisionnel développé pour la **Banque Centrale de la République de Guinée (BCRG)**. Cet outil permet de simuler des chocs économiques mondiaux et d'en visualiser l'impact immédiat sur les équilibres macroéconomiques du pays.

Lien de l'application BCRG - SIPRE | Horizon 2026 · Streamlit


## 🚀 Fonctionnalités Clés
* **Tableau de Bord Interactif (KPI)** : Visualisation en temps réel de l'Inflation IPC, des Réserves de Change, du Taux de Change GNF/USD et de la Liquidité Bancaire.
* **Moteur de Simulation de Chocs** : 
    * Variation du prix de la **Bauxite** (impact sur les réserves).
    * Flux d'**Investissements Étrangers (IDE)**.
    * Ajustement du **Taux Directeur** (politique monétaire).
* **Analyse Régionale Dynamique** : Comparaison de l'efficacité économique par région naturelle avec mise en évidence spécifique (Jaune Drapeau) pour la **Moyenne Guinée**.
* **Module Innovation MNBC** : Suivi des flux pour le futur **Franc Guinéen Numérique (e-GNF)**.
* **Stress Testing** : Analyse de la résilience du système bancaire face aux chocs de liquidité.

## 🛠️ Installation Technique

### 1. Prérequis
* Python 3.9 ou version ultérieure.
* Gestionnaire de paquets `pip`.

### 2. Configuration de l'environnement
```bash
# Accéder au dossier du projet
cd BCRG_INTELLIGENCE

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Windows :
venv\Scripts\activate
# Sur Mac/Linux :
source venv/bin/activate

# Installer les dépendances nécessaires
pip install streamlit pandas plotly statsmodels numpy

# 1. Générer la base de données synthétique
python data_engine.py

# 2. Lancer l'application Streamlit
streamlit run main_app.py
