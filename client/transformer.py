import numpy as np
import pandas as pd

df = pd.read_csv('data.csv', encoding='cp1252')
df["json"] = df.to_json(orient="records", lines=True).splitlines()

df_json = df["json"]
np.savetxt(r'./output.txt', df_json.values, fmt='%s')