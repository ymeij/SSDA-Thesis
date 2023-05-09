import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly
from plotly.subplots import make_subplots

data = pd.read_csv("sent_over_time_per_newspaper.csv", keep_default_na=False)
data.rename({"published_date": "date"}, inplace=True, axis=1)
data["date"] = pd.to_datetime(data["date"])
print(data.shape)

# aggregate based on political alignment
data_agg = data.replace(
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
data_agg = data_agg.groupby(['date', 'newspaper_ideo']).agg({'POSITIVE': 'sum',
                                                             'NEGATIVE': 'sum'}).reset_index()


print(data_agg.shape)
print(data_agg.head())

#data_agg.to_csv("news_ideo_over_time.csv", index=False)

#################################--news ideology one period-##############################################
# sub
df_right = data_agg[data_agg['newspaper_ideo'] == "Right-wing"]
df_left = data_agg[data_agg['newspaper_ideo'] == "Left-wing"]
df_cen = data_agg[data_agg['newspaper_ideo'] == "Centre"]

fig1 = make_subplots(rows=2, cols=1, vertical_spacing = 0.09,
                    subplot_titles=("Positive Articles", "Negative Articles")
                    )
fig1.add_trace(
    go.Scatter(
            x=df_cen["date"],
            y=df_cen["POSITIVE"],
            line_color='#FDBB30',
            name="Centre",
            showlegend=False,
            line=dict(width=1),
        ),
    row=1, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df_right["date"],
            y=df_right["POSITIVE"],
            line_color='#115DA8',
            name="Right-wing",
            showlegend=False,
            line=dict(width=1)
        ),
    row=1, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df_left["date"],
            y=df_left["POSITIVE"],
            line_color='#E4003B',
            name="Left-wing",
            showlegend=False,
            line=dict(width=1)
        ),
    row=1, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df_cen["date"],
            y=df_cen["NEGATIVE"],
            line_color='#FDBB30',
            line=dict(width=1),
            name='Centre'
        ),
    row=2, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df_right["date"],
            y=df_right["NEGATIVE"],
            line_color='#115DA8',
            line=dict(width=1),
            name="Right-wing"
        ),
    row=2, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df_left["date"],
            y=df_left["NEGATIVE"],
            line_color='#E4003B',
            line=dict(width=1),
            name="Left-wing"
        ),
    row=2, col=1
)

fig1.update_xaxes(dict(
        title="Date",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14),
        automargin=False,
        title_standoff = 0.05
    ), row=1, col=1)
fig1.update_xaxes(dict(
        title="Date",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14),
        automargin=False,
        title_standoff = 0.05
    ), row=2, col=1)
fig1.update_yaxes(dict(
        title="Number of Articles",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14),
        range=[0, 30]
    ), row=1, col=1)
fig1.update_yaxes(dict(
        title="Number of Articles",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14),
        #range=[0, 30]
    ), row=2, col=1)

fig1.update_layout(height=1000, width=900, 
                  title_text="Positive and Negative Articles by Newspaper Ideology",
                  template="simple_white",
                  titlefont=dict(family="Arial, sans-serif", size=18),
                  legend = dict(font = dict(size = 14)))

fig1.update_annotations(dict(font_size=16, font_family="Arial"))

fig1.show()
fig1.write_html("pos_neg_articles.html")

##################################--split by period--##########################################

# filter the two seperate time periods
start_summer = pd.to_datetime("2022-05-30")
end_summer = pd.to_datetime("2022-08-01")
summer_22 = data_agg[(data_agg['date'] >= start_summer) & (data_agg['date'] <= end_summer)]

start_winter = pd.to_datetime("2022-11-20")
end_winter = pd.to_datetime("2023-02-10")
end_22_early_23 = data_agg[(data_agg['date'] >= start_winter) & (data_agg['date'] <= end_winter)]


# sub summer
df_right_summer = summer_22[summer_22['newspaper_ideo'] == "Right-wing"]
df_left_summer = summer_22[summer_22['newspaper_ideo'] == "Left-wing"]
df_cen_summer = summer_22[summer_22['newspaper_ideo'] == "Centre"]

# sub winter
df_right_winter = end_22_early_23[end_22_early_23['newspaper_ideo'] == "Right-wing"]
df_left_winter = end_22_early_23[end_22_early_23['newspaper_ideo'] == "Left-wing"]
df_cen_winter = end_22_early_23[end_22_early_23['newspaper_ideo'] == "Centre"]


# colours
colour_map = {'Conservative':'#115DA8', 'Labour': '#E4003B', 'Centre': '#FDBB30'}

# visualise with plotly.go
layout1 = go.Layout(
    title="Number of Pos/Neg Articles over Time",
    titlefont=dict(family="Arial, sans-serif", size=20),
    plot_bgcolor="#FFF",  # Sets background color to white
    xaxis=dict(
        title="Date",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=18),
        tickfont=dict(family="Arial, sans-serif", size=14),
    ),
    yaxis=dict(
        title="Number of Articles",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=18),
        tickfont=dict(family="Arial, sans-serif", size=14),
    ),
    template="simple_white",
)

