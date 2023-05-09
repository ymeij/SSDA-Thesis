import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly
import seaborn as sns
from plotly.subplots import make_subplots

# import dataframe
df = pd.read_csv("debates_sentiments_NEW.csv", keep_default_na=False)

df["date"] = pd.to_datetime(df["date"])

print(df.shape)

# create a date range with missing dates
end_date = pd.to_datetime("2023-02-20")
date_range = pd.date_range(start=df["date"].min(), end=df["date"].max())

# create a dataframe with the date range
date_range_df = pd.DataFrame({"date": date_range})

# merge dataframes to include all dates
merged_df = pd.merge(date_range_df, df, on="date", how="outer")
print(merged_df.shape)
print(merged_df.head())

# fill missing values with 0
merged_df["label"] = merged_df["label"].fillna("NaN")
# set party
merged_df["current_party"] = merged_df["current_party"].fillna("NaN")

# filter for max date of the newspapers: 20 Feb 2023
merged_df=merged_df[merged_df['date'] <= end_date]

# print the final dataframe
print(merged_df.head())
print(merged_df.shape)
# max date in df
print(merged_df["date"].max())

# pivot
speeches_per_date = merged_df.pivot_table(
    columns=["label"], index=["date"], aggfunc="size", fill_value=0
)

speeches_per_date.reset_index(inplace=True)
speeches_per_date = speeches_per_date.drop(columns="NaN")
print("Viewing speeches per date")
print(speeches_per_date.head())
print(speeches_per_date.shape)

#save
speeches_per_date.to_csv("speeches_per_date.csv", index=False)

# speeches per party
# pivot
speeches_per_party = merged_df.pivot_table(
    columns=["label"], index=["current_party"], aggfunc="size", fill_value=0
)

speeches_per_party.reset_index(inplace=True)
speeches_per_party = speeches_per_party.drop(columns="NaN")
print("Viewing speeches per party")
print(speeches_per_party)

# speeches per MP
# pivot
speeches_per_mp = merged_df.groupby("current_party")["speaker"]. nunique()

print("Viewing unique MPs")
print(speeches_per_mp)


# split by party
## add missing values
# create a date range with missing dates
parties = pd.DataFrame({"current_party": df["current_party"].unique()})

print(f"{len(parties) = }")

# create a dataframe with the date range
date_party_range_df = pd.DataFrame({"date": date_range})

date_party_combo = date_party_range_df.merge(parties, how="cross")

# merge dataframes to include all dates
party_df = pd.merge(date_party_combo, df, on=["date", "current_party"], how="outer")
party_df=party_df[party_df['date'] <= end_date]
print(party_df.shape)
print(party_df.head())

# fill missing values with 0
party_df["label"] = party_df["label"].fillna("NaN")

# pivot
speeches_per_date_party = party_df.pivot_table(
    columns=["label"], index=["date", "current_party"], aggfunc="size", fill_value=0
)

# finalise
speeches_per_date_party.reset_index(inplace=True)
speeches_per_date_party = speeches_per_date_party.drop(columns="NaN")
#rename snp and libdem as centre
speeches_per_date_party = speeches_per_date_party.replace(
    {
        "current_party": {
            "Liberal Democrat": "Centre",
            "Scottish National Party": "Centre"
        }
    }
)
#drop parties we dont care about
speeches_per_date_party = speeches_per_date_party[
    (speeches_per_date_party["current_party"] == "Labour")
    | (speeches_per_date_party["current_party"] == "Conservative") 
    | (speeches_per_date_party["current_party"] == "Centre")
]

speeches_per_date_party = speeches_per_date_party.groupby(['date', 'current_party']).agg({'POSITIVE': 'sum',
                                                             'NEGATIVE': 'sum'}).reset_index()

print("Viewing speeches per date per party")
print(speeches_per_date_party.head())
print(speeches_per_date_party.shape)

speeches_per_date_party.to_csv("speeches_per_date_party.csv", index=False)

