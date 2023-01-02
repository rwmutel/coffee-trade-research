import pandas as pd

ico_data = [
    "datasets/2b - Imports.xlsx", 
    "datasets/2c - Re-exports.xlsx", 
    "datasets/4b - Disappearance.xlsx", 
    "datasets/3a - Prices paid to growers.xlsx",
    "datasets/3b - Retail prices.xlsx"
]

imports = pd.read_excel(ico_data[0], header=3, usecols="A,AE")\
    .rename(columns={"Calendar years" : "country", "2019" : "imports"})\
    .dropna(how="all")\
    .drop(index=[1, 4, 33, 39, 40], axis=0)\
    .reset_index(drop=True)
# reexports = pd.read_excel(ico_data[1])
# consumption = pd.read_excel(ico_data[2])
# green_coffee_price = pd.read_excel(ico_data[3])
# roasted_coffee_price = pd.read_excel(ico_data[4])

# population_= pd.read_csv("Countries_population.csv", skiprows=4)

print(imports)