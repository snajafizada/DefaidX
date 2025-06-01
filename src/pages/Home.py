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
    
    df = df[df["Defense_USD"].notna()]  # Filter out rows with missing Defense_Spending
    
    codes_path = "data/clean/all/country_coordinates.csv"
    codes_df = pd.read_csv(codes_path)

    df = df.merge(codes_df[['Country', 'ISO3']], on='Country', how='left')

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
        size_max=100,
        range_x=[100, df["Defense_USD"].max()],
        title="Global Defense Spending (1990–2023)",
        labels={"Defense_USD": "Defense Spending (Million USD)", "Continent": "Region"}
    )

    fig.update_layout(
        title_x=0.4,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        margin=dict(t=40, b=40, l=50, r=50),
        showlegend=False,
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
        textfont=dict(color='black')
    )

    st.plotly_chart(fig, use_container_width=True)
