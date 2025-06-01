import streamlit as st
from pathlib import Path

def show_insights():
    st.markdown(
        """
        <h1 style='font-size:42px;color:#A970FF;font-weight:bold;'>
            Insights
        </h1>
        <p style='font-size:16px;color:#E0E0E0;line-height:1.6;'>
            Coming Soon!
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.write("...")
    # You could dynamically display HTML reports from the assets/insights folder
    #st.markdown(open("assets/insights/how_military_aid_affects_development.html", "r").read(), unsafe_allow_html=True)


#insight_path = Path("assets/insights/aid/oda.html")
#show_html_insight(insight_path)
