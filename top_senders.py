import streamlit as st
import urllib.parse
import requests

def show():
    st.title("Top Senders")

    start_date = st.session_state.get("start_date", "2024-01-01")
    top_n = st.session_state.get("top_n", 10)
    senders_data = st.session_state.get("senders_data", [])

    if senders_data:
        st.success(f"Showing top {top_n} senders since {start_date}")

        # HEADER ROW: Display column headers.
        colH1, colH2, colH3, colH4 = st.columns([1, 3, 5, 2])
        with colH1:
            st.markdown("<p style='text-align:center; font-weight:bold;'>All</p>", unsafe_allow_html=True)
            select_all = st.checkbox("", key="select_all", label_visibility="hidden")
        with colH2:
            st.markdown("<p style='font-weight:bold;'>Sender Name</p>", unsafe_allow_html=True)
        with colH3:
            st.markdown("<p style='font-weight:bold;'>Email Address</p>", unsafe_allow_html=True)
        with colH4:
            st.markdown("<p style='font-weight:bold;'>Unread Emails</p>", unsafe_allow_html=True)

        selected_senders = []
        for sender in senders_data:
            col1, col2, col3, col4 = st.columns([1, 3, 5, 2])
            with col1:
                checked = st.checkbox("", key=f"check_{sender['email']}", value=select_all, label_visibility="hidden")
                if checked:
                    selected_senders.append(sender["email"])
            with col2:
                if st.button(sender["name"], key=f"btn_{sender['email']}"):
                    st.session_state["selected_sender"] = sender
                    st.session_state["page"] = "details"
                    st.rerun()
            with col3:
                st.write(sender["email"])
            with col4:
                st.write(sender["unread_count"])

        colB1, colB2 = st.columns(2)
        with colB1:
            if st.button("❌ Delete Selected Senders' Emails"):
                if selected_senders:
                    success_count = 0
                    for email in selected_senders:
                        # URL encode the email
                        encoded_email = urllib.parse.quote_plus(email)
                        trash_url = f"http://localhost:8080/trash_emails?sender={encoded_email}"
                        headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
                        r = requests.get(trash_url, headers=headers)
                        if r.status_code == 200:
                            success_count += 1
                        else:
                            st.error(f"Failed to delete emails for {email}: HTTP {r.status_code}")
                    if success_count:
                        st.success(f"Deleted emails for {success_count} sender(s): {', '.join(selected_senders)}")
                        # Remove the deleted senders from session data.
                        st.session_state["senders_data"] = [
                            sender for sender in st.session_state["senders_data"]
                            if sender["email"] not in selected_senders
                        ]
                        st.rerun()
                else:
                    st.warning("Please select at least one sender.")
        with colB2:
            if st.button("✅ Mark All as Read"):
                if selected_senders:
                    success_count = 0
                    for email in selected_senders:
                        encoded_email = urllib.parse.quote_plus(email)
                        mark_url = f"http://localhost:8080/mark_as_read?sender={encoded_email}"
                        headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
                        r = requests.get(mark_url, headers=headers)
                        if r.status_code == 200:
                            success_count += 1
                        else:
                            st.error(f"Failed to mark emails as read for {email}: HTTP {r.status_code}")
                    if success_count:
                        st.success(f"Marked emails as read for {success_count} sender(s): {', '.join(selected_senders)}")
                        st.session_state["senders_data"] = [
                            sender for sender in st.session_state["senders_data"]
                            if sender["email"] not in selected_senders
                        ]
                        # Optionally, update your senders_data or refresh the data from backend.
                        # st.session_state["senders_data"] = <fetch updated data from /top_senders endpoint>
                        st.rerun()
                else:
                    st.warning("Please select at least one sender.")
    else:
        st.warning("No sender data available.")

    if st.button("⬅️ Back to Home"):
        st.session_state["page"] = "home"
        st.rerun()
