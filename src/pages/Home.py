import streamlit as st
import pandas as pd
import plotly.express as px

def show_home():
    st.markdown(
        "<h1 style='font-size:42px;color:#A970FF;font-weight:bold;'>Welcome to DefaidX</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style='font-size:18px;color:#E0E0E0;line-height:1.7;'>
            Curious how the world’s priorities are shifting between power and progress?<br>
            <strong>DefaidX</strong> lets you explore the evolution of global spending on arms versus aid —
            revealing the stories behind the numbers shaping the future of geopolitics.
        </p>

        <p style='font-size:15px;color:#BBBBBB;line-height:1.5;'>
            🔍 Use the sidebar to explore our interactive visuals and insights.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr style='border-color:#444;'>", unsafe_allow_html=True)

    show_defense_trend_by_continent()  # ← Your hero visual on the homepage

    st.markdown("<hr style='border-color:#444;'>", unsafe_allow_html=True)
    st.info("🚧 More features coming soon!")

def show_defense_trend_by_continent():
    st.markdown("### 🛡️ Defense Spending by Continent Over Time")

    # Load data
    data_path = "data/clean/all/merged_long_1992-2023.csv"
    df = pd.read_csv(data_path)

    # Clean and prepare
    df = df[df["Defense_USD"].notna()]
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year", "Continent"])
    df["Year"] = df["Year"].astype(int)

    # Aggregate defense spending by year and continent
    df_grouped = (
        df.groupby(["Year", "Continent"])["Defense_USD"]
        .sum()
        .reset_index()
    )

    # Plot
    fig = px.line(
        df_grouped,
        x="Year",
        y="Defense_USD",
        color="Continent",
        markers=True,
        labels={
            "Defense_USD": "Defense Spending (Million USD)",
            "Year": "Year",
            "Continent": "Continent",
        },
        title="Defense Spending by Continent (1992–2023)",
    )

    # Format
    fig.update_layout(
        height=600,
        margin=dict(t=50, l=20, r=20, b=30),
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        font=dict(color="#E0E0E0"),
        xaxis=dict(tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
        legend=dict(title="", font=dict(size=11)),
    )

    st.plotly_chart(fig, use_container_width=True)
