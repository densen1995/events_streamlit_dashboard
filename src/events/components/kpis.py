import streamlit as st
from events.utils.helpers import get_events_df
from datetime import date
import duckdb

#KPI metric cards(showing diffferent counts)
df = get_events_df()


def total_events_kpi():
    cnt = duckdb.sql("SELECT COUNT(*) AS cnt FROM df").df()
    st.metric(label="Total Events", value=f"{cnt['cnt'].iloc[0]:,}")


def onsale_events_kpi():
    cnt = duckdb.sql("SELECT COUNT(*) AS cnt FROM df WHERE status = 'onsale'").df()
    st.metric(label="On Sale Now", value=f"{cnt['cnt'].iloc[0]:,}")


def upcoming_events_kpi():
    today = str(date.today())
    cnt = duckdb.sql(f"SELECT COUNT(*) AS cnt FROM df WHERE date >= '{today}'").df()
    st.metric(label="Upcoming", value=f"{cnt['cnt'].iloc[0]:,}")


def unique_venues_kpi():
    cnt = duckdb.sql("SELECT COUNT(DISTINCT venue_name) AS cnt FROM df").df()
    st.metric(label="Unique Venues", value=f"{cnt['cnt'].iloc[0]:,}")


def segment_event_count_kpi(segment: str, label: str = ""):
    cnt = duckdb.sql(f"""
        SELECT COUNT(*) AS cnt FROM df WHERE segment ILIKE '{segment}'
    """).df()
    st.metric(label=label, value=f"{cnt['cnt'].iloc[0]:,}")
