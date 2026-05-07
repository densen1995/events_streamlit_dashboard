import streamlit as st
from events.utils.helpers import get_events_df
from events.utils.constants import  IMAGE_PATH

#the raw data page, loads the csv file and displays it as an interactive table
def raw_data():
    st.image(IMAGE_PATH /"StockholmsPuls_HeroENG.png", width="stretch")
    st.markdown("# Raw Data")
    st.markdown(f"**{len(get_events_df()):,} events** loaded from the dataset.")
    st.dataframe(get_events_df(), width="stretch")
    st.image(IMAGE_PATH /"StockholmsPuls_FooterENG.webp", width="stretch")


if __name__ == "__main__":
    raw_data()
