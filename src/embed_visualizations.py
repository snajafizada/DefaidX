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
    fig = create_choropleth_map(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

def render_defense_vs_gdp_scatter_excluding_usa_china(df):
    fig = create_defense_vs_gdp_scatter_excluding_usa_china(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

def render_defense_gdp_indexed_trend(df):
    fig = create_defense_gdp_indexed_trend(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

def render_defense_spending_over_time(df):
    fig = create_defense_spending_over_time(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

def render_country_defense_bar_animation(df):
    fig = create_country_defense_bar_animation(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

def render_country_defense_trend(df):
    fig = create_country_defense_trend(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

def show_all_visualizations():
    st.title("🌍 Global Defense Spending Visualizations")

    df = pd.read_csv("C:/Users/snaja/OneDrive/defaidX/data/clean/all/merged_long_1992-2023.csv")
    df["Year"] = df["Year"].astype(str)

    render_choropleth_map(df)
    render_defense_vs_gdp_scatter_excluding_usa_china(df)
    render_defense_gdp_indexed_trend(df)
    render_defense_spending_over_time(df)
    render_country_defense_bar_animation(df)
    render_country_defense_trend(df)
