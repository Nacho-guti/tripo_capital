import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('uk10y_gilt.xlsx', index_col=0, parse_dates=True)

name = df["Name"].iloc[0]
print(name)

daily_yield = df["Last Price"].iloc[0:]
mean = daily_yield.mean()/100
print(f"Mean: {mean:.2%}")