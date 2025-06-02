"""
defense_spending.py
-------------------
Reusable Plotly visualisation builder functions
(mobile-optimised for Streamlit).

Author: DefaidX team
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------------------------------ #
# 🔧  Common layout applied to every figure for consistent dark theme
#     and mobile-friendly sizing / behaviour.
# ------------------------------------------------------------------ #
COMMON_LAYOUT = dict(
    autosize=True,
    height=500,
    plot_bgcolor="#111111",
    paper_bgcolor="#111111",
    font=dict(color="white", size=12),
    margin=dict(l=10, r=10, t=60, b=60),
    xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="white")),
    yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="white")),
    legend=dict(
        font=dict(color="white", size=10),
        orientation="h",
        x=0.5, xanchor="center",
        y=-0.25
    )
)


# ------------------------------------------------------------------ #
# 🗺️  Choropleth – Defence spending as % of GDP
# ------------------------------------------------------------------ #
def create_choropleth_map(df: pd.DataFrame):
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Defense_Share_GDP",
        hover_name="Country",
        hover_data={"Defense_Share_GDP": ':.2f'},
        animation_frame="Year",
        color_continuous_scale="Plasma",
        title="🗺️ Global Defense Spending as % of GDP Over Time",
        template="plotly_dark"
    )

    fig.update_geos(
        showframe=False,
        showcoastlines=False,
        projection_type="natural earth",
        bgcolor="#111111"
    )

    fig.update_layout(
        dragmode="pan",
        uirevision="choropleth_map",
        coloraxis_colorbar=dict(
            title=dict(text="Defense % of GDP", font=dict(color="white")),
            tickfont=dict(color="white")
        ),
        **COMMON_LAYOUT
    )
    return fig


# ------------------------------------------------------------------ #
# 📈  Indexed trend – Defence & GDP (dropdown country selector)
# ------------------------------------------------------------------ #
def create_defense_gdp_indexed_trend(df: pd.DataFrame):
    df = df.dropna(subset=["Defense_USD", "GDP"]).copy()
    df["Year"] = df["Year"].astype(int)
    countries = sorted(df["Country"].unique())

    def build_country_series(country: str):
        sub = df[df["Country"] == country].sort_values("Year")
        base_def, base_gdp = sub.iloc[0][["Defense_USD", "GDP"]]
        sub["Defense_Indexed"] = sub["Defense_USD"] / base_def * 100
        sub["GDP_Indexed"] = sub["GDP"] / base_gdp * 100
        return sub

    data = {c: build_country_series(c) for c in countries}
    init = countries[0]

    fig = go.Figure()
    fig.add_scatter(
        x=data[init]["Year"], y=data[init]["Defense_Indexed"],
        mode="lines+markers", name="Defense (Base 100)",
        text=data[init].apply(lambda r: f"{r['Year']}<br>Defense Indexed: {r['Defense_Indexed']:.1f}", axis=1),
        hoverinfo="text"
    )
    fig.add_scatter(
        x=data[init]["Year"], y=data[init]["GDP_Indexed"],
        mode="lines+markers", name="GDP (Base 100)",
        text=data[init].apply(lambda r: f"{r['Year']}<br>GDP Indexed: {r['GDP_Indexed']:.1f}", axis=1),
        hoverinfo="text"
    )

    # mobile-friendly dropdown centred below chart
    fig.update_layout(
        dragmode="pan",
        uirevision="defense_gdp_indexed_trend",
        title=f"📈 Defense vs GDP Indexed Trend — {init}",
        updatemenus=[dict(
            type="dropdown", direction="down", showactive=True,
            x=0.5, y=-0.25, xanchor="center",
            font=dict(color="white", size=12), bgcolor="#333",
            pad=dict(r=10, t=10),
            buttons=[
                dict(
                    label=c,
                    method="update",
                    args=[
                        {"x": [data[c]["Year"]]*2,
                         "y": [data[c]["Defense_Indexed"], data[c]["GDP_Indexed"]],
                         "text": [
                             data[c].apply(lambda r: f"{r['Year']}<br>Defense Indexed: {r['Defense_Indexed']:.1f}", axis=1),
                             data[c].apply(lambda r: f"{r['Year']}<br>GDP Indexed: {r['GDP_Indexed']:.1f}", axis=1)
                         ]},
                        {"title": f"📈 Defense vs GDP Indexed Trend — {c}"}
                    ]
                ) for c in countries
            ]
        )],
        **COMMON_LAYOUT
    )
    return fig


# ------------------------------------------------------------------ #
# 📊  Scatter – Defence vs GDP (excluding USA & China)
# ------------------------------------------------------------------ #
def create_defense_vs_gdp_scatter_excluding_usa_china(df: pd.DataFrame):
    df = df[~df["Country"].isin(["United States", "China"])]
    df = df.dropna(subset=["GDP", "Defense_USD"]).copy()

    fig = px.scatter(
        df,
        x="Defense_USD",
        y="GDP",
        size="Defense_USD",
        color="Continent",
        hover_name="Country",
        animation_frame="Year",
        animation_group="Country",
        size_max=45,
        title="📊 Defense Spending vs GDP (Excl. USA & China)",
        template="plotly_dark"
    )

    fig.update_traces(
        marker=dict(line=dict(width=0.5, color="black")),
        textfont=dict(size=8, color="black")
    )

    fig.update_layout(
        dragmode="pan",
        uirevision="defense_vs_gdp_scatter_excl_usa_china",
        xaxis=dict(title="Defense Spending (millions USD)", tickformat=","),
        yaxis=dict(title="GDP (millions USD)", tickformat=","),
        **COMMON_LAYOUT
    )
    return fig


# ------------------------------------------------------------------ #
# 🕒  Line – Defense spending over time by continent
# ------------------------------------------------------------------ #
def create_defense_spending_over_time(df: pd.DataFrame):
    df_time = df.groupby(["Year", "Continent"]).Defense_USD.sum().reset_index()
    fig = px.line(
        df_time,
        x="Year", y="Defense_USD", color="Continent",
        markers=True,
        title="🕒 Defense Spending Over Time by Continent",
        template="plotly_dark"
    )
    fig.update_layout(
        dragmode="pan",
        uirevision="defense_spending_over_time",
        hovermode="x unified",
        **COMMON_LAYOUT
    )
    return fig


# ------------------------------------------------------------------ #
# 🏆  Animated bar race – Top 20 spenders
# ------------------------------------------------------------------ #
def create_country_defense_bar_animation(df: pd.DataFrame):
    df = df.copy()
    df["Year"] = df["Year"].astype(str)

    top20 = (df.groupby("Year", group_keys=False)
               .apply(lambda d: d.nlargest(20, "Defense_USD")))
    top20["Rank"] = top20.groupby("Year")["Defense_USD"].rank("first", ascending=False)
    top20.sort_values(["Year", "Rank"], inplace=True)

    fig = px.bar(
        top20, x="Defense_USD", y="Country", orientation="h",
        animation_frame="Year", color="Country",
        range_x=[0, 900_000],
        template="plotly_dark",
        labels={"Defense_USD": "Defense Spending (millions USD)"}
    )

    fig.update_layout(
        dragmode="pan",
        uirevision="country_defense_bar_animation",
        title="🏆 Top 20 Defense Spenders by Year",
        yaxis=dict(title="", categoryorder="total ascending"),
        showlegend=False,
        **COMMON_LAYOUT
    )
    return fig


# ------------------------------------------------------------------ #
# 🧭  Country-level defense trend (multiselect)
# ------------------------------------------------------------------ #
def create_country_defense_trend(df: pd.DataFrame):
    selected = st.multiselect(
        "Select countries", sorted(df["Country"].unique()),
        default=["India", "Germany", "China"]
    )
    if not selected:
        st.info("Select at least one country to view the chart.")
        return None

    filt = df[df["Country"].isin(selected)].copy()
    fig = px.line(
        filt, x="Year", y="Defense_USD", color="Country",
        markers=True,
        title="🧭 Defense Spending Over Time by Country",
        template="plotly_dark"
    )
    fig.update_layout(
        dragmode="pan",
        uirevision="country_defense_trend_multiselect",
        hovermode="x unified",
        **COMMON_LAYOUT
    )
    return fig
