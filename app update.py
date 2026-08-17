import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# 1. Load the processed data
df = pd.read_csv("output/formatted_sales_data.csv")

# Ensure date is parsed correctly and sorted chronologically
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")
# Format date back to string for clean plotting
df["date_str"] = df["date"].dt.strftime("%Y-%m-%d")

# 2. Initialize the Dash app
app = Dash(__name__)

# 3. Define App Layout with Styling
app.layout = html.Div(
    style={
        "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "backgroundColor": "#f8f9fa",
        "minHeight": "100vh",
        "padding": "40px 20px",
        "color": "#333333"
    },
    children=[
        # Main Container Card
        html.Div(
            style={
                "maxWidth": "900px",
                "margin": "0 auto",
                "backgroundColor": "#ffffff",
                "padding": "30px 40px",
                "borderRadius": "12px",
                "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)"
            },
            children=[
                # Header Title
                html.H1(
                    "Soul Foods: Pink Morsel Sales Visualiser",
                    style={
                        "textAlign": "center",
                        "color": "#2c3e50",
                        "marginBottom": "10px",
                        "fontSize": "28px"
                    }
                ),
                
                # Subtitle Context
                html.P(
                    "Analyzing sales before and after the price increase on January 15th, 2021. Use the filter below to explore region-specific performance.",
                    style={
                        "textAlign": "center",
                        "fontSize": "15px",
                        "color": "#7f8c8d",
                        "marginBottom": "30px"
                    }
                ),
                
                # Region Filter Section
                html.Div(
                    style={
                        "marginBottom": "25px",
                        "textAlign": "center",
                        "padding": "15px",
                        "backgroundColor": "#f1f4f8",
                        "borderRadius": "8px"
                    },
                    children=[
                        html.Label(
                            "Filter by Region:",
                            style={
                                "fontWeight": "600",
                                "marginRight": "15px",
                                "color": "#34495e",
                                "display": "block",
                                "marginBottom": "10px"
                            }
                        ),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": " All Regions", "value": "all"},
                                {"label": " North", "value": "north"},
                                {"label": " East", "value": "east"},
                                {"label": " South", "value": "south"},
                                {"label": " West", "value": "west"}
                            ],
                            value="all",
                            inline=True,
                            style={"display": "inline-flex", "gap": "20px", "cursor": "pointer"}
                        )
                    ]
                ),
                
                # Graph Component
                dcc.Graph(
                    id="sales-line-chart"
                )
            ]
        )
    ]
)

# 4. Define Callback to Update Graph Dynamically Based on Region Selection
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    # Filter data based on selection
    if selected_region == "all":
        # Group by date across all regions
        filtered_df = df.groupby("date_str", as_index=False)["sales"].sum()
        title_suffix = "All Regions Combined"
    else:
        # Filter by specific region (ensuring case-insensitivity match)
        filtered_df = df[df["region"].str.lower() == selected_region]
        filtered_df = filtered_df.groupby("date_str", as_index=False)["sales"].sum()
        title_suffix = f"{selected_region.capitalize()} Region"

    # Create line chart
    fig = px.line(
        filtered_df,
        x="date_str",
        y="sales",
        title=f"Pink Morsel Daily Sales — {title_suffix}",
        labels={"date_str": "Date", "sales": "Total Sales ($)"}
    )

    # Highlight price increase date (January 15, 2021)
    fig.add_vline(
        x="2021-01-15",
        line_dash="dash",
        line_color="#e74c3c",
        annotation_text="Price Increase (Jan 15, 2021)",
        annotation_position="top right"
    )

    # Update layout for a modern, clean look
    fig.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Segoe UI, sans-serif", color="#333333"),
        title_font=dict(size=18, color="#2c3e50"),
        xaxis=dict(showgrid=True, gridcolor="#ecf0f1"),
        yaxis=dict(showgrid=True, gridcolor="#ecf0f1"),
        margin=dict(l=40, r=40, t=50, b=40)
    )

    return fig

# 5. Run the server
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)