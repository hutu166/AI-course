# coding=utf-8
import pandas as pd
data = pd.read_csv("1729256604956007.csv")
print(data.head())
data['Total Value'] = data['Price'] * data['Quantity']
print(data)
