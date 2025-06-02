import streamlit as st
import sys
import os

# ── MUST be first Streamlit command ───────────────────────────────────────
st.set_page_config(page_title="DefaidX", layout="wide")


# ── Make src/ importable ──────────────────────────────────────────────────
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# ── Import page modules (each must expose the shown function) ─────────────
from pages import Home, About, Explore, Insights, Contact  # noqa: E402

# ── Initialise / sync navigation state ────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

sidebar_options = ["Home", "About", "Explore", "Insights", "Contact"]

selected = st.sidebar.radio(
    "Select a Section",
    sidebar_options,
    index=sidebar_options.index(st.session_state["page"]),
)


if selected != st.session_state["page"]:
    st.session_state["page"] = selected
    st.rerun()

# ── Render the chosen page ────────────────────────────────────────────────
page = st.session_state["page"]

if page == "Home":
    Home.show_home()
elif page == "About":
    About.show_about()
elif page == "Explore":
    Explore.show_explore()
elif page == "Insights":
    Insights.show_insights()
elif page == "Contact":
    Contact.show_contact()
