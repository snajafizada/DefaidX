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

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Visualizations")
        st.markdown(
            "<p style='color:#DDDDDD;'>Interactive dashboards.</p>",
            unsafe_allow_html=True,
        )
        if st.button("Go to Explore"):
            st.session_state["page"] = "Explore"
            st.rerun()

    with col2:
        st.subheader("🧠 Insights")
        st.markdown(
            "<p style='color:#DDDDDD;'>Uncover stories behind the data.</p>",
            unsafe_allow_html=True,
        )
        if st.button("Go to Insights"):
            st.session_state["page"] = "Insights"
            st.rerun()

    st.markdown("<hr style='border-color:#444;'>", unsafe_allow_html=True)
    st.info("🚧 More features coming soon!")

    # Load data
    data_path = "data/clean/all/merged_long_1992-2023.csv"
    df = pd.read_csv(data_path)

    # Clean data
    df = df[df["Defense_USD"].notna()]
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)
    df = df.sort_values(["Year", "Country"])
    years_sorted = sorted(df["Year"].unique())
    df["Year"] = pd.Categorical(df["Year"], categories=years_sorted, ordered=True)

    # Create figure
    fig = px.scatter(
        df,
        x="Defense_USD",
        y="Continent",
        animation_frame="Year",
        animation_group="Country",
        size="Defense_USD",
        color="Continent",
        hover_name="Country",
        log_x=True,
        size_max=60,
        range_x=[100, df["Defense_USD"].max()],
        title="Global Defense Spending (1990–2023)",
        labels={"Defense_USD": "Defense Spending (Million USD)", "Continent": "Region"},
    )
    
    #fig.update_layout(
        #height=500,
        #paper_bgcolor="#0E1117",
        #plot_bgcolor="#0E1117",
        #font_color="#E0E0E0",
        #margin=dict(l=10, r=10, t=50, b=20),
        #showlegend=True
#)
    st.plotly_chart(fig, use_container_width=True)
