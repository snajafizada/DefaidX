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
    title_x=0.3,
    title_y=0.90,
    plot_bgcolor="#111111",
    paper_bgcolor="#111111",
    font=dict(color="white", size=9),
    margin=dict(l=10, r=10, t=80, b=80),
    legend=dict(
        font=dict(color="white", size=10),
        orientation="h",
        x=0.5, xanchor="center",
        y=-0.25
    )
)

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
        bgcolor="#111111",
        projection_scale=1.2  # zoom in slightly for better focus
    )

    fig.update_layout(
        dragmode="pan",  # allows panning instead of zoom on map
        uirevision="choropleth_map",
        coloraxis_colorbar=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=1.05,  # place colorbar above the map
            title=dict(text="Defense % of GDP", font=dict(color="white")),
            tickfont=dict(color="white"),
        ),
        margin=dict(t=100),  # space on top for colorbar
        **COMMON_LAYOUT
    )

    return fig

# ------------------------------------------------------------------ #
def create_defense_vs_gdp_scatter_excluding_usa_china(df):
    # Filter out USA and China
    df = df[(df['Country'] != 'United States') & (df['Country'] != 'China')]
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
        size='Defense_USD',
        size_max=40,
        log_x=True,
        log_y=True,
        labels={
            "GDP": "GDP (USD, log scale)",
            "Defense_USD": "Defense Spending (USD, log scale)"
        },
        title="Defense Spending vs GDP (Excluding USA & China)",
        template="plotly_dark"
    )

    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    fig.update_layout(
        legend=dict(
            orientation="h",
            y=1.15,
            yanchor="bottom",
            x=0.5,
            xanchor="center",
            bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"),
        ),
        margin=dict(l=10, r=10, t=80, b=80),
        **COMMON_LAYOUT
    )
    return fig

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
            tickfont=dict(color="white"),
            range=[0, 900000]
        ),
        **COMMON_LAYOUT
    )
    return fig

# ------------------------------------------------------------------ #
def create_country_defense_bar_animation(df: pd.DataFrame):
    df_ranked = (
        df.groupby(["Year", "Country"], as_index=False)["Defense_USD"].sum()
        .sort_values(["Year", "Defense_USD"], ascending=[True, False])
    )
    df_ranked["Rank"] = df_ranked.groupby("Year")["Defense_USD"].rank(ascending=False, method="first")
    df_top20 = df_ranked[df_ranked["Rank"] <= 20]

    fig = px.bar(
        df_top20,
        x="Defense_USD",
        y="Country",
        orientation="h",
        animation_frame="Year",
        color="Country",
        title="🏆 Top 20 Defense Spenders Over Time",
        labels={"Defense_USD": "Defense Spending (USD)"},
        template="plotly_dark"
    )

    fig.update_layout(
        xaxis=dict(
            range=[0, 900000],
            title="Defense Spending (millions USD)",
            showgrid=False,
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color="white")
        ),
        bargap=0.1,
        bargroupgap=0.1,
        uirevision="country_defense_bar_animation",
        showlegend=False,
        **COMMON_LAYOUT
    )

    fig.update_traces(marker_line_width=1.5)  # thicker outlines for bars

    return fig


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
            range=[0, 900000],
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="white")
        ),
        **COMMON_LAYOUT
    )
    return fig
