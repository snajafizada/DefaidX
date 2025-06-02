import streamlit as st
import pandas as pd
import plotly.express as px

def show_home():
    st.markdown("<h1 style='font-size:42px;color:#A970FF;font-weight:bold;'>Welcome to DefaidX</h1>", unsafe_allow_html=True)

    # Your intro text omitted for brevity...

    # Load data
    df = pd.read_csv("data/clean/all/merged_long_1992-2023.csv")
    df = df[df["Defense_USD"].notna() & (df["Defense_USD"] > 0)]
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)
    years_sorted = sorted(df["Year"].unique())
    df["Year"] = pd.Categorical(df["Year"], categories=years_sorted, ordered=True)

    fig = px.scatter(
        df,
        y="Defense_USD",
        x="Continent",
        animation_frame="Year",
        animation_group="Country",
        size="Defense_USD",
        color="Continent",
        hover_name="Country",
        log_y=True,
        size_max=60,
        range_y=[100, df["Defense_USD"].max()],
        labels={"Defense_USD": "Defense Spending (Million USD)", "Continent": "Region"},
    )

    fig.update_layout(
        height=600,
        margin=dict(l=20, r=20, t=60, b=40),
        showlegend=False,
        title={
            'text': "Global Defense Spending (1990–2023)",
            'font': {'size': 20},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            tickfont=dict(size=14),
            titlefont=dict(size=16)
        ),
        yaxis=dict(
            tickfont=dict(size=14),
            titlefont=dict(size=16)
        ),
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="#E0E0E0"),
    )

    st.plotly_chart(fig, use_container_width=True)
