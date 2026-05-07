#Dropdown filters
import streamlit as st
from events.utils.helpers import get_events_df

df = get_events_df()

"""Renders a dropdown menu and returns whatever the user picks
    The selected value is returned to the dashboard, which passes it to filtered_table()"""

def date_filter():
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    return st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )


def segment_filter():
    segments = ["All"] + sorted(df["segment"].dropna().unique().tolist())
    return st.selectbox("Segment", options=segments)


def event_name_filter():
    return st.text_input("Search event name", placeholder="e.g. Jazz, Comedy, Mamma Mia...")


def venue_filter():
    venues = ["All"] + sorted(df["venue_name"].dropna().unique().tolist())
    return st.selectbox("Venue", options=venues)
