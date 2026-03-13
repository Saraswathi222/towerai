import pandas as pd

days = 1000

makeup = {
    "conductivity": 350,
    "TDS": 230,
    "chloride": 28,
    "sulfate": 25,
    "magnesium": 22,
    "calcium": 60,
    "alkalinity": 110
}

records = []

COC = 2.5

for day in range(days):

    # evaporation increases cycles slowly
    COC += 0.015

    # blowdown when cycles too high
    if COC > 5:
        COC = 3

    conductivity = makeup["conductivity"] * COC
    TDS = conductivity / 1.5

    chloride = makeup["chloride"] * COC
    sulfate = makeup["sulfate"] * COC
    magnesium = makeup["magnesium"] * COC
    calcium = makeup["calcium"] * COC
    alkalinity = makeup["alkalinity"] * COC

    hardness = calcium + magnesium

    pH = 7.2 + (COC * 0.12)

    temperature = 28 + ((day % 30) * 0.1)

    records.append([
        day, pH, conductivity, temperature,
        TDS, chloride, sulfate, magnesium,
        calcium, alkalinity, hardness
    ])

columns = [
    "day","pH","conductivity","temperature",
    "TDS","chloride","sulfate","magnesium",
    "calcium","alkalinity","hardness"
]

df = pd.DataFrame(records, columns=columns)

df.to_csv("cooling_tower_history.csv", index=False)

print("Dataset generated successfully")