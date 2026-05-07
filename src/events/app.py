#the entrypoint that runs the app
import streamlit as st

#defines a list of pages
pages = [
    st.Page("pages/home.py", title="Home"),
    st.Page("pages/dashboard.py", title="Dashboard"),
    st.Page("pages/raw_data.py", title="Raw Data"),
]

pg = st.navigation(pages) #builds sidebar navigaion menu from list
pg.run()  #runs the page the user has selected
