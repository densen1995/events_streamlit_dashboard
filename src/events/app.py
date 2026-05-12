#the entrypoint that runs the app
import streamlit as st
st.set_page_config(
    page_title= "Stockholms Puls",
    page_icon= "🎭",
    layout= "wide"
)
#defines a list of pages
pages = [
    st.Page("pages/home.py", title="Stockholms Puls"),
    st.Page("pages/dashboard.py", title="Events"),
    st.Page("pages/insights.py", title= "Insights"),
    st.Page("pages/raw_data.py", title="Raw Data"),
]

pg = st.navigation(pages) #builds sidebar navigaion menu from list
pg.run()  #runs the page the user has selected
