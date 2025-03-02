import pandas as pd
import plotly.graph_objects as go
import random


#To do:
'''
1. randomize target colors
2. choose source colors
3. debug sorting
4. label outside the diagram
5. Font of the label
'''

# Load the dataset
file_path = "./concept_keywords.csv"  # Replace with your actual file path
df = pd.read_csv(file_path)

# Function to generate random bright colors
def generate_dark_colors(n):
    return [
        f"#{random.randint(0, 128):02X}{random.randint(0, 128):02X}{random.randint(0, 128):02X}"
        for _ in range(n)
    ]

# Define source colors:
#source_colors_list = ["#909CC2", "#084887", "#7F6947", "#BA7A27", "#F58A07", "#F79B2E", "#F9AB55", "#F8D0A8"]
source_colors_list = ["#1A8FE3", "#4050EB", "#6610F2", "#9C119E", "#D11149", "#E14127", "#F17105", "#EC9A17"]
# Count occurrences of target nodes for sorting
target_counts_sorted = df.iloc[:, 1].value_counts()

# Sort target nodes based on occurrence count (high to low)
sorted_targets = target_counts_sorted.index.tolist()

# Sort dataframe based on target node rankings
df_sorted = df.sort_values(by=df.columns[1], key=lambda x: x.map(target_counts_sorted), ascending=False)

# Extract nodes again after sorting
source_nodes_sorted = df_sorted.iloc[:, 0].tolist()
target_nodes_sorted = df_sorted.iloc[:, 1].tolist()
nodes_sorted = list(dict.fromkeys(source_nodes_sorted + sorted_targets))  # Preserve order

# Update node mapping
node_indices_sorted = {node: i for i, node in enumerate(nodes_sorted)}

# Create source and target indices
source_indices_sorted = [node_indices_sorted[src] for src in source_nodes_sorted]
target_indices_sorted = [node_indices_sorted[tgt] for tgt in target_nodes_sorted]

# Generate new dark colors for nodes
dark_colors = generate_dark_colors(len(set(target_nodes_sorted)))

# Assign bright colors to source nodes
source_colors = {node: source_colors_list[i % len(source_colors_list)] for i, node in enumerate(set(source_nodes_sorted))}

# Assign the same color to corresponding flows
# Convert source colors to RGBA format with adjusted opacity (e.g., 0.5 = 50% opacity)
flow_opacity = 0.4  # Adjust this value (0 = transparent, 1 = solid)
link_colors = [
    f"rgba({int(source_colors_list[src][1:3], 16)}, {int(source_colors_list[src][3:5], 16)}, {int(source_colors_list[src][5:7], 16)}, {flow_opacity})"
    for src in source_indices_sorted
]

# Assign bright colors to all nodes
target_colors_list = generate_dark_colors(len(target_counts_sorted))
target_colors = {node: target_colors_list[i % len(target_colors_list)] for i, node in enumerate(set(target_nodes_sorted))}
node_colors = list(source_colors.values()) + list(target_colors.values())

# Generate Sankey diagram
fig = go.Figure(go.Sankey(
    node=dict(
        pad=2,  # Reduce padding to attach bars together
        thickness=30,
        line=dict(color="black", width=0),
        label=nodes_sorted,
        color=node_colors
    ),
    link=dict(
        source=source_indices_sorted,
        target=target_indices_sorted,
        value=[100] * len(source_indices_sorted),  # Equal weights
        color=link_colors
    )
))

fig.update_layout(
    title_text="Concepts and Keywords",
    font_family="Arial",
    font_size=24,
    height = 1800,
    width = 1600,
    title_font_family="Arial",
)
# Save the updated Sankey diagram
fig.write_html("sankey_diagram_final.html")
fig.write_image("sankey_diagram_final.jpg")
# Show the diagram
fig.show()
