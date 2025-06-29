import streamlit as st

def show_about():
    st.markdown(
        """
        <h1 style='font-size:42px;color:#A970FF;font-weight:bold;'>About DefaidX</h1>
        
        <p style='font-size:16px;color:#E0E0E0;line-height:1.6;'>
        <strong style='color:#FFFFFF;'>DefaidX</strong> is a data storytelling project that explores the public financing of arms and aid — and how these spending choices shape global development.
        </p>

        <p style='font-size:15px;color:#E0E0E0;line-height:1.6;'>
        Using open-source datasets, DefaidX helps unpack key questions:
        </p>
        
        <ul style='font-size:15px;color:#BBBBBB;line-height:1.6;'>
        <li>How has global spending on defense and aid changed over the past decades?</li>
        <li>Who invests the most in defense — and who exports the most weapons?</li>
        <li>How do countries weigh military budgets against social and economic needs?</li>
        <li>Are we living through a new arms race?</li>
        </ul>

        <p style='font-size:15px;color:#E0E0E0;line-height:1.6;'>
        Beyond the charts, DeFaidX turns raw data into stories that uncover patterns and spark new questions about power, policy, and development.
        </p>
        """,
        unsafe_allow_html=True,
    )
