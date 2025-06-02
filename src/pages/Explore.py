import streamlit as st
import pandas as pd
from pathlib import Path
from embed_visualizations import (
    render_choropleth_map,
    render_defense_vs_gdp_scatter_excluding_usa_china,
    render_defense_gdp_indexed_trend,
    render_country_defense_bar_animation,
    render_country_defense_trend,
    render_defense_spending_over_time
)

DATA_PATH = Path("data/clean/all/merged_long_1992-2023.csv")

def show_explore():
    st.markdown(
        "<h1 style='font-size:42px;color:#A970FF;font-weight:bold;'>📊 Explore Our Data-Rich Visuals</h1>",
        unsafe_allow_html=True,
    )

    explore_section = st.selectbox("Choose Topic", ["Defense", "Aid"])

    if explore_section == "Defense":
        defense_option = st.selectbox("Choose Defense Topic", [
            "Defense Spending", "Arms Trade", "Other Defense Indicators"
        ])

        if defense_option == "Defense Spending":
            if DATA_PATH.exists():
                df = pd.read_csv(DATA_PATH)
                df["Year"] = df["Year"].astype(str)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 🗺️ Choropleth Map: Global Defense Spending as % of GDP")
                render_choropleth_map(df)

                st.markdown("### 📊 Scatter Plot: Defense vs GDP (Excluding USA & China)")
                render_defense_vs_gdp_scatter_excluding_usa_china(df)

                st.markdown("### 📉 Indexed Trend: Defense Spending & GDP")
                
                # Add a country selector for the user to choose the country for the indexed trend
                country = st.selectbox("Select Country for Indexed Trend:", sorted(df['Country'].unique()))
                
                # Now call the function with both df and the selected country
                fig = render_defense_gdp_indexed_trend(df, country)
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("### 🏆 Animated Bar Chart: Top 20 Defense Spenders")
                render_country_defense_bar_animation(df)

                st.markdown("### 🧭 Country Comparison: Defense Spending Trends")
                st.markdown(
                    "<p style='font-size:16px; color:#E0E0E0;'>Choose countries from the dropdown in the chart to explore individual defense spending trends over time.</p>",
                    unsafe_allow_html=True
                )
                render_country_defense_trend(df)

                st.markdown("### 🕒 Time Series: Global Defense Spending Over Time")
                render_defense_spending_over_time(df)



    if explore_section == "Aid":
        aid_option = st.selectbox("Choose Aid Topic", [
            "Top Donors & Recipients"
        ])

        if DATA_PATH.exists():
            df = pd.read_csv(DATA_PATH)
            df["Year"] = df["Year"].astype(str)

            if aid_option == "Top Donors & Recipients":
                st.markdown("### 💸 Top Aid Donors and Recipients Over Time")
                st.markdown(
                    "<p style='font-size:16px; color:#E0E0E0;'>Visualize the most generous donor countries and major recipient countries from 1992 to 2023.</p>",
                    unsafe_allow_html=True,
                )
                # render_top_donors_recipients_bar_animation(df)
