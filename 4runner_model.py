# 4runner_model.py

import sys
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
import plotly.express as px
import plotly.io as pio
from datetime import datetime, timezone

def process_data(df):
    df[["year", "make", "model", "trim"]] = df["title"].str.extract(r"(\d{4})\s+(\w+)\s+(\w+)\s+(.*)")
    df["year"] = df["year"].astype(int)
    df["age"] = 2025 - df["year"]
    df["log_mileage"] = np.log(df["mileage"])
    return df

def build_model(df):
    X = df[["trim", "age", "log_mileage"]]
    y = df["price"]

    categorical = ["trim"]
    numerical = ["age", "log_mileage"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEndocder(handle_unknown="ignore"), categorical),
            ("num", "passthrough", numerical)
        ]
    )

    model = make_pipeline(preprocessor, LinearRegression())
    model.fit(X, y)

    y_pred = model.predict(X)
    df["predicted_price"] = y_pred
    df["residual"] = df["price"] - df["predicted_price"]
    return model, df

def plot_results(df):
    fig = px.scatter(
        df,
        x="predicted_price",
        y="price",
        color_continuous_scale="RdBu_r",
        custom_data=["title", "trim", "year", "mileage", "dealer", "price", "predicted_price", "residual"],
        title="Predicted vs Actual Used 4Runner Prices"
    )

    fig.update_traces(
        hovertemplate=
            "<b>%{customdata[0]}</b><br>" +
            "Trim: %{customdata[1]}<br>" +
            "Year: %{customdata[2]}<br>" +
            "Mileage: %{customdata[3]:,} mi<br>" +
            "Dealer: %{customdata[4]}<br>" +
            "Actual Price: $%{customdata[5]:,.0f}<br>" +
            "Predicted: $%{customdata[6]:,.0f}<br>" +
            "Residual: $%{customdata[7]:,.0f}<extra></extra>"
    )
    fig.update_traces(df["url"])

    min_val = min(df["price"].min(), df["predicted_price"].min())
    max_val = max(df["price"].max(), df["predicted_price"].max())
    fig.add_shape(
        type="line",
        x0=min_val, y0=min_val,
        x1=max_val, y1=max_val,
        line=dict(color="red", dash="dash")
    )
    fig.update_traces(marker=dict(size=8), mode='markers')
    fig.update_layout(clickmode="event+select")

    pio.write_html(fig, file="output/latest_plot.html", auto_open=False)

def main():
    date = sys.argv[1] if len(sys.argv) > 1 else datetime.now(timezone.utc).strftime("%Y%m%d")
    df = pd.read_csv(f"data/{date}_carsdotcom_4runners.csv")
    processed_df = process_data(df)
    model, modeled_df = build_model(processed_df)
    plot_results(modeled_df)
    return 0

if __name__ == '__main__':
    main()
