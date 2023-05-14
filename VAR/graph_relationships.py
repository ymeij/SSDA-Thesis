import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pp
from collections import Counter

# Granger preprocessing
granger_data = pd.read_csv("granger_var3_graph.csv")
parties = ["Conservative", "Labour", "Centre-parties"]
ideologies = ["Centre", "Left-wing", "Right-wing"]

for val in ["x", "y"]:
    # Fix Centre parties having an _
    granger_data[f"{val}_name"] = granger_data[f"{val}_name"].str.replace(
        "Centre_parties", "Centre-parties"
    )

    granger_data[f"{val}_stripped"] = granger_data[f"{val}_name"].str.split("_").str[-1]

    granger_data[f"{val}_is_party"] = granger_data[f"{val}_stripped"].isin(parties)
    # data["x_is_ideology"] = data["x_stripped"].isin(ideologies)


var_data = pd.read_csv("varmodel_3_pvalues_graph.csv")
var_data.columns = ["x_name", "y_name", "var_pvalue"]

for val in ["x", "y"]:
    # Fix Centre parties having an _
    var_data[f"{val}_name"] = var_data[f"{val}_name"].str.replace(
        "Centre_parties", "Centre-parties"
    )
var_data["lag"] = var_data["x_name"].str.split(".").str[0].str[1].astype(int)
var_data["x_name"] = var_data["x_name"].str.split(".").str[1]

combo_data = var_data.merge(granger_data, on=["x_name", "y_name", "lag"], how="left")
print(f"{len(combo_data) = }")
# Var data is already filtered based on its p-value

filtered = combo_data[combo_data["x_is_party"] != combo_data["y_is_party"]].copy()
print(f"{len(filtered) = }")

significant_data = filtered[filtered["p-value"] < 0.05].copy()
print(f"{len(significant_data) = }")

# lag_1 = significant_data[significant_data["lag"] == 1].copy()
# print(lag_1.head())
# print(f"{len(lag_1) = }")

for val in ["x", "y"]:
    # Fix Centre parties having an _
    significant_data[f"{val}_name"] = significant_data[f"{val}_name"].str.replace(
        "_", " "
    )
    significant_data[f"{val}_name"] = significant_data[f"{val}_name"].str.title()


edges = list(zip(significant_data["x_name"], significant_data["y_name"]))

edge_labels = {edge: lag for edge, lag in zip(edges, significant_data["lag"])}

print(edges[0:5])

# Graph signficant Granger relationships

G = nx.DiGraph()
# G = nx.MultiDiGraph()
G.add_edges_from(edges)
pos = nx.circular_layout(G)
graph_edges = G.edges()

# Get edge counts for colouring bidirectionality.

edge_counts = Counter()


for edge in graph_edges:
    edge_counts[edge] += 1
    # Add the inverse edge too
    edge_counts[(edge[1], edge[0])] += 1

edge_colours = ["green" if edge_counts[edge] > 1 else "purple" for edge in graph_edges]

# Calculate the label offsets

x_abs = 0.8
x_rel = 0.3
y_abs = 0.2
y_rel = 0.3

ideo_positive = {
    f"Positive {x.title()}": (-x_abs + i * x_rel, i * y_rel + y_abs)
    for i, x in enumerate(ideologies)
}
ideo_negative = {
    f"Negative {x.title()}": (-x_abs + i * x_rel, -i * y_rel - y_abs)
    for i, x in enumerate(ideologies)
}
party_positive = {
    f"Positive {x.title()}": (x_abs - i * x_rel, i * y_rel + y_abs)
    for i, x in enumerate(parties)
}
party_negative = {
    f"Negative {x.title()}": (x_abs - i * x_rel, -i * y_rel - y_abs)
    for i, x in enumerate(parties)
}
pos_manual = {}
pos_manual.update(**ideo_positive, **ideo_negative, **party_negative, **party_positive)


def get_node_colour(node_name: str) -> str:
    if "Centre" in node_name:
        return "#FDBB30"
    elif "Labour" in node_name or "Left-Wing" in node_name:
        return "#E4003B"
    elif "Conservative" in node_name or "Right-Wing" in node_name:
        return "#115DA8"

    raise ValueError(f"Bad node name {node_name}")


colour_map = [get_node_colour(node) for node in G]

# centre:
# '#FDBB30'
# conservative/right-wing:
# '#115DA8'
# labour/left-wing:
# '#E4003B'

nx.draw(
    G,
    pos_manual,
    # node_size=2500, #Size for manual plotting
    node_size=1000,
    arrowsize=15,
    min_target_margin=20,
    min_source_margin=21,
    node_color=colour_map,
    edge_color=edge_colours,
)
# connectionstyle="arc3,rad=0.1")


def label_offset(val: float, offset: float) -> float:
    return val + offset if val > 0 else val - offset


offset_pos = {
    node: (label_offset(coords[0], offset=0.0), label_offset(coords[1], offset=0.15))
    for node, coords in pos_manual.items()
}


nx.draw_networkx_labels(G, offset_pos, font_size=8)
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()
plt.xlim((-1, 1))
plt.ylim((-1, 1))


# Create a legend for the edge arrow colors
legend_colours = ["green", "purple"]
legend_labels = ["Bidirectional", "Unidirectional"]
legend_handles = [
    plt.Line2D([], [], color=legend_colours[i], label=legend_labels[i])
    for i in range(len(legend_colours))
]
plt.legend(handles=legend_handles)
plt.savefig("relationship_graph.png", bbox_inches="tight", dpi=1200)
