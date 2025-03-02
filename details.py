import streamlit as st

def show():
    if "selected_sender" not in st.session_state:
        st.warning("No sender selected. Go back to the main page.")
        st.stop()

    sender = st.session_state["selected_sender"]
    st.title(f"Emails from {sender['name']} ({sender['email']})")

    # ✅ 检查 `st.session_state` 里是否已经存了邮件数据
    if "email_data" not in st.session_state:
        # ✅ 只在第一次进入页面时生成数据，并存入 `session_state`
        email_data = [
            {"id": "1", "subject": "Monthly Ride Summary", "priority": "High"},
            {"id": "2", "subject": "Exclusive Offer for You!", "priority": "Medium"},
            {"id": "3", "subject": "Your Weekly Newsletter", "priority": "Low"},
            {"id": "4", "subject": "Important Account Update", "priority": "High"},
            {"id": "5", "subject": "Limited Time Deal!", "priority": "Medium"},
        ]
        st.session_state["email_data"] = email_data
    else:
        # ✅ 直接从 `session_state` 读取邮件数据，避免优先级变化
        email_data = st.session_state["email_data"]

    # ✅ 按照 `Priority` 从高到低排序
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    email_data.sort(key=lambda x: priority_order[x["priority"]])

    if not email_data:
        st.warning("No emails found.")
        st.stop()

    # ✅ 选中的邮件
    col1, col2, col3 = st.columns([1, 5, 2])
    with col1:
        select_all_emails = st.checkbox("Select All")
    with col2:
        st.write("Email Subject")
    with col3:
        st.write("Priority")

    selected_emails = []
    for email in email_data:
        with col1:
            checked = st.checkbox("", key=email["id"], value=select_all_emails)
            if checked:
                selected_emails.append(email["id"])
        with col2:
            st.write(email["subject"])
        with col3:
            # ✅ 让 Priority 有不同颜色
            priority_color = {
                "High": "🔴 High",
                "Medium": "🟡 Medium",
                "Low": "🟢 Low"
            }
            st.write(priority_color[email["priority"]])

    # ✅ 操作按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete Selected Emails"):
            if selected_emails:
                # ✅ 删除邮件时，同时更新 `session_state`
                st.session_state["email_data"] = [email for email in email_data if email["id"] not in selected_emails]
                st.success(f"Deleted {len(selected_emails)} emails from {sender['name']}")
                st.rerun()

    with col2:
        if st.button("Mark Selected Emails as Read"):
            if selected_emails:
                st.success(f"Marked {len(selected_emails)} emails as read from {sender['name']}")
                st.rerun()

    # ✅ 返回按钮
    if st.button("Back to Top Senders"):
        st.session_state["page"] = "top_senders"
        st.rerun()
