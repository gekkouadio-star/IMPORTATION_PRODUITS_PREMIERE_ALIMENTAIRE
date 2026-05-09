import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURATION ---
st.set_page_config(page_title="Observatoire Alimentaire CEDEAO", layout="wide")

# --- STYLE PROFESSIONNEL (CSS) ---
st.markdown("""
    <style>
    .main-title {
        color: #1E3A8A;
        background-color: #F0F4F8;
        padding: 20px;
        border-radius: 10px;
        border-left: 10px solid #1E3A8A;
        text-align: center;
        margin-bottom: 25px;
    }
    .project-header {
        font-size: 14px;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0px;
    }
    </style>
    <div class="main-title">
        <p class="project-header">PROJET PROFESSIONNEL • DATA SCIENCE & ANALYTICS</p>
        <h1>OBSERVATOIRE DE LA SÉCURITÉ ALIMENTAIRE : AFRIQUE DE L'OUEST</h1>
        <p>Analyse Prédictive des Flux d'Importations des Denrées Stratégiques (Horizon 2030)</p>
    </div>
    """, unsafe_allow_html=True)

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/denrees_afrique_ouest_clean.csv")
    df_pred = pd.read_csv("outputs/predictions_2030_multi_produits.csv")
    return df, df_pred

try:
    df, df_pred = load_data()
except FileNotFoundError:
    st.error("Les fichiers de données sont introuvables. Veuillez lancer 'python main.py' d'abord.")
    st.stop()

# --- NAVIGATION SIDEBAR ---
st.sidebar.title("Dashboard")
page = st.sidebar.radio("Aller vers :", ["Évolution par pays", "Prédictions 2030", "Analyse Comparative"])

st.sidebar.divider()

# --- FILTRES GLOBAUX ---
available_products = df['commodity_name'].unique()
selected_product = st.sidebar.selectbox("Choisir un produit :", available_products)

available_countries = df[df['commodity_name'] == selected_product]['reporterDesc'].unique()
selected_country = st.sidebar.selectbox("Choisir un pays :", available_countries)

df_filtered = df[(df['reporterDesc'] == selected_country) & (df['commodity_name'] == selected_product)]
df_pred_filtered = df_pred[(df_pred['Pays'] == selected_country) & (df_pred['Produit'] == selected_product)]

# ---------------------------------------------------------
# PARTIE 1 : ÉVOLUTION DES PAYS
# ---------------------------------------------------------
if page == "Évolution par pays":
    st.header(f"{selected_product} : Analyse Historique au {selected_country}")
    
    data_plot = df_filtered.groupby('refYear').agg({'tonnes': 'sum', 'millions_usd': 'sum'}).reset_index()
    data_plot = data_plot.sort_values('refYear')
    
    if not data_plot.empty:
        c1, c2 = st.columns(2)
        last_vol = data_plot['tonnes'].iloc[-1]
        last_val = data_plot['millions_usd'].iloc[-1]
        
        if last_vol > 0:
            c1.metric(f"Dernier Volume ({int(data_plot['refYear'].iloc[-1])})", f"{int(last_vol):,} T".replace(',', ' '))
        else:
            c1.metric(f"Dernier Volume ({int(data_plot['refYear'].iloc[-1])})", "Non déclaré")
            
        c2.metric("Dernière Facture (M$)", f"{last_val:.2f} M$")

        st.divider()
        
        st.subheader("Corrélation entre Volume Physique et Coût d'Importation")
        fig = go.Figure()
        
        # AJOUT DES ÉTIQUETTES SUR LES BARRES (Volume)
        fig.add_trace(go.Bar(
            x=data_plot['refYear'], 
            y=data_plot['tonnes'], 
            name="Volume (Tonnes)", 
            marker_color='#00CC96',
            text=data_plot['tonnes'].apply(lambda x: f"{int(x):,} T" if x > 0 else ""),
            textposition='outside'
        ))
        
        fig.add_trace(go.Scatter(
            x=data_plot['refYear'], 
            y=data_plot['millions_usd'], 
            name="Coût (M$)", 
            yaxis="y2", 
            line=dict(color='red', width=3),
            mode='lines+markers+text',
            text=data_plot['millions_usd'].apply(lambda x: f"{x:.1f}M$"),
            textposition='top center'
        ))

        fig.update_layout(
            yaxis=dict(title="Volume en Tonnes"),
            yaxis2=dict(title="Coût en Millions USD", overlaying="y", side="right"),
            legend=dict(x=0, y=1.2, orientation="h"),
            template="plotly_white",
            xaxis=dict(tickmode='linear'),
            margin=dict(t=100) # Espace pour les étiquettes du haut
        )
        st.plotly_chart(fig, width='stretch')
    else:
        st.warning("Données insuffisantes pour ce produit dans ce pays.")