fig = make_subplots(rows=2, cols=2, horizontal_spacing = 0.08, vertical_spacing = 0.12,
                    subplot_titles=("Positive Articles during Summer 2022", "Negative Articles during Summer 2022", 
                                                    "Positive Articles during Winter 22-23", "Negative Articles during Winter 22-23"),
                    row_heights=[0.5,0.5,]
                    )

fig.add_trace(
    go.Scatter(
            x=df_cen_summer["date"],
            y=df_cen_summer["POSITIVE"],
            line_color='#FDBB30',
            name="Centre",
            showlegend=False,
            line=dict(width=1)
        ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
            x=df_right_summer["date"],
            y=df_right_summer["POSITIVE"],
            line_color='#115DA8',
            name="Right-wing",
            showlegend=False,
            line=dict(width=1)
        ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
            x=df_left_summer["date"],
            y=df_left_summer["POSITIVE"],
            line_color='#E4003B',
            name="Left-wing",
            showlegend=False,
            line=dict(width=1)
        ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
            x=df_cen_summer["date"],
            y=df_cen_summer["NEGATIVE"],
            name="Centre",
            line_color='#FDBB30',
            line=dict(width=1)
        ),
    row=1, col=2
)

fig.add_trace(
    go.Scatter(
            x=df_right_summer["date"],
            y=df_right_summer["NEGATIVE"],
            name="Right-wing",
            line_color='#115DA8',
            line=dict(width=1)
        ),
    row=1, col=2
)

fig.add_trace(
    go.Scatter(
            x=df_left_summer["date"],
            y=df_left_summer["NEGATIVE"],
            name="Left-wing",
            line_color='#E4003B',
            line=dict(width=1)
        ),
    row=1, col=2
)

fig.add_trace(
    go.Scatter(
            x=df_cen_winter["date"],
            y=df_cen_winter["POSITIVE"],
            line_color='#FDBB30',
            name="Centre",
            showlegend=False,
            line=dict(width=1)
        ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
            x=df_right_winter["date"],
            y=df_right_winter["POSITIVE"],
            line_color='#115DA8',
            name="Right-wing",
            showlegend=False,
            line=dict(width=1)
        ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
            x=df_left_winter["date"],
            y=df_left_winter["POSITIVE"],
            line_color='#E4003B',
            name="Left-wing",
            showlegend=False,
            line=dict(width=1)
        ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
            x=df_cen_winter["date"],
            y=df_cen_winter["NEGATIVE"],
            name="Centre",
            line_color='#FDBB30',
            showlegend=False,
            line=dict(width=1)
        ),
    row=2, col=2
)

fig.add_trace(
    go.Scatter(
            x=df_right_winter["date"],
            y=df_right_winter["NEGATIVE"],
            line_color='#115DA8',
            name="Right-wing",
            showlegend=False,
            line=dict(width=1)
        ),
    row=2, col=2
)

fig.add_trace(
    go.Scatter(
            x=df_left_winter["date"],
            y=df_left_winter["NEGATIVE"],
            line_color='#E4003B',
            name="Left-wing",
            showlegend=False,
            line=dict(width=1)
        ),
    row=2, col=2
)

fig.update_xaxes(dict(
        title="Date",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14, color='black'),
        automargin=False,
        tickformat='%d %b %y',
        title_standoff = 0.05
    ), row=1, col=1)
fig.update_xaxes(dict(
        title="Date",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14, color='black'),
        automargin=False,
        tickformat='%d %b %y',
        title_standoff = 0.05
    ), row=1, col=2)
fig.update_yaxes(dict(
        title="Number of Articles",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14, color='black'),
        range=[0,25]
    ), row=1, col=1)
fig.update_yaxes(dict(
        title="Number of Articles",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14,  color='black'),
        #range=[0,25]
    ), row=1, col=2)
fig.update_xaxes(dict(
        title="Date",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14, color='black'),
        title_standoff = 2,
        tickformat='%d %b %y',
        automargin=False
    ), row=2, col=1)
fig.update_xaxes(dict(
        title="Date",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14, color='black'),
        title_standoff = 2,
        tickformat='%d %b %y',
        automargin=False
    ), row=2, col=2)
fig.update_yaxes(dict(
        title="Number of Articles",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14, color='black'),
        range=[0,30]
    ), row=2, col=1)
fig.update_yaxes(dict(
        title="Number of Articles",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14, color='black'),
        #range=[0,30]
    ), row=2, col=2)

fig.update_layout(height=800, width=1200, 
                  title_text="Positive and Negative Articles by Newspaper Ideology",
                  template="simple_white",
                  titlefont=dict(family="Arial, sans-serif", size=18),
                  legend = dict(font = dict(size = 14)))

fig.update_annotations(dict(font_size=16, font_family="Arial"))

fig.show()
fig1.write_html("pos_neg_articles_zoomed.html")