import streamlit as st
import pandas as pd
from visualisations.defense_spending import (
    create_choropleth_map,
    create_defense_vs_gdp_scatter_excluding_usa_china,
    create_defense_gdp_indexed_trend,
    create_defense_spending_over_time,
    create_country_defense_bar_animation,
    create_country_defense_trend
)

def render_choropleth_map(df):
    st.markdown("### 🗺️ Choropleth Map: Defense Spending as % of GDP")
    fig = create_choropleth_map(df)
    if fig:
        with st.container():
            st.plotly_chart(fig, use_container_width=True)

def render_defense_vs_gdp_scatter_excluding_usa_china(df):
    st.markdown("### 📊 Scatter Plot: Defense vs GDP (Excl. USA & China)")
    fig = create_defense_vs_gdp_scatter_excluding_usa_china(df)
    if fig:
        with st.container():
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for this plot.")

def render_defense_gdp_indexed_trend(df, country):
    st.markdown("### 📈 Indexed Trend: Defense & GDP Over Time")
    fig = create_defense_gdp_indexed_trend(df, country)
    if fig:
        with st.container():
            st.plotly_chart(fig, use_container_width=True)

def render_defense_spending_over_time(df):
    st.markdown("### 🕒 Continental Trends: Defense Spending Over Time")
    fig = create_defense_spending_over_time(df)
    if fig:
        with st.container():
            st.plotly_chart(fig, use_container_width=True)

def render_country_defense_bar_animation(df):
    st.markdown("### 🏆 Animated Bar Chart: Top 20 Defense Spenders")
    fig = create_country_defense_bar_animation(df)
    if fig:
        with st.container():
            st.plotly_chart(fig, use_container_width=True)

def render_country_defense_trend(df):
    st.markdown("### 🧭 Country Comparison: Defense Spending Trends")
    fig = create_country_defense_trend(df)
    if fig:
        with st.container():
            st.plotly_chart(fig, use_container_width=True)

def show_all_visualizations():
    st.title("🌍 Global Defense Spending Visualizations")
    st.markdown(
        """
        Below are interactive visualizations of global defense spending trends, GDP comparisons, and country-level insights.
        All charts are optimized for both desktop and mobile.
        """
    )
    df = pd.read_csv("data/clean/all/merged_long_1992-2023.csv")
    df["Year"] = df["Year"].astype(str)

    render_choropleth_map(df)
    render_defense_vs_gdp_scatter_excluding_usa_china(df)
    render_defense_gdp_indexed_trend(df)
    render_defense_spending_over_time(df)
    render_country_defense_bar_animation(df)
    render_country_defense_trend(df)
