import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly
import seaborn as sns
from plotly.subplots import make_subplots

# import dataframe
df = pd.read_csv("speeches_per_date_party.csv", keep_default_na=True)
df["date"] = pd.to_datetime(df["date"])

print(df.head())

end_date = pd.to_datetime("2023-02-20")

df=df[df['date'] <= end_date]
##################################--one period--###############################################
# sub
df_con = df[df['current_party'] == "Conservative"]
df_lab = df[df['current_party'] == "Labour"]
df_cen = df[df['current_party'] == "Centre"]

fig1 = make_subplots(rows=2, cols=1, vertical_spacing = 0.09,
                    subplot_titles=("Positive Speeches", "Negative Speeches")
                    )

fig1.add_trace(
    go.Scatter(
            x=df_con["date"],
            y=df_con["POSITIVE"],
            line_color='#115DA8',
            showlegend=False,
            line=dict(width=1),
            name="Conservative"
        ),
    row=1, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df_lab["date"],
            y=df_lab["POSITIVE"],
            line_color='#E4003B',
            showlegend=False,
            line=dict(width=1),
            name="Labour"
        ),
    row=1, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df_cen["date"],
            y=df_cen["POSITIVE"],
            line_color='#FDBB30',
            showlegend=False,
            line=dict(width=1),
            name="Centre"
        ),
    row=1, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df_con["date"],
            y=df_con["NEGATIVE"],
            line_color='#115DA8',
            line=dict(width=1),
            name="Conservative"
        ),
    row=2, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df_lab["date"],
            y=df_lab["NEGATIVE"],
            line_color='#E4003B',
            line=dict(width=1),
            name="Labour"
        ),
    row=2, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df_cen["date"],
            y=df_cen["NEGATIVE"],
            line_color='#FDBB30',
            line=dict(width=1),
            name="Centre"
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
        title="Number of Speeches",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14),
        range=[0,80]
    ), row=1, col=1)
fig1.update_yaxes(dict(
        title="Number of Speeches",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14),
        range=[0,80]
    ), row=2, col=1)

fig1.update_layout(height=1000, width=900, 
                  title_text="Positive and Negative Speeches per Party",
                  template="simple_white",
                  titlefont=dict(family="Arial, sans-serif", size=18),
                  legend = dict(font = dict(size = 14)))

fig1.update_annotations(dict(font_size=16, font_family="Arial"))

fig1.show()
fig1.write_html("pos_neg_speeches.html")


##################################--split by period--##########################################

# filter the two seperate time periods
start_summer = pd.to_datetime("2022-05-30")
end_summer = pd.to_datetime("2022-08-01")
summer_22 = df[(df['date'] >= start_summer) & (df['date'] <= end_summer)]

start_winter = pd.to_datetime("2022-11-20")
end_winter = pd.to_datetime("2023-02-10")
end_22_early_23 = df[(df['date'] >= start_winter) & (df['date'] <= end_winter)]


# sub summer
df_con_summer = summer_22[summer_22['current_party'] == "Conservative"]
df_lab_summer = summer_22[summer_22['current_party'] == "Labour"]
df_cen_summer = summer_22[summer_22['current_party'] == "Centre"]

# sub winter
df_con_winter = end_22_early_23[end_22_early_23['current_party'] == "Conservative"]
df_lab_winter = end_22_early_23[end_22_early_23['current_party'] == "Labour"]
df_cen_winter = end_22_early_23[end_22_early_23['current_party'] == "Centre"]


# colours
colour_map = {'Conservative':'#115DA8', 'Labour': '#E4003B', 'Centre': '#FDBB30'}

# visualise with plotly.go
layout1 = go.Layout(
    title="Number of Pos/Neg Speeches over Time",
    titlefont=dict(family="Arial, sans-serif", size=20),
    plot_bgcolor="#FFF",  # Sets background color to white
    xaxis=dict(
        title="Date",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=18),
        tickfont=dict(family="Arial, sans-serif", size=14),
    ),
    yaxis=dict(
        title="Number of speeches",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=18),
        tickfont=dict(family="Arial, sans-serif", size=14),
    ),
    template="simple_white",
)

