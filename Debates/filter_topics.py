cp ..import glob
from pathlib import Path
import xml.etree.ElementTree as ET
from collections import defaultdict
from pprint import pp
import pandas as pd

dataset = pd.read_csv("all_debate_text.csv", keep_default_na=False)

keywords = ["strike", "industrial action", "labour dispute", "industrial dispute"]
# this is is to exclude uses of the word strikes that don't meet the topic
anti_keywords = [
    "ukraine",
    "russia",
    "strikes me",
    "strike me",
    "strike a balance",
    "airstrike",
    "missile strike",
    "strike the right balance",
    "strikes the right balance",
    "strike-off",
    "strike up",
    "strike off",
    "strike out",
]
# keywords = ["strike", "industrial action", "labour dispute", "industrial dispute", "trade union", "walkout"]

columns_to_search = ["major_heading", "minor_heading", "text"]

def find_topics(row) -> bool:
    # look for anti keywords at the speech level
    for column in columns_to_search:
        value = row[column].lower()
        for keyword in anti_keywords:
            if keyword in value:
                # if there is an anti-keyword then don't include this
                return False
    for column in columns_to_search:
        value = row[column].lower()
        for keyword in keywords:
            if keyword in value:
                return True
    return False


dataset["matched"] = dataset.apply(find_topics, axis=1)

# print(dataset.head())
print(dataset.shape)

matched_only = dataset[dataset["matched"] == True]
print(matched_only.shape)
matched_only.to_csv("matched_speeches_only.csv", index=False)

# Descriptives
data_overview = matched_only.groupby("current_party").size()
data_overview = data_overview.to_frame()

data_overview.to_csv("debates_overview.csv")