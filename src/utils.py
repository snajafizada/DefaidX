import streamlit as st
import pandas as pd
from typing import Optional

# Path to the unified metadata file that contains Country, ISO3, lat, lon
COUNTRY_COORDS_CSV = r"C:\Users\snaja\OneDrive\defaidX\data\clean\all\country_coordinates.csv"

###############################################################################
# Internal helpers
###############################################################################

@st.cache_data(show_spinner=False, ttl=86400)
def _load_country_metadata(csv_path: str = COUNTRY_COORDS_CSV) -> pd.DataFrame:
    """Return a DataFrame with normalised column names.

    The function trims white‑space and harmonises column names so that at the
    Streamlit‑level we can rely on *exactly* the following columns being
    present:
    - ``Country``  – Country name as used across Defaidtics datasets.
    - ``ISO3``     – 3‑letter ISO‑3166 alpha‑3 code.
    - ``lat``      – Latitude.
    - ``lon``      – Longitude.
    """
    df = pd.read_csv(csv_path)

    # ── Normalise header casing / spelling ────────────────────────────────────
    df.rename(columns=lambda c: c.strip(), inplace=True)

    # ISO column
    iso_candidates = {
        c for c in df.columns if c.lower().replace("-", "_") in {"iso3", "alpha3", "alpha_3", "iso_3", "iso"}
    }
    if "ISO3" not in df.columns:
        if iso_candidates:
            df.rename(columns={iso_candidates.pop(): "ISO3"}, inplace=True)
        else:
            raise KeyError(
                "Could not find an ISO3 column in the metadata CSV. "
                "Add a column named 'ISO3' or a synonym like 'alpha‑3'.",
            )

    # Latitude / longitude columns – accept common variants
    lat_candidates = [c for c in df.columns if c.lower() in {"lat", "latitude"}]
    lon_candidates = [c for c in df.columns if c.lower() in {"lon", "lng", "long", "longitude"}]
    if lat_candidates and lon_candidates:
        df.rename(columns={lat_candidates[0]: "lat", lon_candidates[0]: "lon"}, inplace=True)
    else:
        raise KeyError("Could not find both latitude and longitude columns in the metadata CSV.")

    return df[["Country", "ISO3", "lat", "lon"]]

###############################################################################
# Public API used throughout Defaidtics
###############################################################################

@st.cache_data(show_spinner=False, ttl=86400)
def get_country_coords_from_csv(
    countries: tuple[str, ...],
    csv_path: str = COUNTRY_COORDS_CSV,
) -> dict[str, tuple[Optional[float], Optional[float]]]:
    """Return a mapping ``{country: (lat, lon)}`` for the requested countries.

    If a country is not present in the metadata file the value is
    ``(None, None)`` so that calling code can decide how to handle it.
    """
    df = _load_country_metadata(csv_path)
    coords_lookup = {row["Country"]: (row["lat"], row["lon"]) for _, row in df.iterrows()}
    return {country: coords_lookup.get(country, (None, None)) for country in countries}


def country_to_iso3(country_name: str, csv_path: str = COUNTRY_COORDS_CSV) -> str:
    """Return the ISO3 code for *country_name* or "N/A" if not found."""
    df = _load_country_metadata(csv_path)
    row = df.loc[df["Country"] == country_name]
    if row.empty:
        return "N/A"
    return row.iloc[0]["ISO3"]

###############################################################################
# Miscellaneous helpers
###############################################################################

def show_html_insight(file_path: str) -> None:
    """Render an HTML file inside Streamlit with a fixed height and scroll."""
    with open(file_path, "r", encoding="utf-8") as handle:
        html_content = handle.read()
    st.components.v1.html(html_content, height=1000, scrolling=True)
