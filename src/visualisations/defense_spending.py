import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go


COMMON_LAYOUT = dict(
    autosize=True,
    title_x=0.1,
    dragmode="pan",
    uirevision=True,
    plot_bgcolor="#111111",
    paper_bgcolor="#111111",
    font=dict(color="white", size=12),
    xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="white")),
    yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="white")),
    legend=dict(
        font=dict(color="white", size=10),
        orientation="h",
        x=0.5,
        xanchor="center",
        y=-0.2
    ),
    margin=dict(l=10, r=10, t=60, b=60)
)



def create_choropleth_map(df):
    df = df.copy()
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Defense_Share_GDP",
        hover_name="Country",
        hover_data={"Defense_Share_GDP": ':.2f'},
        animation_frame="Year",
        title="🗺️ Global Defense Spending as % of GDP Over Time",
        template="plotly_dark",
        color_continuous_scale="Plasma"
    )

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='natural earth',
            bgcolor="#111111"
        ),
        coloraxis_colorbar=dict(
            title=dict(text="Defense Share of GDP (%)", font=dict(color="white")),
            tickfont=dict(color="white")
        ),
        **COMMON_LAYOUT
    )

    return fig


def create_defense_gdp_indexed_trend(df):
    df = df.dropna(subset=["Defense_USD", "GDP"]).copy()
    df["Year"] = df["Year"].astype(int)
    countries = sorted(df["Country"].unique())
    data_dict = {}

    for country in countries:
        df_c = df[df["Country"] == country].sort_values("Year")
        base_def = df_c["Defense_USD"].iloc[0]
        base_gdp = df_c["GDP"].iloc[0]

        df_c["Defense_Indexed"] = (df_c["Defense_USD"] / base_def) * 100
        df_c["GDP_Indexed"] = (df_c["GDP"] / base_gdp) * 100
        df_c["Defense_Hover"] = df_c.apply(lambda r: f"Year: {r['Year']}<br>Defense: {r['Defense_USD']:.2f}M<br>Indexed: {r['Defense_Indexed']:.2f}", axis=1)
        df_c["GDP_Hover"] = df_c.apply(lambda r: f"Year: {r['Year']}<br>GDP: {r['GDP']:.2f}M<br>Indexed: {r['GDP_Indexed']:.2f}", axis=1)

        data_dict[country] = {
            "year": df_c["Year"],
            "defense_indexed": df_c["Defense_Indexed"],
            "gdp_indexed": df_c["GDP_Indexed"],
            "defense_hover": df_c["Defense_Hover"],
            "gdp_hover": df_c["GDP_Hover"],
        }

    init_country = countries[0]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data_dict[init_country]["year"],
        y=data_dict[init_country]["defense_indexed"],
        text=data_dict[init_country]["defense_hover"],
        hoverinfo="text",
        mode="lines+markers",
        name="Defense Spending (Base 100)"
    ))
    fig.add_trace(go.Scatter(
        x=data_dict[init_country]["year"],
        y=data_dict[init_country]["gdp_indexed"],
        text=data_dict[init_country]["gdp_hover"],
        hoverinfo="text",
        mode="lines+markers",
        name="GDP (Base 100)"
    ))

    fig.update_layout(
    dragmode="pan",
    uirevision=True,
    **COMMON_LAYOUT
)


    fig.update_layout(
        title=dict(
            text=f"📈 Defense Spending & GDP Indexed Trend: {init_country}",
            #font=dict(size=16, color="white"),
            #x=0.3
        ),

        updatemenus=[
    dict(
        type="dropdown",
        direction="down",
        showactive=True,
        x=0.5,
        y=-0.2,
        xanchor="center",
        font=dict(color="white", size=12),
        bgcolor="#333",
        pad=dict(r=10, t=10),
        buttons=[
            dict(
                label=country,
                method="update",
                args=[
                    {
                        "x": [data_dict[country]["year"]] * 2,
                        "y": [data_dict[country]["defense_indexed"], data_dict[country]["gdp_indexed"]],
                        "text": [data_dict[country]["defense_hover"], data_dict[country]["gdp_hover"]],
                    },
                    {
                        "title": {
                            "text": f"<b>📈 Defense Spending & GDP Indexed Trend: {country}</b>",
                            "x": 0.3,
                            "font": {"size": 16, "color": "white"}
                        }
                    }
                ]
            )
            for country in countries
        ]
    )
],
    **COMMON_LAYOUT
    )

    return fig



