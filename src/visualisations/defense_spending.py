 #
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
    height=600,
    title_x=0.3,
    title_y= 1,
    plot_bgcolor="#111111",
    paper_bgcolor="#111111",
    font=dict(color="white", size=9),
    margin=dict(l=10, r=10, t=80, b=80),
     legend=dict(
        orientation="h",            # horizontal legend
        y=1.15,                     # move legend *above* plot area
        xanchor="center",
        x=0.5,
    )
)

# 1 ------------------------------------------------------------------ #
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
        dragmode="zoom",  # allows zooming directly on the map
        uirevision="choropleth_map",
        coloraxis_colorbar=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=1.1,  # move above the map
            title=dict(text="Defense % of GDP", font=dict(color="white")),
            tickfont=dict(color="white")
        ),
        **COMMON_LAYOUT
    )

    return fig



#2-------------------------------------------------------------------------------

def create_defense_vs_gdp_scatter_excluding_usa_china(df: pd.DataFrame):
    # Filter out USA and China
    df = df[(df['Country'] != 'United States') & (df['Country'] != 'China')]

    # Drop rows with NaNs in columns used
    df_clean = df.dropna(subset=['Defense_USD', 'GDP', 'Year', 'Country', 'Continent'])

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
        size='Defense_USD',
        size_max=40,
        log_x=True,
        log_y=True,
        labels={
            "GDP": "GDP (USD)",
            "Defense_USD": "Defense Spending (USD)"
        },
        title="Defense Spending vs GDP (Without USA & China)",
        template="plotly_dark"
    )

    # Clean layout: remove grid lines
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    # Move legend above the plot, away from animation slider
    fig.update_layout(
        **COMMON_LAYOUT
    )

    return fig

#3------------------------------------------------------------------
# 🕒  Line – Defense spending over time by continent
# ------------------------------------------------------------------ 
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

def create_country_defense_bar_animation(df: pd.DataFrame):
    # Aggregate and rank
    df_ranked = (
        df.groupby(["Year", "Country"], as_index=False)["Defense_USD"].sum()
        .sort_values(["Year", "Defense_USD"], ascending=[True, False])
    )
    df_ranked["Rank"] = df_ranked.groupby("Year")["Defense_USD"].rank(ascending=False, method="first")

    # Keep only Top 20 per year
    df_top20 = df_ranked[df_ranked["Rank"] <= 20]

    # Ensure Country is string type
    df_top20["Country"] = df_top20["Country"].astype(str)

    fig = px.bar(
        df_top20,
        x="Defense_USD",
        y="Country",
        orientation="h",
        animation_frame="Year",
        animation_group="Country",
        color="Country",
        title="🏆 Top 20 Defense Spenders Over Time",
        labels={"Defense_USD": "Defense Spending (USD)"},
        template="plotly_dark",
        category_orders={"Country": df_top20["Country"].unique()}
    )

    # Make bars thicker
    fig.update_traces(marker_line_width=0, width=0.5)

    # Layout
    fig.update_layout(
        **COMMON_LAYOUT,
        xaxis=dict(
            title="Defense Spending (USD)",
            showgrid=False,
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color="white"),
            categoryorder="total ascending"  # Highest spender at top
        ),
        bargap=0.3,
        uirevision="country_defense_bar_animation",
        showlegend=False
    )

    return fig

#5--------------------------------------------------------------------
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

#6--------------------------------------------------------------------------------
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