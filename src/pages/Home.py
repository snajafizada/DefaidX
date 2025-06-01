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

    # Load defense spending data
    data_path = "data/clean/all/merged_long_1992-2023.csv"
    df = pd.read_csv(data_path)

    # Load country codes
    codes_path = "data/clean/all/country_coordinates.csv"
    codes_df = pd.read_csv(codes_path)

    df = df.merge(codes_df[['Country', 'ISO3']], on='Country', how='left')

    # Filter missing Defense_USD
    df = df[df["Defense_USD"].notna()]

    # Convert Year to int and sort, set ordered categorical for animation
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)
    df = df.sort_values(["Year", "Country"])
    years_sorted = sorted(df["Year"].unique())
    df["Year"] = pd.Categorical(df["Year"], categories=years_sorted, ordered=True)

    st.markdown(
        "<div style='color:white; font-size:14px; margin-bottom:10px;'>"
        "👉 Swipe horizontally on the chart below to view all countries."
        "</div>",
        unsafe_allow_html=True,
    )

    fig = px.bar(
        df,
        x="Country",
        y="Defense_USD",
        color="Continent",
        animation_frame="Year",
        animation_group="Country",
        labels={"Defense_USD": "Defense Spending (Million USD)", "Country": "Country"},
        title="Defense Spending by Country (1992–2023)",
    )

    fig.update_layout(
        height=600,
        title=dict(
            text="Defense Spending by Country (1992–2023)",
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=20, color='white')
        ),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white", size=12),
        margin=dict(t=70, b=120, l=40, r=20),
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(size=9),
            fixedrange=False,
            automargin=True,
            showgrid=False,
            title="Country",
        ),
        yaxis=dict(
            type="log",
            title="Defense Spending (log scale)",
            gridcolor="gray",
            zeroline=False,
        ),
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True)
