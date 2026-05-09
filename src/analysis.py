import pandas as pd
import matplotlib.pyplot as plt
import os

def run_economic_analysis():
    input_path = "data/raw/denrees_afrique_ouest.csv"
    output_processed = "data/processed/denrees_afrique_ouest_clean.csv"
    
    if not os.path.exists(input_path):
        print(f"❌ Fichier de données introuvable : {input_path}")
        return

    df = pd.read_csv(input_path)

    countries_map = {
        204: 'Bénin', 854: 'Burkina Faso', 132: 'Cabo Verde', 384: 'Côte d\'Ivoire',
        270: 'Gambie', 288: 'Ghana', 324: 'Guinée', 624: 'Guinée-Bissau',
        430: 'Libéria', 466: 'Mali', 478: 'Mauritanie', 562: 'Niger',
        434: 'Nigeria', 686: 'Sénégal', 694: 'Sierra Leone', 768: 'Togo'
    }
    df['reporterDesc'] = df['reporterCode'].map(countries_map)

    # --- CORRECTION DU NETTOYAGE ---
    # On remplit les poids (netWgt) vides par 0 pour ne pas perdre la donnée de coût
    df['netWgt'] = df['netWgt'].fillna(0)
    
    # On ne supprime que si le PRIX, le PAYS ou le NOM DU PRODUIT manque
    df_clean = df.dropna(subset=['primaryValue', 'reporterDesc', 'commodity_name']).copy()
    
    # Conversions
    df_clean['tonnes'] = df_clean['netWgt'] / 1000
    df_clean['millions_usd'] = df_clean['primaryValue'] / 1_000_000

    # Sauvegarde
    os.makedirs("data/processed", exist_ok=True)
    df_clean.to_csv(output_processed, index=False)

    # --- GÉNÉRATION DES GRAPHIQUES ---
    os.makedirs("outputs", exist_ok=True)
    products = df_clean['commodity_name'].unique()

    for prod in products:
        prod_df = df_clean[df_clean['commodity_name'] == prod]
        
        # Top 5 pays par coût moyen
        avg_costs = prod_df.groupby('reporterDesc')['millions_usd'].mean()
        top_countries = avg_costs.nlargest(5).index.tolist() 

        plt.figure(figsize=(12, 7))
        for c in top_countries:
            # CORRECTION : Ajout du .sort_values('refYear') pour éviter les graphiques en zigzag
            data = prod_df[prod_df['reporterDesc'] == c].groupby('refYear')['millions_usd'].sum().reset_index().sort_values('refYear')
            plt.plot(data['refYear'], data['millions_usd'], marker='o', label=f"{c}", linewidth=2)
        
        plt.title(f"Coût annuel des importations : {prod} (Top 5 Pays)", fontsize=14)
        plt.ylabel("Millions de USD")
        plt.xlabel("Année")
        plt.legend(title="Pays")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"outputs/cout_{prod.replace(' ', '_')}.png")
        plt.close()

    # Graphique Dual Axis
    def plot_dual_axis(country_name, country_code, product_name):
        # CORRECTION : Tri par année ici aussi
        data = df_clean[(df_clean['reporterCode'] == country_code) & 
                        (df_clean['commodity_name'] == product_name)].groupby('refYear').agg({
                            'tonnes': 'sum', 
                            'millions_usd': 'sum'
                        }).reset_index().sort_values('refYear')
        
        if data.empty: return

        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Axe 1 : Volume
        color = 'tab:blue'
        ax1.set_xlabel('Année')
        ax1.set_ylabel('Volume (Tonnes)', color=color)
        # On affiche les barres même si elles sont à 0 (donnée manquante)
        ax1.bar(data['refYear'], data['tonnes'], color=color, alpha=0.3)
        ax1.tick_params(axis='y', labelcolor=color)

        # Axe 2 : Coût
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Coût (Millions USD)', color=color)
        ax2.plot(data['refYear'], data['millions_usd'], color=color, marker='o', linewidth=2)
        ax2.tick_params(axis='y', labelcolor=color)

        plt.title(f"{product_name} : Volume vs Coût au {country_name}")
        fig.tight_layout()
        plt.savefig(f"outputs/dual_{country_name}_{product_name.replace(' ', '_')}.png")
        plt.close()

    # On lance pour les catégories demandées
    for p in products:
        plot_dual_axis("Sénégal", 686, p)
        plot_dual_axis("Côte d'Ivoire", 384, p)

    print(f"✅ Analyse terminée. Les volumes à 0 indiquent des données non déclarées par les douanes.")

if __name__ == "__main__":
    run_economic_analysis()