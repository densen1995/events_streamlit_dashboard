#helpers are reusable utility functions

from pathlib import Path
import pandas as pd
import streamlit as st
from events.utils.constants import DATA_PATH

# Opens any text file and returns its full contents as a string
def read_textfile(path: Path) -> str:
    with open(path) as file:
        return file.read()

""" Reads a CSS file then injects it into the page using a <style> HTML tag. unsafe_allow_html=True tells Streamlit "yes,
    that this is raw HTML, allow it."""
def read_css(path: Path) -> str:
    css = read_textfile(path)
    st.write(f"<style>{css}</style>", unsafe_allow_html=True)


@st.cache_data  #decorator for running and saving a function in the memory
def get_events_df() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH / "events_combined.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["venue_city"] = df["venue_city"].str.strip().str.title()
    return df
