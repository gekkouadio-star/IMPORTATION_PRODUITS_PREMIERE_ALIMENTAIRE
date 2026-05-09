import os
import requests
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("COMTRADE_API_KEY")

def fetch_west_africa_full():
    url = "https://comtradeapi.un.org/data/v1/get/C/A/HS"
    
    # 1. Configuration des paramètres (CEDEAO + Mauritanie)
    countries = "204,854,132,384,270,288,324,624,430,466,478,562,434,686,694,768"
    period_blocks = ["2010,2011,2012,2013,2014", "2015,2016,2017,2018,2019", "2020,2021,2022,2023,2024"]
    
    # Dictionnaire des codes SH
    commodities = {
        '1006': 'Riz',
        '10': 'Céréales',
        '03': 'Produits Halieutiques',
        '17': 'Sucre',
        '22': 'Boissons'
    }
    
    all_data = []

    # 2. Boucle sur les produits
    for code, name in commodities.items():
        print(f"\n📦 DEBUT COLLECTE : {name} (Code {code})")
        
        # 3. Boucle sur les périodes
        for block in period_blocks:
            print(f"  📥 Bloc {block}...", end=" ", flush=True)
            params = {
                'reporterCode': countries,
                'period': block,
                'cmdCode': code,
                'flowCode': 'M',
                'partnerCode': '0',
                'subscription-key': API_KEY
            }
            
            try:
                # Ajout d'un timeout pour éviter les blocages infinis
                response = requests.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    batch = response.json().get('data', [])
                    if batch:
                        df_batch = pd.DataFrame(batch)
                        
                        # --- CORRECTION : HARMONISATION DES COLONNES DE POIDS ---
                        # L'API utilise parfois 'netWgt', parfois 'qty', ou rien du tout.
                        # On force la création de 'netWgt' pour ne pas casser le concat final.
                        if 'netWgt' not in df_batch.columns:
                            # On cherche une alternative (certains produits utilisent 'weight')
                            alternative_cols = ['weight', 'qty', 'primaryQuantity']
                            found = False
                            for col in alternative_cols:
                                if col in df_batch.columns:
                                    df_batch['netWgt'] = df_batch[col]
                                    found = True
                                    break
                            if not found:
                                df_batch['netWgt'] = 0 # Valeur par défaut si rien n'est trouvé
                        
                        df_batch['commodity_name'] = name
                        all_data.append(df_batch)
                        print(f"✅ ({len(batch)} lignes)")
                    else:
                        print("📭 (Vide)")
                        
                    # Petite pause pour respecter les limites de l'API
                    time.sleep(2) 
                    
                elif response.status_code == 429:
                    print("\n🛑 Rate limit atteint. Pause de 15 secondes...")
                    time.sleep(15)
                elif response.status_code in [500, 502]:
                    print(f"\n⚠️ Erreur Serveur UN ({response.status_code}). Le bloc est peut-être trop lourd.")
                else:
                    print(f"\n⚠️ Erreur {response.status_code}")
                    
            except Exception as e:
                print(f"\n💥 Erreur réseau : {e}")

    # 4. Sauvegarde finale
    if all_data:
        # On s'assure que toutes les colonnes 'netWgt' sont traitées comme des nombres
        df_total = pd.concat(all_data, ignore_index=True)
        df_total['netWgt'] = pd.to_numeric(df_total['netWgt'], errors='coerce').fillna(0)
        
        output_path = "data/raw/denrees_afrique_ouest.csv"
        os.makedirs("data/raw", exist_ok=True)
        df_total.to_csv(output_path, index=False)
        print(f"\n✨ COLLECTE TERMINÉE : {len(df_total)} lignes enregistrées dans {output_path}")
    else:
        print("\n❌ Échec : Aucune donnée n'a pu être concaténée.")

if __name__ == "__main__":
    fetch_west_africa_full()