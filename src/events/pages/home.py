#the home page with intro
import streamlit as st
from events.utils.helpers import read_textfile
from events.utils.constants import MARKDOWN_PATH, IMAGE_PATH



#loads all content into the page (title,description, images)
def home():
    st.markdown("# Stockholm Puls")
    st.image(IMAGE_PATH /"StockholmsPuls_HeroENG.png", use_container_width=True)
    st.markdown(read_textfile(MARKDOWN_PATH / "intro_events.md"))
    st.image(IMAGE_PATH /"StockholmsPuls_FooterENG.webp", use_container_width=True)


if __name__ == "__main__":
    home()
