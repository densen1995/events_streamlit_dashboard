#Charts and tables 
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from events.utils.helpers import get_events_df
import duckdb
import pydeck as pdk

df = get_events_df()

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

 #Running SQL queries and building summary tables
   
df_by_segment = duckdb.sql("""
    SELECT segment, COUNT(*) AS event_count
    FROM df
    GROUP BY segment
    ORDER BY event_count DESC
""").df()

df_by_month_raw = duckdb.sql("""
    SELECT month_name, month_num, COUNT(*) AS event_count
    FROM df
    GROUP BY month_name, month_num
""").df()

# Merge against a full 12 month spine so every month always appears in order
month_spine = pd.DataFrame({"month_name": MONTH_ORDER, "month_num": range(1, 13)})
df_by_month = month_spine.merge(df_by_month_raw, on=["month_name", "month_num"], how="left").fillna(0)
df_by_month["event_count"] = df_by_month["event_count"].astype(int)

df_top_genres = duckdb.sql("""
    SELECT genre, COUNT(*) AS event_count
    FROM df
    GROUP BY genre
    ORDER BY event_count DESC
""").df()

df_top_venues = duckdb.sql("""
    SELECT venue_name, COUNT(*) AS event_count
    FROM df
    WHERE venue_name IS NOT NULL
    GROUP BY venue_name
    ORDER BY event_count DESC
""").df()


def bar_colors(values: pd.Series) -> list:
    """Green = highest bar, red = lowest bar, steel blue = everything else."""
    if len(values) == 0:
        return []
    max_v, min_v = values.max(), values.min()
    if max_v == min_v:
        return ["#3498db"] * len(values)
    return [
        "#2ecc71" if v == max_v else "#e74c3c" if v == min_v else "#3498db"
        for v in values
    ]


def add_color_legend(fig: go.Figure) -> go.Figure:
    fig.add_annotation(
        text="🟢 Highest  🔵 Middle  🔴 Lowest", #color badges from emoji picker
        xref="paper", yref="paper",
        x=1.0, y=-0.22,
        showarrow=False,
        font=dict(size=11, color="#555"),
        align="right",
    )
    return fig


#  Bar charts

def top_venues_chart(n: int = 8):
    dff = df_top_venues.head(n).sort_values("event_count", ascending=True)
    fig = go.Figure(go.Bar(
        x=dff["event_count"],
        y=dff["venue_name"],
        orientation="h",
        marker_color=bar_colors(dff["event_count"]),
        text=dff["event_count"],
        textposition="outside",
    ))
    fig.update_layout(
        title=dict(
    text=(
        "Top 8 Event Venues<br>"
        "<span style='font-size:16px; color:gray;'>"
        "Which venues host the most events?"
        "</span>"
    ),
    x=0
),
        xaxis_title="",
        yaxis_title="",
        height=400,
        margin=dict(b=100),
        xaxis= dict(title_standoff= 8),
    )
    add_color_legend(fig)
    with st.container(border=True):
        st.plotly_chart(fig, width="stretch")


# Line Charts 

