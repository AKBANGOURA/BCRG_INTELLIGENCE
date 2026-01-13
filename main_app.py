import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np
from datetime import datetime

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="BCRG - SIPRE | Horizon 2026",
    page_icon="🏛️",
    layout="wide"
)

# --- 2. STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border-left: 5px solid #CE1126;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stTabs [aria-selected="true"] {
        background-color: #FCD116 !important;
        color: #000 !important;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #009460;
        color: white;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('bcrg_data.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        dates = pd.date_range(start='2020-01-01', periods=60, freq='MS')
        return pd.DataFrame({
            'Date': dates,
            'Inflation': np.random.uniform(8, 12, 60),
            'Reserves_USD': np.random.uniform(1.8, 2.5, 60),
            'Taux_USD_GNF': np.random.uniform(8500, 8700, 60),
            'Liquidite_Bancaire': np.random.uniform(90, 110, 60),
            'NPL_Ratio': np.random.uniform(5, 8, 60)
        })

df = load_data()
latest = df.iloc[-1]

# --- 4. SIDEBAR : PARAMÈTRES ET SIMULATIONS ---
with st.sidebar:
    # Affichage du logo/drapeau (Armoiries de la Guinée)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Coat_of_arms_of_Guinea.svg/500px-Abzeichen_Guinea.svg.png", use_container_width=True)
    
    st.title("Pilotage Stratégique")
    st.markdown("---")
    
    st.subheader("🔮 Projections")
    horizon = st.select_slider("Horizon prévisionnel (Mois)", options=[1, 3, 6, 12], value=3)
    
    st.subheader("🌪️ Facteurs de Stress Externes")
    choc_bauxite = st.slider("Variation Prix Bauxite (%)", -50, 20, 0)
    choc_ide = st.slider("Flux Investissements (IDE) %", -30, 30, 0)
    
    st.subheader("⚙️ Leviers de Politique Monétaire")
    ajust_taux_dir = st.slider("Ajustement Taux Directeur (bps)", -200, 500, 0)
    
    st.markdown("---")
    if st.button("📄 Générer Note de Conjoncture"):
        st.success("Rapport prêt pour le Gouverneur.")

# --- 5. CALCULS D'IMPACT DYNAMIQUE (LOGIQUE MÉTIER) ---
# Impact sur les Réserves (Bauxite + IDE)
impact_res_kpi = latest['Reserves_USD'] * (1 + (choc_bauxite * 0.01) + (choc_ide * 0.005))

# Impact sur le Taux de Change (Pression sur le GNF si les réserves baissent)
pression_change = abs(choc_bauxite) * 4 + abs(choc_ide) * 2
taux_dynamique = latest['Taux_USD_GNF'] + pression_change

# Impact sur l'Inflation (Importée + Politique Monétaire)
# Si on augmente le taux directeur (ajust_taux_dir > 0), on freine l'inflation
effet_monetaire = ajust_taux_dir * 0.001
inflation_dynamique = latest['Inflation'] + (pression_change * 0.006) - effet_monetaire

# --- 6. HEADER ---
st.title("🏛️ BCRG - Système Intégré de Pilote et Résilience (SIPRE)")
st.caption("Interface de supervision souveraine - Direction des Études et DSI")

# --- 7. AFFICHAGE DES KPI INTERACTIFS ---
col1, col2, col3, col4 = st.columns(4)

col1.metric("Inflation IPC", f"{inflation_dynamique:.2f}%", 
           f"{inflation_dynamique - latest['Inflation']:.2f}%", delta_color="inverse")

col2.metric("Réserves de Change", f"{impact_res_kpi:.2f} Mds$", 
           f"{impact_res_kpi - latest['Reserves_USD']:.2f} Mds$", delta_color="normal")

col3.metric("Taux GNF/USD", f"{int(taux_dynamique)}", 
           f"+{int(pression_change)} GNF" if pression_change > 0 else "Stable")

col4.metric("Liquidité Système", f"{latest['Liquidite_Bancaire'] - (ajust_taux_dir/100):.1f}%", 
           f"{-ajust_taux_dir} bps")

st.markdown("---")

# --- 8. ONGLETS ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Analyse Macro", "🛡️ Supervision Bancaire", "🪙 Innovation MNBC", "🌪️ Stress Tests"])

with tab1:
    st.subheader("Projection de l'Inflation (Modèle IA)")
    model = ExponentialSmoothing(df['Inflation'], trend='add', seasonal='add', seasonal_periods=12).fit()
    forecast = model.forecast(horizon)
    # On ajuste la prédiction avec l'inflation dynamique calculée
    forecast = forecast + (inflation_dynamique - latest['Inflation'])
    
    future_dates = pd.date_range(start=df['Date'].iloc[-1], periods=horizon+1, freq='MS')[1:]
    fig_inf = go.Figure()
    fig_inf.add_trace(go.Scatter(x=df['Date'], y=df['Inflation'], name="Historique", line=dict(color='#009460', width=3)))
    fig_inf.add_trace(go.Scatter(x=future_dates, y=forecast, name="Projection ajustée", line=dict(color='#CE1126', dash='dash')))
    st.plotly_chart(fig_inf, use_container_width=True)

with tab2:
    st.subheader("Santé du Secteur Bancaire")
    c_sup1, c_sup2 = st.columns(2)
    with c_sup1:
        fig_liq = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = latest['Liquidite_Bancaire'],
            title = {'text': "Ratio de Liquidité Global (%)"},
            gauge = {'axis': {'range': [0, 150]}, 'bar': {'color': "#FCD116"}}))
        st.plotly_chart(fig_liq, use_container_width=True)
    with c_sup2:
        st.write("### Matrice d'Exposition Interbancaire")
        nodes = ["BCRG", "SGBG", "Ecobank", "UBA", "Vista", "Orabank"]
        matrix = np.random.rand(6,6)
        st.plotly_chart(px.imshow(matrix, x=nodes, y=nodes, color_continuous_scale='Reds'), use_container_width=True)

with tab3:
    st.subheader("🪙 Écosystème e-GNF (Franc Guinéen Numérique)")
    cm1, cm2 = st.columns([2, 1])
    with cm1:
        vol_mnbc = pd.DataFrame({'H': range(24), 'V': np.random.randint(200, 800, 24)})
        st.plotly_chart(px.area(vol_mnbc, x='H', y='V', title="Volume e-GNF (Milliards)", color_discrete_sequence=['#FCD116']), use_container_width=True)
    with cm2:
        st.metric("Adoption Mobile", "18.5%", "+2.1%")
        st.info("Le Ledger National est synchronisé sur 12 nœuds certifiés.")

with tab4:
    st.subheader("Analyse de Résilience (Stress Test)")
    if choc_bauxite < -30 or impact_res_kpi < 1.5:
        st.error(f"ALERTE : Les réserves tombent à {impact_res_kpi:.2f} Mds$. Seuil de sécurité critique !")
    else:
        st.success("Le système absorbe actuellement le choc sans rupture de convertibilité.")
    
    fig_choc = go.Figure(go.Bar(
        x=["Actuel", "Simulé"], y=[latest['Reserves_USD'], impact_res_kpi],
        marker_color=['#009460', '#CE1126']))
    st.plotly_chart(fig_choc, use_container_width=True)

st.markdown("---")
st.markdown("<center>🏛️ <b>Projet SIPRE-BCRG</b> | Développé pour la Direction des Systèmes d'Information</center>", unsafe_allow_html=True)