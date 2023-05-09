from pathlib import Path
from pprint import pp
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates
import numpy as np

# Import data
# THIS DATA CONTAINS THE BODY OF THE TEXT AND IS THEREFORE NOT AVAILABLE 
# THE CODE HAS BEEN PROVIDED TO UNDERSTAND THE FILTERING
data = pd.read_csv("newspaper_sentiments_NEW.csv", keep_default_na=False)
print(data.shape)

# make sure newspaper dates are dates
data["published_date"] = data["published_date"].astype("datetime64[ns]")

# fix newspaper names
data = data.replace(
    {
        "newspaper_line": {
            "MAIL ON SUNDAY (London)": "Daily Mail and Mail on Sunday",
            "DAILY MAIL (London)": "Daily Mail and Mail on Sunday",
            "Mail on Sunday (London)": "Daily Mail and Mail on Sunday",
            "The Independent (United Kingdom)": "The Independent",
            "The Independent - Daily Edition": "The Independent",
            "Metro (UK)": "Metro",
            "The Daily Telegraph (London)": "The Daily Telegraph",
            "The Guardian (London)": "The Guardian",
            "The Sun (England)": "The Sun",
            "The Sunday Times (London)": "The Times and The Sunday Times",
            "The Times (London)": "The Times and The Sunday Times",
        }
    }
)

# removing more duplicates for the independent based only on body
data_filtered = data.drop_duplicates(subset=["body"])

# removing articles that mention the word football 
anti_keywords = ["football"]
columns_to_search = ["body"]

def find_topics(row) -> bool:
    # look for anti keywords at the speech level
    for column in columns_to_search:
        value = row[column].lower()
        for keyword in anti_keywords:
            if keyword in value:
                # if there is an anti-keyword then don't include this
                return False
            return True

data_filtered["matched"] = data_filtered.apply(find_topics, axis=1)

print(data_filtered.shape)

data_matched = data_filtered[data_filtered["matched"] == True]
print(data_matched.shape)

data_overview = data_matched.groupby(["newspaper_line"]).size()

print(data_overview)

# agg
data_agg = data_matched.replace(
    {
        "newspaper_line": {
            "Daily Mail and Mail on Sunday": "Right-wing",
            "Daily Mirror": "Left-wing",
            "The Independent": "Centre",
            "Metro": "Centre",
            "The Daily Telegraph": "Right-wing",
            "The Guardian": "Left-wing",
            "The Sun": "Right-wing",
            "The Times and The Sunday Times": "Right-wing",
        }
    }
)

data_agg = data_agg.rename(columns={"newspaper_line": "newspaper_ideo"})

print("VIEWING ARTICLES PER IDEOLOGOY")
data_agg_grouped = data_agg.groupby(["newspaper_ideo", "label"]).size()
print(data_agg_grouped)

# Overview per newspaper overall
articles_overview = data.pivot_table(
    columns=["label"],
    index=["newspaper_line"],
    aggfunc="size",
    fill_value=0,
)

# Aggregate data by date
articles_per_date = data.pivot_table(
    columns=["label"],
    index=["published_date"],
    aggfunc="size",
    fill_value=0,
)
articles_per_date.reset_index(inplace=True)
print("How many newspaper articles per date")
print(articles_per_date.head())

articles_per_date.to_csv("news_sent_over_time.csv", index=False)


# Then split by newspaper
# create a date range with missing dates
date_range = pd.date_range(
    start=data["published_date"].min(), end=data["published_date"].max()
)
newspapers = pd.DataFrame({"newspaper_line": data["newspaper_line"].unique()})

print(f"{len(newspapers) = }")

# create a dataframe with the date range
date_newspaper_range_df = pd.DataFrame({"published_date": date_range})

date_newspaper_combo = date_newspaper_range_df.merge(newspapers, how="cross")

# merge dataframes to include all dates
newspaper_df = pd.merge(
    date_newspaper_combo, data, on=["published_date", "newspaper_line"], how="outer"
)
print(newspaper_df.shape)
print(newspaper_df.head())

# fill missing values with 0
newspaper_df["label"] = newspaper_df["label"].fillna("NaN")

# pivot
articles_per_date_newspapers = newspaper_df.pivot_table(
    columns=["label"],
    index=["published_date", "newspaper_line"],
    aggfunc="size",
    fill_value=0,
)

# finalise
articles_per_date_newspapers.reset_index(inplace=True)
articles_per_date_newspapers = articles_per_date_newspapers.drop(columns="NaN")
print("Viewing articles per date per newspaper")
print(articles_per_date_newspapers.head())
print(articles_per_date_newspapers.shape)

articles_per_date_newspapers.to_csv("sent_over_time_per_newspaper.csv", index=False)