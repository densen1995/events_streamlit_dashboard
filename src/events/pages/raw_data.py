import streamlit as st
from events.utils.helpers import get_events_df

#the raw data page, loads the csv file and displays it as an interactive table
def raw_data():
    st.markdown("# Raw Data")
    st.markdown(f"**{len(get_events_df()):,} events** loaded from the dataset.")
    st.dataframe(get_events_df(), use_container_width=True)


if __name__ == "__main__":
    raw_data()