# ---------------------------------------------------------
# PARTIE 2 : PRÉDICTIONS 2030
# ---------------------------------------------------------
elif page == "Prédictions 2030":
    st.header(f"Projections IA Horizon 2030 : {selected_product}")
    
    if not df_pred_filtered.empty:
        pred_row = df_pred_filtered.iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            vol_2030 = int(pred_row['Volume_2030_Tonnes'])
            if vol_2030 > 0:
                st.metric("Besoin Prévu (2030)", f"{vol_2030:,} T".replace(',', ' '))
            else:
                st.metric("Besoin Prévu (2030)", "N/A (Poids non déclaré)")
            st.write(f"Tendance projetée : **{pred_row['Tendance']}**")
            
        with col2:
            st.metric("Impact Budgétaire Estimé (2030)", f"{pred_row['Cout_2030_MUSD']:.2f} M$")
            st.info("Note stratégique : La prédiction financière est basée sur la valeur transactionnelle agrégée.")

        st.subheader("Trajectoire Prévisionnelle")
        hist_df = df_filtered.groupby('refYear')['tonnes'].sum().reset_index().sort_values('refYear')
        
        fig_pred = go.Figure()
        fig_pred.add_trace(go.Scatter(
            x=hist_df['refYear'], y=hist_df['tonnes'],
            mode='lines+markers', name='Données Réelles',
            line=dict(color='#1f77b4', width=3)
        ))

        last_year = hist_df['refYear'].iloc[-1]
        last_val = hist_df['tonnes'].iloc[-1]
        
        fig_pred.add_trace(go.Scatter(
            x=[last_year, 2030],
            y=[last_val, pred_row['Volume_2030_Tonnes']],
            mode='lines+markers+text', 
            name='Projection IA',
            line=dict(color='red', width=3, dash='dash'),
            text=["", f"{int(pred_row['Volume_2030_Tonnes']):,} T"],
            textposition="top right"
        ))
        
        fig_pred.update_layout(
            template="plotly_white", 
            xaxis=dict(title="Année", range=[2009, 2031]),
            yaxis=dict(title="Volume (Tonnes)")
        )
        st.plotly_chart(fig_pred, width='stretch')
    else:
        st.warning("Modèle de prédiction non disponible pour cette sélection.")

# ---------------------------------------------------------
# PARTIE 3 : ANALYSE COMPARATIVE
# ---------------------------------------------------------
else:
    st.header(f"Analyse Comparative Régionale : {selected_product}")
    st.markdown(f"Benchmark des projections 2030 au sein de l'espace CEDEAO.")

    critere = st.radio("Sélectionner l'indicateur de performance :", ["Coût (Millions USD)", "Volume (Tonnes)"], horizontal=True)
    
    y_axis = 'Volume_2030_Tonnes' if critere == "Volume (Tonnes)" else 'Cout_2030_MUSD'
    suffixe = " T" if critere == "Volume (Tonnes)" else " M$"
    
    comp_df = df_pred[df_pred['Produit'] == selected_product].sort_values(y_axis, ascending=False)

    if not comp_df.empty:
        # AJOUT DES ÉTIQUETTES SUR CHAQUE BARRE
        fig_comp = px.bar(
            comp_df, 
            x='Pays', 
            y=y_axis, 
            color=y_axis,
            text=comp_df[y_axis].apply(lambda x: f"{x:,.0f}{suffixe}".replace(',', ' ')),
            color_continuous_scale='Viridis',
            title=f"Répartition régionale prévue en 2030 ({critere})"
        )
        
        fig_comp.update_traces(textposition='outside')
        fig_comp.update_layout(margin=dict(t=50))
        
        st.plotly_chart(fig_comp, width='stretch')
        
        if critere == "Volume (Tonnes)" and comp_df[y_axis].sum() == 0:
            st.warning("Absence de données volumétriques pour ce produit. Veuillez consulter l'indicateur 'Coût'.")
    else:
        st.error("Données comparatives non générées.")