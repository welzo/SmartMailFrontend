import streamlit as st

def show():
    st.title("Top Senders")

    # 获取存储的日期和 Top N
    start_date = st.session_state.get("start_date", "2024-01-01")
    top_n = st.session_state.get("top_n", 10)

    # ✅ 使用 Mock 数据（暂时不请求后端）
    senders_data = st.session_state.get("senders_data", [])

    if senders_data:
        st.success(f"Showing top {top_n} senders since {start_date}")

        # ✅ 让 Streamlit 控制按钮的跳转逻辑
        col1, col2, col3, col4 = st.columns([1, 3, 5, 2])
        with col1:
            select_all = st.checkbox("All", key="select_all")

        with col2:
            st.write("Sender Name")

        with col3:
            st.write("Email Address")

        with col4:
            st.write("Unread Emails")

        # 选中的发件人
        selected_senders = []
        for sender in senders_data:
            with col1:
                checked = st.checkbox("", key=f"check_{sender['email']}", value=select_all)
                if checked:
                    selected_senders.append(sender["email"])

            with col2:
                # ✅ 使用 `st.button()` 让按钮可以跳转
                if st.button(sender["name"], key=f"btn_{sender['email']}"):
                    st.session_state["selected_sender"] = sender
                    st.session_state["page"] = "details"
                    st.rerun()  # ✅ Streamlit 重新加载页面

            with col3:
                st.write(sender["email"])

            with col4:
                st.write(sender["unread"])

        # 2️⃣ 添加操作按钮（删除 & 标为已读）
        col1, col2 = st.columns(2)

        with col1:
            if st.button("❌ Delete Selected Senders' Emails"):
                if selected_senders:
                    st.success(f"Deleted all emails from: {', '.join(selected_senders)}")
                else:
                    st.warning("Please select at least one sender.")

        with col2:
            if st.button("✅ Mark All as Read"):
                if selected_senders:
                    st.success(f"Marked all emails as read from: {', '.join(selected_senders)}")
                else:
                    st.warning("Please select at least one sender.")

    # 3️⃣ 返回首页
    if st.button("⬅️ Back to Home"):
        st.session_state["page"] = "home"
        st.rerun()
