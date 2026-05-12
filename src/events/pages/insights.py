import streamlit as st
from events.utils.helpers import read_textfile, read_css, get_events_df
from events.utils.constants import MARKDOWN_PATH, STYLE_PATH, IMAGE_PATH
from events.components.charts import (
    events_trend_line_chart,
    top_venues_chart,
    segment_pie_chart,
    genre_pie_chart,
)


def insights():
    st.image(IMAGE_PATH /"StockholmsPuls_HeroENG.png", width="stretch")
    st.markdown("# View Insights")



    # Segment pie (full width)
    segment_pie_chart()

     # Month line trend (full width, markers and value labels)
    events_trend_line_chart()

    # Genres pie and Venues bar side by side
    col1, col2 = st.columns(2)
    with col1:
        genre_pie_chart(8)
    with col2:
        top_venues_chart(7)   

    st.image(IMAGE_PATH /"StockholmsPuls_FooterENG.webp", width="stretch")

    read_css(STYLE_PATH / "dashboard.css") # injects custom CSS to style the dashboard.

if __name__ == "__main__":
    insights()