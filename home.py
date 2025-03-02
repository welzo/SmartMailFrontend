# home.py
import streamlit as st
import datetime
import requests

def show():
    st.title("Smart News Cleaner")
    
    # Read query parameters on every run
    query_params = st.experimental_get_query_params()
    if "access_token" in query_params:
        st.session_state["access_token"] = query_params["access_token"][0]
        # Clear the query parameters so they aren’t processed repeatedly.
        st.experimental_set_query_params()
    
    if "access_token" not in st.session_state:
        st.info("You must authenticate first. Click the link below:")
        st.markdown("[Authenticate here](http://localhost:8080/authorize)")
        st.stop()
    
    st.subheader("Filter Emails by Date")
    start_date = st.date_input("Select Start Date", datetime.date.today())
    top_n = st.number_input("Show Top Senders", min_value=5, max_value=50, value=10, step=1)
    
    if st.button("Get Emails Data"):
        st.session_state["start_date"] = str(start_date)
        st.session_state["top_n"] = top_n
        
        url = f"http://localhost:8080/top_senders?date={start_date}&limit={top_n}"
        headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.session_state["senders_data"] = data
                # Switch to the top_senders page and rerun.
                st.session_state["page"] = "top_senders"
                st.rerun()
            else:
                st.error(f"Error fetching data: HTTP {response.status_code}")
        except Exception as e:
            st.error(f"Request failed: {e}")
