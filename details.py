import streamlit as st
import urllib.parse
import requests

def show():
    if "selected_sender" not in st.session_state:
        st.warning("No sender selected. Go back to the main page.")
        st.stop()

    sender = st.session_state["selected_sender"]
    st.title(f"Emails from {sender['name']} ({sender['email']})")

    # Use fetched emails if available, otherwise fallback to static sample data
    if "selected_sender_details" in st.session_state:
        email_data = st.session_state["selected_sender_details"]
    else:
        st.warning("No email details available. Showing sample data.")
        email_data = [
            {"email_id": "1", "subject": "Monthly Ride Summary", "priority": "High"},
            {"email_id": "2", "subject": "Exclusive Offer for You!", "priority": "Medium"},
            {"email_id": "3", "subject": "Your Weekly Newsletter", "priority": "Low"},
            {"email_id": "4", "subject": "Important Account Update", "priority": "High"},
            {"email_id": "5", "subject": "Limited Time Deal!", "priority": "Medium"},
        ]

    # Sort email_data if needed
    email_data.sort(key=lambda x: x["priority"], reverse=False)

    # Check if there are emails to display
    if email_data:
        # Layout the email details with a table-like view
        col1, col2, col3 = st.columns([1, 5, 2])
        with col1:
            select_all_emails = st.checkbox("Select All")
        with col2:
            st.write("Email Subject")
        with col3:
            st.write("Spam Level")

        selected_emails = []
        for email in email_data:
            with col1:
                checked = st.checkbox("", key=email["email_id"], value=select_all_emails)
                if checked:
                    selected_emails.append(email["email_id"])
            with col2:
                st.write(email["subject"])
            with col3:
                priority_value = email["priority"]
                if isinstance(priority_value, int):
                    if priority_value >= 8:
                        priority_text = f"🔴"
                    elif priority_value <= 5:
                        priority_text = f"🟢"
                    else:
                        priority_text = f"🟡"
                else:
                    priority_text = str(priority_value)
                st.write(priority_text)

        # Operations on selected emails
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Delete Selected Emails"):
                if selected_emails:
                    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
                    errors = []
                    for email_id in selected_emails:
                        encoded_email_id = urllib.parse.quote_plus(email_id)
                        url = f"http://localhost:8080/trash_email_by_id?email_id={encoded_email_id}"
                        try:
                            response = requests.get(url, headers=headers)
                            if response.status_code == 200:
                                st.write(f"Email {email_id} moved to trash successfully.")
                                st.session_state.pop("senders_data", None)
                            else:
                                error_detail = response.json().get("details", "Unknown error")
                                errors.append(f"Error deleting {email_id}: {error_detail}")
                        except Exception as e:
                            errors.append(f"Error deleting {email_id}: {e}")
                    if errors:
                        st.error("\n".join(errors))
                    else:
                        st.success(f"Deleted {len(selected_emails)} emails from {sender['name']}")
                    st.session_state["selected_sender_details"] = [
                        email for email in email_data if email["email_id"] not in selected_emails
                    ]
                    st.rerun()

        with col2:
            if st.button("Mark Selected Emails as Read"):
                if selected_emails:
                    st.success(f"Marked {len(selected_emails)} emails as read from {sender['name']}")
                    st.rerun()
    else:
        st.warning("No emails found.")

    # The Back button is placed outside the email check, so it's always visible.
    if st.button("Back to Top Senders"):
        st.session_state["page"] = "top_senders"
        st.rerun()
