"""This page pulls everything together and then it renders the description, chart, map
 value counts (also in columns), and the filter section"""

import streamlit as st
from events.utils.helpers import read_textfile, read_css, get_events_df
from events.utils.constants import MARKDOWN_PATH, STYLE_PATH, IMAGE_PATH
from events.components.kpis import (
    total_events_kpi,
    onsale_events_kpi,
    upcoming_events_kpi,
    unique_venues_kpi,
    segment_event_count_kpi,
)
from events.components.charts import (
    events_trend_line_chart,
    top_venues_chart,
    segment_pie_chart,
    genre_pie_char
    event_cards,
    venue_map,
)
from events.components.filters import date_filter, segment_filter, event_name_filter, venue_filter


def dashboard_layout():
    st.image(IMAGE_PATH /"StockholmsPuls_HeroENG.png", width="stretch")
    st.markdown("# Stockholm Puls")
    st.markdown(read_textfile(MARKDOWN_PATH / "dashboard_description.md"))

    st.markdown("Event count by segment")

    segments = (
        "Arts & Theatre",
        "Music",
        "Miscellaneous",
        "Nightlife",
        "Sports",

    )
    segment_emojis = {
        "Arts & Theatre": "🎭",
        "Music": "🎶",
        "Miscellaneous": "👾",
        "Nightlife": "🌙",
        "Sports": "🏅",
    }

    cols = st.columns(len(segments))
    for col, segment in zip(cols, segments):
        with col:
            label= f"{segment_emojis[segment]} {segment}"
            segment_event_count_kpi(segment=segment, label=label)
    st.markdown("## Overview")

    cols = st.columns(4)
    with cols[0]:
        total_events_kpi()
    with cols[1]:
        onsale_events_kpi()
    with cols[2]:
        upcoming_events_kpi()
    with cols[3]:
        unique_venues_kpi()


    st.markdown("## Explore Events")

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        date_range = date_filter()
    with row1_col2:
        segment = segment_filter()

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        name_query = event_name_filter()
    with row2_col2:
        venue = venue_filter()


    df = get_events_df()

    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start, end = date_range
        df = df[(df["date"].dt.date >= start) & (df["date"].dt.date <= end)]
    elif hasattr(date_range, "year"):
        df = df[df["date"].dt.date == date_range]

    if segment != "All":
        df = df[df["segment"] == segment]

    if name_query:
        df = df[df["name"].str.contains(name_query, case=False, na=False)]

    if venue != "All":
        df = df[df["venue_name"] == venue]

    st.markdown(f"**{len(df):,} event(s) found**")

    st.markdown("### Event Listings")
    event_cards(df)

    st.markdown("###  Map")
    venue_map(df)


    #Segment pie(full width)
    segment_pie_chart()

    # Month line trend (full width, markers and value labels)
    events_trend_line_chart()

    # Genres pie and Venues bar side by side
    col1, col2 = st.columns(2)
    with col1:
        genre_pie_chart(8)
    with col2:
        top_venues_chart(8)

    st.image(IMAGE_PATH / "StockholmsPuls_FooterENG.webp", width="stretch")

    read_css(STYLE_PATH / "dashboard.css")  # injects custom CSS to style the dashboard.

if __name__ == "__main__":
    dashboard_layout()
