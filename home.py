import streamlit as st
import datetime


def show():
    st.title("Smart News Cleaner")

    # 1️⃣ 选择日期
    st.subheader("Filter Emails by Date")
    start_date = st.date_input("Select Start Date", datetime.date.today())

    # 2️⃣ 选择 Top N 发件人
    top_n = st.number_input("Show Top Senders", min_value=5, max_value=50, value=10, step=1)

    # 3️⃣ 获取数据按钮
    if st.button("Get Emails Data"):
        st.session_state["start_date"] = str(start_date)
        st.session_state["top_n"] = top_n
        st.session_state["page"] = "top_senders"
        st.session_state["senders_data"] = [
            {"name": "Uber", "email": "uber@example.com", "unread": 100},
            {"name": "Postman", "email": "postman@example.com", "unread": 20},
            {"name": "IKEA", "email": "ikea@example.com", "unread": 6},
        ]
        st.rerun()

