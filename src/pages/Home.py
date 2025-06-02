import streamlit as st
import pandas as pd
import plotly.express as px

# ──────────────────────────────────────────────────────────────────────────
#  HERO PAGE
# ──────────────────────────────────────────────────────────────────────────
def show_home() -> None:
    # -------------------  headline & intro  -------------------------------
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

    # -------------------  hero visualisation  -----------------------------
    show_defense_trend_by_continent()

    st.markdown("<hr style='border-color:#444;'>", unsafe_allow_html=True)
    st.info("🚧 More features coming soon!")


# ──────────────────────────────────────────────────────────────────────────
#  DEFENSE TREND CHART
# ──────────────────────────────────────────────────────────────────────────
def show_defense_trend_by_continent() -> None:
    st.markdown("### 🛡️ Defense Spending by Continent (1992 – 2023)")

    # 1 · load --------------------------------------------------------------
    data_path = "data/clean/all/merged_long_1992-2023.csv"
    df = pd.read_csv(data_path)

    # 2 · clean -------------------------------------------------------------
    df = df[df["Defense_USD"].notna() & (df["Defense_USD"] > 0)]
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["Year", "Continent"])
    df["Year"] = df["Year"].astype(int)

    # 3 · aggregate ---------------------------------------------------------
    trend = (
        df.groupby(["Year", "Continent"], as_index=False)["Defense_USD"]
        .sum()
        .rename(columns={"Defense_USD": "Defense (M USD)"})
    )

    # 4 · plot --------------------------------------------------------------
    fig = px.line(
        trend,
        x="Year",
        y="Defense (M USD)",
        color="Continent",
        markers=True,
        template="plotly_dark",
    )

    # 5 · layout (only 100 % safe keys) ------------------------------------
    fig.update_layout(
        height=560,
        margin=dict(l=20, r=20, t=50, b=40),
        title={
            "text": "Defense Spending by Continent, 1992-2023",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20},
        },
        legend=dict(title="", font=dict(size=11)),
        font=dict(color="#E0E0E0"),
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
    )

    st.plotly_chart(fig, use_container_width=True)
