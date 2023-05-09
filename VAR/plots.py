import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly
import seaborn as sns
from plotly.subplots import make_subplots


# import dataframe
df = pd.read_csv("articles_speeches.csv", keep_default_na=True)
print(df.head())
df["date"] = pd.to_datetime(df["date"])

print(df.head())

fig1 = make_subplots(rows=2, cols=2, vertical_spacing = 0.1,
                    subplot_titles=("Positive Speeches", "Negative Speeches",
                                    "Positive Articles", "Negative Articles")
                    )

fig1.add_trace(
    go.Scatter(
            x=df["date"],
            y=df["POSITIVE_Conservative"],
            line_color='#115DA8',
            showlegend=False,
            name="Conservative",
            line=dict(width=1)
        ),
    row=1, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df["date"],
            y=df["POSITIVE_Labour"],
            line_color='#E4003B',
            showlegend=False,
            name="Labour",
            line=dict(width=1)
        ),
    row=1, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df["date"],
            y=df["POSITIVE_Centre_parties"],
            line_color='#FDBB30',
            showlegend=False,
            name="Centre",
            line=dict(width=1)
        ),
    row=1, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df["date"],
            y=df["NEGATIVE_Conservative"],
            line_color='#115DA8',
            line=dict(width=1),
            name="Conservative",
            legendgroup="group1"
        ),
    row=1, col=2
)

fig1.add_trace(
    go.Scatter(
            x=df["date"],
            y=df["NEGATIVE_Labour"],
            line_color='#E4003B',
            line=dict(width=1),
            name="Labour",
            legendgroup="group1"
        ),
    row=1, col=2
)

fig1.add_trace(
    go.Scatter(
            x=df["date"],
            y=df["NEGATIVE_Centre_parties"],
            line_color='#FDBB30',
            line=dict(width=1),
            name="Centre",
            legendgroup="group1",
            legendgrouptitle_text="Parties"
        ),
    row=1, col=2
)

fig1.add_trace(
    go.Scatter(
            x=df["date"],
            y=df["POSITIVE_Centre"],
            line_color='#FDBB30',
            showlegend=False,
            name="Centre",
            line=dict(width=1)
        ),
    row=2, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df["date"],
            y=df["POSITIVE_Right-wing"],
            line_color='#115DA8',
            showlegend=False,
            name="Right-wing",
            line=dict(width=1)
        ),
    row=2, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df["date"],
            y=df["POSITIVE_Left-wing"],
            line_color='#E4003B',
            showlegend=False,
            name="Left-wing",
            line=dict(width=1)
        ),
    row=2, col=1
)

fig1.add_trace(
    go.Scatter(
            x=df["date"],
            y=df["NEGATIVE_Centre"],
            line_color='#FDBB30',
            name="Centre",
            line=dict(width=1),
            legendgroup="group2"
        ),
    row=2, col=2
)

fig1.add_trace(
    go.Scatter(
            x=df["date"],
            y=df["NEGATIVE_Right-wing"],
            line_color='#115DA8',
            name="Right-wing",
            line=dict(width=1),
            legendgroup="group2"
        ),
    row=2, col=2
)

fig1.add_trace(
    go.Scatter(
            x=df["date"],
            y=df["NEGATIVE_Left-wing"],
            line_color='#E4003B',
            name="Left-wing",
            line=dict(width=1),
            legendgroup="group2",
            legendgrouptitle_text="Newspapers"
        ),
    row=2, col=2
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
    ), row=1, col=2)
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
    ), row=1, col=2)
fig1.update_xaxes(dict(
        title="Date",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14, color='black'),
        title_standoff = 2,
        tickformat='%d %b %y',
        automargin=False
    ), row=2, col=1)
fig1.update_xaxes(dict(
        title="Date",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14, color='black'),
        title_standoff = 2,
        tickformat='%d %b %y',
        automargin=False
    ), row=2, col=2)
fig1.update_yaxes(dict(
        title="Number of Articles",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14, color='black'),
        range=[0,31]
    ), row=2, col=1)
fig1.update_yaxes(dict(
        title="Number of Articles",
        showgrid=True,  
        titlefont=dict(family="Arial, sans-serif", size=14),
        tickfont=dict(family="Arial, sans-serif", size=14, color='black'),
        range=[0,31]
    ), row=2, col=2)

# update the first legend
fig1.update_traces(showlegend=True, selector=dict(legendgroup='group1'), secondary_y=False)

# update the second legend
fig1.update_traces(showlegend=True, selector=dict(legendgroup='group2'), secondary_y=True)


fig1.update_layout(height=800, width=1200, 
                  title_text="Positive and Negative Speeches and Articles",
                  template="simple_white",
                  titlefont=dict(family="Arial, sans-serif", size=18),
                  legend=dict(tracegroupgap=250, font=dict(size=14)))

fig1.update_annotations(dict(font_size=16, font_family="Arial"))

fig1.show()
fig1.write_html("articles_speechesc.html")