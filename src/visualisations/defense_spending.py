"""
defense_spending.py
-------------------
Reusable Plotly visualisation builder functions
(mobile-optimised for Streamlit).

Author: DefaidX team
"""

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
    legend=dict(
        font=dict(color="white", size=10),
        orientation="h",
        x=0.5, xanchor="center",
        y=-0.25
    )
)

# ------------------------------------------------------------------ #
# 🗺️  Choropleth – Defense spending as % of GDP
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
# 📈  Indexed trend – Defense & GDP (dropdown country selector)
# ------------------------------------------------------------------ #
def create_defense_gdp_indexed_trend(df: pd.DataFrame, country: str):
    df = df.dropna(subset=["Defense_USD", "GDP"]).copy()
    df["Year"] = df["Year"].astype(int)

    sub = df[df["Country"] == country].sort_values("Year")
    if sub.empty:
        return None

    base_def, base_gdp = sub.iloc[0][["Defense_USD", "GDP"]]
    sub["Defense_Indexed"] = sub["Defense_USD"] / base_def * 100
    sub["GDP_Indexed"] = sub["GDP"] / base_gdp * 100

    fig = go.Figure()
    fig.add_scatter(
        x=sub["Year"], y=sub["Defense_Indexed"],
        mode="lines+markers", name="Defense (Base 100)",
        text=sub.apply(lambda r: f"{r['Year']}<br>Defense Indexed: {r['Defense_Indexed']:.1f}", axis=1),
        hoverinfo="text"
    )
    fig.add_scatter(
        x=sub["Year"], y=sub["GDP_Indexed"],
        mode="lines+markers", name="GDP (Base 100)",
        text=sub.apply(lambda r: f"{r['Year']}<br>GDP Indexed: {r['GDP_Indexed']:.1f}", axis=1),
        hoverinfo="text"
    )

    fig.update_layout(
        dragmode="pan",
        uirevision=f"defense_gdp_indexed_trend_{country}",
        title=f"📈 Defense vs GDP Indexed Trend — {country}",
        xaxis=dict(
            title="Year",
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            title="Indexed Value (Base 100)",
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="white")
        ),
        **COMMON_LAYOUT
    )
    return fig


def create_defense_vs_gdp_scatter_excluding_usa_china(df):
    # Filter out USA and China
    df = df[(df['Country'] != 'United States') & (df['Country'] != 'China')]

    # Drop rows with NaNs in columns used
    df_clean = df.dropna(subset=['Defense_USD', 'GDP', 'Year', 'Country'])

    if df_clean.empty:
        return None

    fig = px.scatter(
        df_clean,
        x='GDP',
        y='Defense_USD',
        animation_frame='Year',
        animation_group='Country',
        color='Continent',
        hover_name='Country',
        size='Defense_USD',  # size cannot contain NaNs now
        size_max=40,
        log_x=True,
        log_y=True,
        labels={
            "GDP": "GDP (USD, log scale)",
            "Defense_USD": "Defense Spending (USD, log scale)"
        },
        title="Defense Spending vs GDP (Excluding USA & China)",
    )

    fig.update_layout(**COMMON_LAYOUT)
    return fig


# ------------------------------------------------------------------ #
# 🕒  Line – Defense spending over time by continent
# ------------------------------------------------------------------ #
def create_defense_spending_over_time(df: pd.DataFrame):
    df_time = df.groupby(["Year", "Continent"], as_index=False)["Defense_USD"].sum()
    df_time["Year"] = df_time["Year"].astype(int)

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
        xaxis=dict(
            title="Year",
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            title="Defense Spending (millions USD)",
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="white")
        ),
        **COMMON_LAYOUT
    )
    return fig


# ------------------------------------------------------------------ #
# 🏆  Animated bar race – Top 20 spenders
# ------------------------------------------------------------------ #
def create_country_defense_bar_animation(df: pd.DataFrame):
    df = df.copy()
    df["Year"] = df["Year"].astype(str)

    # For each year, top 20 countries by Defense_USD
    top20 = (
        df.groupby("Year", group_keys=False)
          .apply(lambda d: d.nlargest(20, "Defense_USD"))
    )
    top20["Rank"] = top20.groupby("Year")["Defense_USD"].rank("first", ascending=False)
    top20.sort_values(["Year", "Rank"], inplace=True)

    max_defense = top20["Defense_USD"].max() * 1.1

    fig = px.bar(
        top20, x="Defense_USD", y="Country", orientation="h",
        animation_frame="Year", color="Country",
        range_x=[0, max_defense],
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
# 🧭  Country-level defense trend (multiselect input removed here)
# ------------------------------------------------------------------ #
def create_country_defense_trend(df: pd.DataFrame, selected_countries: list[str]):
    if not selected_countries:
        return None

    filt = df[df["Country"].isin(selected_countries)].copy()
    filt["Year"] = filt["Year"].astype(int)

    fig = px.line(
        filt, x="Year", y="Defense_USD", color="Country",
        markers=True,
        title="🧭 Defense Spending Over Time by Country",
        template="plotly_dark"
    )
    fig.update_layout(
        dragmode="pan",
        uirevision="country_defense_trend",
        hovermode="x unified",
        xaxis=dict(
            title="Year",
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            title="Defense Spending (millions USD)",
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="white")
        ),
        **COMMON_LAYOUT
    )
    return fig
