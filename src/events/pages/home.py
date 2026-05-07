#the home page with intro
import streamlit as st
from events.utils.helpers import read_textfile
from events.utils.constants import MARKDOWN_PATH, IMAGE_PATH
from events.components.charts import count_table_chart



#loads all content into the page (title,description, images, events breakdowns)
def home():
    st.image(IMAGE_PATH /"StockholmsPuls_HeroENG.png", width="stretch")
    st.markdown("# Stockholms Puls")
    st.markdown(read_textfile(MARKDOWN_PATH / "intro_events.md"))

    st.markdown("## Event Breakdowns")
    features = ("status", "day_of_week", "source", "segment")
    cols = st.columns(len(features))
    for col, feature in zip(cols, features):
        with col:
            st.markdown(f"**{feature.replace('_', ' ').title()}**")
            count_table_chart(feature=feature)


    
    st.image(IMAGE_PATH /"StockholmsPuls_FooterENG.webp", width="stretch")


if __name__ == "__main__":
    home()
