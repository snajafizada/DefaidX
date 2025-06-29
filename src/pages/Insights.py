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
    # here I will dynamically display HTML reports from the assets/insights folder
    #st.markdown(open("assets/insights/nameofthefiletitleofthereport.html", "r").read(), unsafe_allow_html=True)


#insight_path = Path("assets/insights/aid/titleofthereport.html")
#show_html_insight(insight_path)
