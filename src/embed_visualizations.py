import streamlit as st
import pandas as pd
import plotly.express as px
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

def render_defense_gdp_indexed_trend(df):
    st.markdown("### 📈 Indexed Trend: Defense & GDP Over Time")
    country = st.selectbox("Select Country for Indexed Trend:", sorted(df['Country'].unique()))
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
    st.markdown(
         "<p style='font-size:16px; color:#E0E0E0;'>Choose countries from the dropdown to explore individual defense spending trends over time.</p>",
         unsafe_allow_html=True
    )
    countries = st.multiselect(
         "Select Countries:",
         options=sorted(df["Country"].unique()),
         default=["United States", "China"]  # or your preferred default
    )
    if countries:
        fig = create_country_defense_trend(df, countries)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please select at least one country to display the trends.")
