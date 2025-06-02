import streamlit as st
import pandas as pd
import plotly.express as px

def show_home():
    st.markdown(
        "<h1 style='font-size:32px;color:#A970FF;font-weight:bold;'>Welcome to DefaidX</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style='font-size:14px;color:#E0E0E0;line-height:1.5;'>
            Curious how the world’s priorities are shifting between power and progress?<br>
            <strong>DefaidX</strong> lets you explore the evolution of global spending on arms versus aid —
            revealing the stories behind the numbers shaping the future of geopolitics.
        </p>

        <p style='font-size:13px;color:#BBBBBB;line-height:1.3;'>
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
            "<p style='color:#DDDDDD;font-size:14px;'>Interactive dashboards.</p>",
            unsafe_allow_html=True,
        )
        if st.button("Go to Explore"):
            st.session_state["page"] = "Explore"
            st.rerun()

    with col2:
        st.subheader("🧠 Insights")
        st.markdown(
            "<p style='color:#DDDDDD;font-size:14px;'>Uncover stories behind the data.</p>",
            unsafe_allow_html=True,
        )
        if st.button("Go to Insights"):
            st.session_state["page"] = "Insights"
            st.rerun()

    st.markdown("<hr style='border-color:#444;'>", unsafe_allow_html=True)
    st.info("🚧 More features coming soon!")

    data_path = "data/clean/all/merged_long_1992-2023.csv"
    df = pd.read_csv(data_path)

    codes_path = "data/clean/all/country_coordinates.csv"
    codes_df = pd.read_csv(codes_path)

    df = df.merge(codes_df[['Country', 'ISO3']], on='Country', how='left')
    df = df[df["Defense_USD"].notna()]

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)
    df = df.sort_values(["Year", "Country"])
    years_sorted = sorted(df["Year"].unique())
    df["Year"] = pd.Categorical(df["Year"], categories=years_sorted, ordered=True)

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
        size_max=55,  # smaller bubbles
        #range_y=[100, 900000],
        title="Global Defense Spending (1992–2023)",
        labels={"Defense_USD": "Defense Spending (Million USD)", "Continent": "Region"}
    )

    fig.update_layout(
        height=600,  
        width=None,  
        title_x=0.19,
        title_y=0.93,
        title_font=dict(size=16),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white", size=10),  # smaller font
        margin=dict(t=90, b=40, l=10, r=20),
        showlegend=False,

        xaxis=dict(
            type='category',
            categoryorder='array',
            categoryarray=["Africa", "Asia", "Europe", "North America", "Oceania", "South America"],
            tickangle=-45,
            showgrid=True,
            zeroline=True,
            tickfont=dict(size=9),
            automargin=True,
        ),
        yaxis=dict(
            showgrid=False,
            gridcolor='gray',
            zeroline=False,
            type='log',
            range=[3, 6],
            title="Defense Spending (Million USD)",
            title_font=dict(size=11),
            tickfont=dict(size=9),
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

    st.plotly_chart(fig, use_container_width=True)
