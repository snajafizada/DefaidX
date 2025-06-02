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
            st.experimental_rerun()

    with col2:
        st.subheader("🧠 Insights")
        st.markdown(
            "<p style='color:#DDDDDD;'>Uncover stories behind the data.</p>",
            unsafe_allow_html=True,
        )
        if st.button("Go to Insights"):
            st.session_state["page"] = "Insights"
            st.experimental_rerun()

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

    # Create the figure
    fig = px.scatter(
        df,
        x="Continent",
        y="Defense_USD",
        animation_frame="Year",
        animation_group="Country",
        size="Defense_USD",
        color="Continent",
        hover_name="Country",
        log_y=True,
        size_max=30,
        range_y=[100, 900000],
        title="Global Defense Spending (1990–2023)",
        labels={"Defense_USD": "Defense Spending (Million USD)", "Continent": "Region"}
    )

    # Update layout for vertical, narrow figure with tight continent spacing
    fig.update_layout(
        height=900,  # tall figure
        width=400,   # narrow width
        title_x=0.5,
        title_y=0.95,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        margin=dict(t=80, b=70, l=60, r=40),
        showlegend=False,
        xaxis=dict(
            type='category',
            categoryorder='array',
            categoryarray=["Africa", "Asia", "Europe", "North America", "Oceania", "South America"],
            tickangle=-45,
            showgrid=True,
            zeroline=True,
            range=[-0.5, 5.5],  # tighten categorical axis around continents
            automargin=True,
        ),
        yaxis=dict(
            showgrid=False,
            gridcolor='gray',
            zeroline=False,
            type='log',
            range=[2, 5.95],  # corresponds to 100 to ~900,000 in log scale
            title="Defense Spending (Million USD)"
        ),
        updatemenus=[dict(
            type="buttons",
            x=0.05,
            y=-0.1,
            buttons=[
                dict(label="Play", method="animate",
                     args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)]),
                dict(label="Pause", method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate",
                                        transition=dict(duration=0))])
            ]
        )]
    )

    fig.update_traces(
        marker=dict(line=dict(width=1, color="gray")),
        textfont=dict(color='white')
    )

    st.plotly_chart(fig, use_container_width=True)