fig = make_subplots(rows=2, cols=2, horizontal_spacing = 0.08, vertical_spacing = 0.12,
                    subplot_titles=("Positive Speeches during Summer 2022", "Negative Speeches during Summer 2022", 
                                                    "Positive Speeches during Winter 22-23", "Negative Speeches during Winter 22-23"),
                    row_heights=[0.5,0.5,]
                    )

fig.add_trace(
    go.Scatter(
            x=df_con_summer["date"],
            y=df_con_summer["POSITIVE"],
            line_color='#115DA8',
            showlegend=False,
            name="Conservative",
            line=dict(width=1)
        ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
            x=df_lab_summer["date"],
            y=df_lab_summer["POSITIVE"],
            line_color='#E4003B',
            showlegend=False,
            name="Labour",
            line=dict(width=1)
        ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
            x=df_cen_summer["date"],
            y=df_cen_summer["POSITIVE"],
            line_color='#FDBB30',
            showlegend=False,
            name="Centre",
            line=dict(width=1)
        ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
            x=df_con_summer["date"],
            y=df_con_summer["NEGATIVE"],
            name="Conservative",
            line_color='#115DA8',
            line=dict(width=1)
        ),
    row=1, col=2
)

fig.add_trace(
    go.Scatter(
            x=df_lab_summer["date"],
            y=df_lab_summer["NEGATIVE"],
            name="Labour",
            line_color='#E4003B',
            line=dict(width=1)
        ),
    row=1, col=2
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
            x=df_con_winter["date"],
            y=df_con_winter["POSITIVE"],
            line_color='#115DA8',
            showlegend=False,
            name="Conservative",
            line=dict(width=1)
        ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
            x=df_lab_winter["date"],
            y=df_lab_winter["POSITIVE"],
            line_color='#E4003B',
            showlegend=False,
            name="Labour",
            line=dict(width=1)
        ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
            x=df_cen_winter["date"],
            y=df_cen_winter["POSITIVE"],
            line_color='#FDBB30',
            showlegend=False,
            name="Centre",
            line=dict(width=1)
        ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
            x=df_con_winter["date"],
            y=df_con_winter["NEGATIVE"],
            line_color='#115DA8',
            showlegend=False,
            name="Conservative",
            line=dict(width=1)
        ),
    row=2, col=2
)

fig.add_trace(
    go.Scatter(
            x=df_lab_winter["date"],
            y=df_lab_winter["NEGATIVE"],
            line_color='#E4003B',
            showlegend=False,
            name="Labour",
            line=dict(width=1)
        ),
    row=2, col=2
)

fig.add_trace(
    go.Scatter(
            x=df_cen_winter["date"],
            y=df_cen_winter["NEGATIVE"],
            line_color='#FDBB30',
            showlegend=False,
            name='Centre',
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
        title="Number of Speeches",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14, color='black'),
        range=[0,80]
    ), row=1, col=1)
fig.update_yaxes(dict(
        title="Number of Speeches",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14,  color='black'),
        range=[0,80]
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
        title="Number of Speeches",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14, color='black'),
        range=[0,80]
    ), row=2, col=1)
fig.update_yaxes(dict(
        title="Number of Speeches",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14, color='black'),
        range=[0,80]
    ), row=2, col=2)

fig.update_layout(height=800, width=1200, 
                  title_text="Positive and Negative Speeches per Party",
                  template="simple_white",
                  titlefont=dict(family="Arial, sans-serif", size=18),
                  legend = dict(font = dict(size = 14)))

fig.update_annotations(dict(font_size=16, font_family="Arial"))

fig.show()
fig.write_html("pos_neg_speeches_zoomed.html")