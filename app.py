import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# 1. Load the processed data generated in the previous task
df = pd.read_csv("output/formatted_sales_data.csv")

# Ensure date is parsed correctly and sorted chronologically
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Optional: If you want total daily sales across all regions combined, 
# or if your CSV has individual entries that need aggregation per date:
df_grouped = df.groupby("date", as_index=False)["sales"].sum()

# 2. Create the line chart using Plotly Express
fig = px.line(
    df_grouped,
    x="date",
    y="sales",
    title="Pink Morsel Daily Sales Over Time",
    labels={"date": "Date", "sales": "Total Sales ($)"}
)

# Optional visual styling to highlight the price increase date (January 15, 2021)
fig.add_vline(
    x="2021-01-15",
    line_dash="dash",
    line_color="red",
    annotation_text="Price Increase (Jan 15, 2021)",
    annotation_position="top right"
)

# 3. Initialize the Dash app
app = Dash(__name__)

# 4. Define the layout of the app
app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "padding": "20px", "textAlign": "center"},
    children=[
        # Header title
        html.H1(
            "Soul Foods: Pink Morsel Sales Visualiser",
            style={"color": "#2c3e50", "marginBottom": "20px"}
        ),
        
        # Subtitle context explaining the business question
        html.P(
            "Analyzing whether sales were higher before or after the Pink Morsel price increase on January 15th, 2021.",
            style={"fontSize": "16px", "color": "#7f8c8d", "marginBottom": "30px"}
        ),
        
        # Graph component
        dcc.Graph(
            id="pink-morsel-line-chart",
            figure=fig
        )
    ]
)

# 5. Run the server
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)