import pandas as pd
import os

if __name__ == "__main__":
    parameters = pd.read_excel('.\Parameters.xlsx')
    parameters = parameters.set_index('Simbolo')
    for root, dirs, files in os.walk(".\Simulations"):
        for file in files:
            ticker = file.replace(".xlsx", "")
            filename = os.path.join(root, file)
            df = pd.read_excel(filename)
            df = df.sort_values(by='Total efficency', ascending=False).head(1)
            df['Period'].values[0]
            parameters.loc[ticker]['Periodo'] = df['Period'].values[0]
            parameters.loc[ticker]['SmoothK'] = df['SmoothK'].values[0]
            parameters.loc[ticker]['SmoothD'] = df['SmoothD'].values[0]
            print(df)

    parameters.to_excel('.\Parameters.xlsx')