def events_trend_line_chart():
    """Monthly trend — line with a marker dot and value label at every point."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_by_month["month_name"],
        y=df_by_month["event_count"],
        mode="lines+markers+text",
        text=df_by_month["event_count"],
        textposition="top center",
        textfont=dict(size=12, color="#1a1a2e"),
        marker=dict(
            size=11,
            color="#e63946",
            symbol="circle",
            line=dict(color="white", width=2),
        ),
        line=dict(color="#3498db", width=3),
        fill="tozeroy",
        fillcolor="rgba(52,152,219,0.08)",
    ))
    fig.update_layout(
        title=dict(
    text=(
        "Monthly Events Trend (Jan – Dec, 2026)<br>"
        "<span style='font-size:16px; color:gray;'>"
        "May shows a clear peak in activity🔥"
        "</span>"
    ),
    x=0.5
), 
        xaxis=dict(
            categoryorder="array",
            categoryarray=MONTH_ORDER,
            title="MONTH",
            tickangle=-30,
        ),
        yaxis_title="EVENT COUNT",
        height=420,
        showlegend=False,
        margin=dict(t=60, b=80),
    )
    with st.container(border=True):
        st.plotly_chart(fig, width="stretch")


# Pie Charts

def segment_pie_chart():
    fig = px.pie(
        df_by_segment,
        names="segment",
        values="event_count",
        title=(
        "Event Share by Segment<br>"
        
        "<span style='font-size:20px; color:gray;'>"
        "<sup>A few key segments dominate event participation, "
        "revealing where audience interest is strongest.</sup>"
    ),
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.35,
    )
    fig.update_traces(
        textinfo="percent+label",
        textfont_size=12,
        pull=[0.05] * len(df_by_segment),
    )
    fig.update_layout(height=380, margin=dict(t=60, b=40))
    with st.container(border=True):
        st.plotly_chart(fig, width="stretch")


def genre_pie_chart(n: int = 8):
    dff = df_top_genres.head(n)
    fig = px.pie(
        dff,
        names="genre",
        values="event_count",
        title=f"Top {n} Genres — Share",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hole=0.35,
    )
    fig.update_traces(
        textinfo="percent+label",
        textfont_size=11,
    )
    fig.update_layout(height=380, margin=dict(t=60, b=40))
    with st.container(border=True):
        st.plotly_chart(fig,width="stretch")


# Tables + Cards + Map 

def count_table_chart(feature: str, label: str = ""):
    dff = df[feature].value_counts()
    st.dataframe(dff, width="stretch")


def event_cards(df_filtered: pd.DataFrame):
    if df_filtered.empty:
        st.info("No events match your filters. Try adjusting the date range or segment.")
        return

    total = len(df_filtered)
    shown = min(total, 12)

    for _, row in df_filtered.head(shown).iterrows():
        col1, col2 = st.columns([1, 2])

        with col1:
            try:
                st.image(row["image_url"], width="stretch")
            except Exception:
                st.markdown("🎭 *Image unavailable*")

        with col2:
            status_badge = {
                "onsale": "🟢 On Sale",     #selected color badges with emoji pickers 
                "cancelled": "🔴 Cancelled",
                "rescheduled": "🟡 Rescheduled", 
                "offsale": "⚫ Off Sale",
            }.get(str(row["status"]).lower(), f"⚪ {row['status']}")

            date_str = (
                row["date"].strftime("%A, %B %d %Y")
                if hasattr(row["date"], "strftime")
                else str(row["date"])
            )
            time_val = row.get("time")
            time_str = (
                f" at {time_val}"
                if pd.notna(time_val) and str(time_val) not in ("nan", "")
                else ""
            )
            venue = row["venue_name"] if pd.notna(row.get("venue_name")) else "Unknown Venue"
            city = row["venue_city"] if pd.notna(row.get("venue_city")) else "Stockholm"

            st.markdown(f"### {row['name']}")
            st.markdown(f"**Date:** {date_str}{time_str}")
            st.markdown(f"**Venue:** {venue}, {city}")
            st.markdown(f"**Category:** {row['segment']} — {row['genre']}")
            st.markdown(f"**Status:** {status_badge}")
            st.link_button("🎟️ Get Tickets / More Info", row["url"])

        st.divider()

    if total > shown:
        st.caption(f"Showing {shown} of {total} events. Use filters to narrow your results.")

#Map using pydeck to get desired backgorund effect
def venue_map(df_filtered: pd.DataFrame):
    map_df = (
        df_filtered[["venue_lat", "venue_lon"]]
        .rename(columns={"venue_lat": "lat", "venue_lon": "lon"})
        .dropna()
    )
    if not map_df.empty:
        st.pydeck_chart(
            pdk.Deck(
                map_style="road",  
                initial_view_state=pdk.ViewState(
                    latitude=map_df["lat"].mean(),
                    longitude=map_df["lon"].mean(),
                    zoom=10,
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=map_df,
                        get_position="[lon, lat]",
                        get_radius=100,
                        get_color=[0, 120, 255],  # blue points
                    )
                ],
            )
        )
    else:
        st.info("No location data available.")