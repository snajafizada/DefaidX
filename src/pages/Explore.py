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

DATA_PATH = Path("C:/Users/snaja/OneDrive/defaidX/data/clean/all/merged_long_1992-2023.csv")

def show_explore():
    st.markdown(
        "<h1 style='font-size:42px;color:#A970FF;font-weight:bold;'>📊 Explore Our Data-Rich Visuals </h1>",
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

                st.markdown(
                    """
                    <p style='font-size:16px; color:#E0E0E0; line-height:1.5; margin-top:1rem;'>
                        Explore how defense spending evolves across countries worldwide with this interactive choropleth map.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
                render_choropleth_map(df)

                st.markdown(
                    """
                    <p style='font-size:16px; color:#E0E0E0; line-height:1.5; margin-top:2rem;'>
                        Watch the animated top 20 countries by defense spending over time.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )

                render_defense_vs_gdp_scatter_excluding_usa_china(df)

                st.markdown(
                    """
                    <p style='font-size:16px; color:#E0E0E0; line-height:1.5; margin-top:2rem;'>
                        View indexed trends of defense spending and GDP by country to understand relative changes over time.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
                render_defense_gdp_indexed_trend(df)

                st.markdown(
                    """
                    <p style='font-size:16px; color:#E0E0E0; line-height:1.5; margin-top:2rem;'>
                        The Evolution of Top Spenders Over Time.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
                
                render_country_defense_bar_animation(df)

                st.markdown(
                    """
                    <p style='font-size:16px; color:#E0E0E0; line-height:1.5; margin-top:2rem;'>
                        clich from the drop down menu to explore defense spending trends by individual countries with this detailed visualization.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
                render_country_defense_trend(df)

                st.markdown(
                    """
                    <p style='font-size:16px; color:#E0E0E0; line-height:1.5; margin-top:2rem; margin-bottom:3rem;'>
                        Overview the defense spending over time across countries.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
                render_defense_spending_over_time(df)




    if explore_section == "Aid":
        aid_option = st.selectbox("Choose Aid Topic", [
            "Top Donors & Recipients"
        ])

        if DATA_PATH.exists():
            df = pd.read_csv(DATA_PATH)
            df["Year"] = df["Year"].astype(str)

            if aid_option == "Aid Disbursement":
                st.markdown(
                    """
                    <p style='font-size:16px; color:#E0E0E0; line-height:1.5; margin-top:1rem;'>
                        Explore how aid is disbursed across countries over time with this interactive visualization.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
                #render_aid_disbursement_map(df)

            elif aid_option == "Aid Type Distribution":
                st.markdown(
                    """
                    <p style='font-size:16px; color:#E0E0E0; line-height:1.5; margin-top:2rem;'>
                        See how different types of aid—humanitarian, development, military—are distributed globally.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
                #render_aid_type_distribution_chart(df)

            elif aid_option == "Top Donors & Recipients":
                st.markdown(
                    """
                    <p style='font-size:16px; color:#E0E0E0; line-height:1.5; margin-top:2rem;'>
                        Visualize the top aid donor and recipient countries over the years.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
                #render_top_donors_recipients_bar_animation(df)
