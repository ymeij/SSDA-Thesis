import glob

from pathlib import Path

import xml.etree.ElementTree as ET
from collections import defaultdict

from pprint import pp

import pandas as pd

dataset = pd.read_csv("strike_debates.csv", keep_default_na=False)
print(dataset.head())

# group by all columns except text
grouped_data = dataset.groupby(by=list(set(dataset.columns)-set(("text",))), axis=0, as_index=False)

pp(grouped_data.head())

agged_data = grouped_data.agg({"text": " ".join})

print(agged_data.head())

agged_data.to_csv("agg_debates.csv", index=False)