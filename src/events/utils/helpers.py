from pathlib import Path
import pandas as pd
import streamlit as st
from events.utils.constants import DATA_PATH


def read_textfile(path: Path) -> str:
    with open(path) as file:
        return file.read()


def read_css(path: Path) -> str:
    css = read_textfile(path)
    st.write(f"<style>{css}</style>", unsafe_allow_html=True)


@st.cache_data
def get_events_df() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH / "events_combined.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["venue_city"] = df["venue_city"].str.strip().str.title()
    return df