speeches_per_date_party=speeches_per_date_party[speeches_per_date_party['date'] <= end_date]

## visualise with px
fig2 = px.line(speeches_per_date_party, x="date", y="NEGATIVE", color="current_party",
               title="Number of Negative Speeches over Time by Party",
               labels={
                     "date": "Date",
                     "NEGATIVE": "Number of Negative Speeches",
                     "current_party": "Party of the Speaker"
                 },
                 template="plotly_white",
                 color_discrete_sequence=['#115DA8', '#E4003B','#FDBB30'],
                 )
fig2.update_yaxes(showline=True, linewidth=1, linecolor='black')
fig2.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig2.update_layout(yaxis = dict(tickfont=dict(family="Arial, sans-serif", size=14)),
                   xaxis = dict(tickfont=dict(family="Arial, sans-serif", size=14)))
fig2.update_traces(line=dict(width=1))
fig2.show()

#positive data 
fig3 = px.line(speeches_per_date_party, x="date", y="POSITIVE", color="current_party",
               title="Number of Positive Speeches over Time by Party",
               labels={
                     "date": "Date",
                     "POSITIVE": "Number of Positive Speeches",
                     "current_party": "Party of the Speaker"
                 },
                 template="plotly_white",
                 color_discrete_sequence=['#115DA8', '#E4003B','#FDBB30'],
                 )
fig3.update_yaxes(showline=True, linewidth=1, linecolor='black')
fig3.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig3.update_layout(yaxis = dict(tickfont=dict(family="Arial, sans-serif", size=14)),
                   xaxis = dict(tickfont=dict(family="Arial, sans-serif", size=14)))
fig3.update_traces(line=dict(width=1))
fig3.show()


# filter the two seperate time periods
start_summer = pd.to_datetime("2022-05-30")
end_summer = pd.to_datetime("2022-08-01")
summer_22 = speeches_per_date_party[(speeches_per_date_party['date'] >= start_summer) & (speeches_per_date_party['date'] <= end_summer)]

start_winter = pd.to_datetime("2022-11-30")
end_winter = pd.to_datetime("2023-02-10")
end_23_early_23 = speeches_per_date_party[(speeches_per_date_party['date'] >= start_winter) & (speeches_per_date_party['date'] <= end_winter)]

# viz summer pos
fig4 = px.line(summer_22, x="date", y="POSITIVE", color="current_party",
               title="Number of Positive Speeches over Time by Party during Summer 2022",
               labels={
                     "date": "Date",
                     "POSITIVE": "Number of Positive Speeches",
                     "current_party": "Party of the Speaker"
                 },
                 template="plotly_white",
                 color_discrete_sequence=['#115DA8', '#E4003B','#FDBB30'],
                 )
fig4.update_yaxes(showline=True, linewidth=1, linecolor='black')
fig4.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig4.update_layout(yaxis = dict(tickfont=dict(family="Arial, sans-serif", size=14)),
                   xaxis = dict(tickfont=dict(family="Arial, sans-serif", size=14)))
fig4.update_traces(line=dict(width=1.8))
fig4.show()

# neg viz summer
fig5 = px.line(summer_22, x="date", y="NEGATIVE", color="current_party",
               title="Number of Negative Speeches over Time by Party during Summer 2022",
               labels={
                     "date": "Date",
                     "POSITIVE": "Number of Negative Speeches",
                     "current_party": "Party of the Speaker"
                 },
                 template="plotly_white",
                 color_discrete_sequence=['#115DA8', '#E4003B','#FDBB30'],
                 )
fig5.update_yaxes(showline=True, linewidth=1, linecolor='black')
fig5.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig5.update_layout(yaxis = dict(tickfont=dict(family="Arial Black", size=14)),
                   xaxis = dict(tickfont=dict(family="Arial Black", size=14)))
fig5.update_traces(line=dict(width=1.8))
fig5.show()
