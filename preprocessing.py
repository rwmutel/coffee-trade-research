'''
This script was created to generate nice and clean .csv with the data about
coffee trade as of 2019 from raw International Coffee Organization .xlsx data.
It contains comments on some not obvious moments and can be easily scaled for the other years
'''

import pandas as pd

# sourcee files can be loaded both from ico.org or from dataset enclosed
ico_data = [
    # "datasets/2b - Imports.xlsx", 
    # "datasets/2c - Re-exports.xlsx", 
    # "datasets/4b - Disappearance.xlsx", 
    "https://www.ico.org/historical/1990%20onwards/Excel/2b%20-%20Imports.xlsx", 
    "https://www.ico.org/historical/1990%20onwards/Excel/2c%20-%20Re-exports.xlsx", 
    "https://www.ico.org/historical/1990%20onwards/Excel/4b%20-%20Disappearance.xlsx", 
    # "datasets/3a - Prices paid to growers.xlsx",
    # "datasets/3b - Retail prices.xlsx"
]
imports = pd.read_excel(ico_data[0], header=3, usecols="A,AE")\
    .rename(columns={"Calendar years" : "country", "2019" : "imports"})
reexports = pd.read_excel(ico_data[1], header=3, usecols="A,AE")\
    .rename(columns={"Calendar years" : "country", "2019" : "reexports"})
consumption = pd.read_excel(ico_data[2], header=3, usecols="A,AE")\
    .rename(columns={"Calendar years" : "country", "2019" : "consumption"})
# green_coffee_price = pd.read_excel(ico_data[3])
# roasted_coffee_price = pd.read_excel(ico_data[4])

trade_dfs = [imports, reexports, consumption]
for df in trade_dfs:
    df.dropna(how="all", inplace=True)
    # at indexes 1, 4, 33, 39, 40 there are some rows, which does not represent actual state and can be ommited
    df.drop(index=[1, 4, 33, 39, 40], axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    # EU countries have some indentation before them,
    # it is necessary to strip their name to merge this df with population
    df["country"] = df["country"].apply(lambda x: x.strip())

# loading the data about countries population
# NB: the original World Bank was a bit modified for the convinience:
#   Slovak Republic -> Slovakia
#   United States   -> United States of America 
population = pd\
    .read_csv("datasets/Countries_population.csv", header=2, usecols=["Country Name", "2019"], dtype={"2019": "Int64"})\
    .rename(columns={"Country Name": "country", "2019": "population"})

result = pd.merge(population, imports, how="inner", on="country")
result = pd.merge(result, reexports, how="inner", on="country")
result = pd.merge(result, consumption, how="inner", on="country")

# to make the dataframe more compact
result.at[32, "country"] = "United States"

# we are interested in identical random variables, thus we have to divide the 
# amount of coffee by the population to get per capita data
# NB: ICO data is in thousands of coffee bags (each weights 60 kilograms), 
# it would be nice to have the data in more human friendly format - kilograms
result["imports"] = round(result["imports"] * 60 * 1000 / result["population"], 4)
result["reexports"] = round(result["reexports"] * 60 * 1000 / result["population"], 4)
result["consumption"] = round(result["consumption"] * 60 * 1000 / result["population"], 4)
result.drop("population", axis=1, inplace=True)

result.to_csv("datasets/Coffee_Dataset_2019.csv", index=False)