import streamlit as st

# ========== 模拟数据 ==========
# Newsletter 发件人 (名称, 邮箱, 未读邮件数量)
mock_senders = [
    {"name": "Uber", "email": "uber@example.com", "unread": 100},
    {"name": "Postman", "email": "postman@example.com", "unread": 20},
    {"name": "IKEA", "email": "ikea@example.com", "unread": 6},
]

# 存储全局状态
if "page" not in st.session_state:
    st.session_state["page"] = "home"  # 首页 or 邮件详情页
if "selected_sender" not in st.session_state:
    st.session_state["selected_sender"] = None

# ========== 首页（展示所有 Newsletter 发送者） ==========
if st.session_state["page"] == "home":
    st.title("SmartMails - Your Newsletters, Organized!")

    # 1️⃣ 选择发件人（全选/多选）
    st.subheader("Newsletter Senders")

    col1, col2, col3, col4 = st.columns([1, 3, 3, 2])

    with col1:
        select_all = st.checkbox("All")

    with col2:
        st.write("Sender Name")

    with col3:
        st.write("Email Address")

    with col4:
        st.write("Unread Emails")

    selected_senders = []
    for sender in mock_senders:
        with col1:
            checked = st.checkbox("", key=sender["email"], value=select_all)
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
            st.write(sender["unread"])

    # 2️⃣ 批量操作按钮
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Delete Selected Senders' Emails"):
            if selected_senders:
                st.success(f"Deleted all emails from: {', '.join(selected_senders)}")
            else:
                st.warning("Please select at least one sender.")

    with col2:
        if st.button("Unsubscribe Selected Senders"):
            if selected_senders:
                st.success(f"Unsubscribed from: {', '.join(selected_senders)}")
            else:
                st.warning("Please select at least one sender.")

    with col3:
        if st.button("Mark All as Read"):
            if selected_senders:
                st.success(f"Marked all emails as read from: {', '.join(selected_senders)}")
            else:
                st.warning("Please select at least one sender.")

# ========== 邮件详情页 ==========
elif st.session_state["page"] == "details":
    sender = st.session_state["selected_sender"]
    st.title(f"Emails from {sender['name']} ({sender['email']})")

    # 模拟该发件人的邮件数据
    mock_emails = [
        {"id": "1", "subject": "Monthly Ride Summary"},
        {"id": "2", "subject": "Exclusive Offer for You!"},
        {"id": "3", "subject": "Your Weekly Newsletter"},
    ]

    # 选中的邮件
    col1, col2 = st.columns([1, 5])
    with col1:
        select_all_emails = st.checkbox("All Emails")
    with col2:
        st.write("Email Subject")

    selected_emails = []
    for email in mock_emails:
        with col1:
            checked = st.checkbox("", key=email["id"], value=select_all_emails)
            if checked:
                selected_emails.append(email["id"])

        with col2:
            st.write(email["subject"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete Selected Emails"):
            if selected_emails:
                st.success(f"Deleted {len(selected_emails)} emails from {sender['name']}")
            else:
                st.warning("Please select at least one email.")

    with col2:
        if st.button("Mark Selected Emails as Read"):
            if selected_emails:
                st.success(f"Marked {len(selected_emails)} emails as read from {sender['name']}")
            else:
                st.warning("Please select at least one email.")

    # 返回按钮
    if st.button("Back to Senders List"):
        st.session_state["page"] = "home"
        st.rerun()
