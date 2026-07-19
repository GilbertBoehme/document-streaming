import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data.csv"
OUTPUT_FILE = BASE_DIR / "output.txt"

df = pd.read_csv(INPUT_FILE, encoding="cp1252")
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    format="%m/%d/%y %H:%M",
).dt.strftime("%d/%m/%Y %H:%M")

with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    for row in df.to_dict(orient="records"):
        f.write(json.dumps(row, ensure_ascii=False))
        f.write("\n")
