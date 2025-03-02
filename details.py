import streamlit as st
import urllib.parse

def show():
    if "selected_sender" not in st.session_state:
        st.warning("No sender selected. Go back to the main page.")
        st.stop()

    sender = st.session_state["selected_sender"]
    st.title(f"Emails from {sender['name']} ({sender['email']})")

    # Use fetched emails if available, otherwise fallback to static sample data
    if "selected_sender_details" in st.session_state:
        # Expecting the fetched details to be a list of emails with keys: email_id, subject, and priority
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

    # If your backend already prioritized the emails, you might not need to re-sort them.
    # But if you want to enforce an order (say, highest priority first), you can do so:
    # For example, if priority is numeric (e.g., 1-10), you might want to sort like:
    email_data.sort(key=lambda x: x["priority"], reverse=False)  # Adjust based on your logic

    if not email_data:
        st.warning("No emails found.")
        st.stop()

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
            # Use a unique key for each checkbox, based on the email_id
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
                # Fallback if 'priority' isn't an integer
                priority_text = str(priority_value)

            st.write(priority_text)

    # Operations on selected emails
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete Selected Emails"):
            if selected_emails:
                # Remove emails whose email_id is in selected_emails.
                st.session_state["selected_sender_details"] = [
                    email for email in email_data if email["email_id"] not in selected_emails
                ]
                st.success(f"Deleted {len(selected_emails)} emails from {sender['name']}")
                st.rerun()

    with col2:
        if st.button("Mark Selected Emails as Read"):
            if selected_emails:
                # You can trigger your backend mark-as-read action here.
                st.success(f"Marked {len(selected_emails)} emails as read from {sender['name']}")
                st.rerun()

    # Back button to go to top senders page
    if st.button("Back to Top Senders"):
        st.session_state["page"] = "top_senders"
        st.rerun()
