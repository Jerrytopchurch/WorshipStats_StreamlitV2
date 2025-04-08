
import pandas as pd
from collections import Counter

def split_names(value):
    if pd.isna(value): return []
    return [n.strip() for n in str(value).split("/") if n.strip() not in ["", "NaN", "暫停"]]

def flatten_people(df):
    melted = df.drop(columns=['聚會名稱', '來源檔案'], errors='ignore')
    names = melted.values.flatten()
    all_names = []
    for cell in names:
        all_names.extend(split_names(cell))
    return Counter(all_names)

def calculate_statistics(df, weights):
    counts = flatten_people(df)
    df_people = pd.DataFrame(counts.items(), columns=["姓名", "總次數"])
    df_people["加權分數"] = df_people["總次數"] * 2  # 簡化版權重

    median = df_people["總次數"].median()
    potential = df_people[(df_people["總次數"] <= median) & (df_people["總次數"] >= 2)].copy()
    heavy = df_people[(df_people["加權分數"] > df_people["加權分數"].quantile(0.9)) | (df_people["總次數"] > 15)].copy()

    return df_people, potential, heavy
