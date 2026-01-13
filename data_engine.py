import pandas as pd
import numpy as np

def generate_bcrg_dataset():
    dates = pd.date_range(start='2020-01-01', end='2025-12-01', freq='MS')
    n = len(dates)
    
    # Simulation réaliste : Inflation en baisse, Réserves en hausse, GNF stable
    data = {
        'Date': dates,
        'Inflation': np.linspace(12.5, 5.2, n) + np.random.normal(0, 0.3, n),
        'Reserves_USD': np.linspace(1.6, 2.1, n) + np.random.normal(0, 0.05, n),
        'Taux_USD_GNF': np.linspace(8500, 8750, n) + np.random.normal(0, 20, n),
        'Liquidite_Bancaire': np.random.uniform(95, 120, n),
        'NPL_Ratio': np.linspace(10, 6.5, n) + np.random.normal(0, 0.2, n) # Créances douteuses
    }
    df = pd.DataFrame(data)
    df.to_csv('bcrg_data.csv', index=False)
    print("Base de données BCRG générée avec succès.")

if __name__ == "__main__":
    generate_bcrg_dataset()