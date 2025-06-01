import streamlit as st

def show_about():
    st.markdown(
        """
        <h1 style='font-size:42px;color:#A970FF;font-weight:bold;'>About DefaidX</h1>
        
        <p style='font-size:16px;color:#E0E0E0;line-height:1.6;'>
        <strong style='color:#FFFFFF;'>DefaidX</strong> is a small data project that explores how countries invest in defense and aid — and what those choices reveal about global priorities, power, and policy.
        </p>

        <p style='font-size:15px;color:#E0E0E0;line-height:1.6;'>
        Using open-source datasets and interactive visualizations, DefaidX helps unpack key questions:
        </p>

        <ul style='font-size:15px;color:#BBBBBB;line-height:1.6;'>
            <li>Who spends the most on defense — and who trades the most weapons?</li>
            <li>How has global military spending evolved over the last few decades?</li>
            <li>Are we in a modern arms race?</li>
            <li>How do countries balance military spending with social and economic needs?</li>
        </ul>

        <p style='font-size:15px;color:#E0E0E0;line-height:1.6;'>
        Alongside the visuals, DefaidX also publishes short, data-backed insights that highlight patterns and raise questions — turning raw numbers into accessible stories about how our geopolitical landscape is shifting.
        </p>
        """,
        unsafe_allow_html=True,
    )