def create_defense_vs_gdp_scatter_excluding_usa_china(df):
    # filter out USA & China and rows with missing values
    df = (
        df[~df["Country"].isin(["United States", "China"])]
        .dropna(subset=["GDP", "Defense_USD"])
        .copy()
    )

    fig = px.scatter(
        df,
        x="Defense_USD",
        y="GDP",
        size="Defense_USD",
        color="Continent",
        hover_name="Country",
        text="Country",
        animation_frame="Year",
        animation_group="Country",
        size_max=60,
        title="📊 Defense Spending vs GDP Over Time (Excluding USA & China)",
        template="plotly_dark",
    )

    # style markers & labels
    fig.update_traces(
        textposition="middle center",
        textfont=dict(size=8, color="black"),
        marker=dict(line=dict(width=0.5, color="black")),
    )

    # axis & layout tweaks
    layout_updates = COMMON_LAYOUT.copy()
    layout_updates["xaxis"] = dict(
        title="Defense Spending (USD millions)",
        tickformat=",",
        range=[0, 130_000],              # 👈 fixed x-axis: 0 → 900 000
        showgrid=False,
        zeroline=False,
        tickfont=dict(color="white"),
    )
    layout_updates["yaxis"] = dict(
        title="GDP (USD millions)",
        tickformat=",",
        range=[
            df["GDP"].min() * 0.9,
            df["GDP"].max() * 1.3,
        ],
        showgrid=False,
        zeroline=False,
        tickfont=dict(color="white"),
    )

    # apply all custom layout settings
    fig.update_layout(**layout_updates)

    return fig



def create_defense_spending_over_time(df):
    df_time = df.groupby(["Year", "Continent"]).Defense_USD.sum().reset_index()
    fig = px.line(
        df_time,
        x="Year",
        y="Defense_USD",
        color="Continent",
        markers=True,
         # 👈 Set x-axis (spending) range here
        title="📈 Defense Spending Over Time by Continent",
        template="plotly_dark"
    )
    fig.update_layout(
        hovermode="x unified",
        **COMMON_LAYOUT
    )
    return fig


def create_country_defense_bar_animation(df):
    df = df.copy()
    df["Year"] = df["Year"].astype(str)

    bloomberg_colors = [
        "#9467bd", "#393b79", "#7b4173", "#a55194", "#d6616b", "#3182bd"
    ]

    top_20_per_year = (
        df.groupby("Year", group_keys=False)
        .apply(lambda x: x.nlargest(20, "Defense_USD"))
        .copy()
    )

    top_20_per_year["Rank"] = (
        top_20_per_year.groupby("Year")["Defense_USD"]
        .rank(method="first", ascending=False)
    )
    top_20_per_year.sort_values(by=["Year", "Rank"], inplace=True)

    fig = px.bar(
    top_20_per_year,
    x="Defense_USD",
    y="Country",
    orientation="h",
    animation_frame="Year",
    color="Country",
    hover_name="Country",
    range_x=[0, 900_000],  # 👈 Set x-axis (spending) range here
    template="plotly_dark",
    color_discrete_sequence=bloomberg_colors,
    labels={"Defense_USD": "Defense Spending (USD Millions)"},
)

    fig.update_layout(
        title=dict(
            text="Top 20 Defense Spenders by Year",
            font=dict(size=16, color="white"),
            x=0.7,
            #xanchor="center"
        ),
        yaxis=dict(
            title="",
            categoryorder="total ascending"
        ),
        showlegend=False,
        **COMMON_LAYOUT
    )

    return fig


def create_country_defense_trend(df):
    selected_countries = st.multiselect(
        "Select Countries to View Trends",
        options=sorted(df["Country"].unique()),
        default=["India", "Germany", "China"]
    )

    if not selected_countries:
        st.warning("⚠️ Please select at least one country.")
        return None

    df_filtered = df[df["Country"].isin(selected_countries)].copy()
    fig = px.line(
        df_filtered,
        x="Year",
        y="Defense_USD",
        color="Country",
        markers=True,
        title="📈 Defense Spending Over Time by Country",
        template="plotly_dark"
    )
    fig.update_layout(
        hovermode="x unified",
        **COMMON_LAYOUT
    )
    return fig

# Add any other defense spending visualizations you want here,
# using the same pattern for consistent style.
