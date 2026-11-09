import streamlit as st
from streamlit_option_menu import option_menu

from database import (
    create_new_conversation,
    get_all_conversations,
    load_messages,
    rename_conversation,
    delete_conversation
)


def show_sidebar():

    with st.sidebar:

        st.title("🤖 Dynamic AI Assistant")

        page = option_menu(
            menu_title="Navigation",
            options=[
                "Chat",
                "Analytics",
                "Document Assistant",
                "About"
            ],
            icons=[
                "house-fill",
                "bar-chart-fill",
                "file-earmark-text-fill",
                "info-circle-fill"
            ],
            default_index=0
        )

        st.divider()

        if st.button("➕ New Chat", use_container_width=True):

            st.session_state.messages = []

            st.session_state.conversation_id = create_new_conversation()

            st.rerun()

        st.divider()

        st.subheader("💬 Chat History")

        search = st.text_input(
            "🔍 Search Chats",
            placeholder="Search..."
        )

        conversations = get_all_conversations()

        for conversation in conversations:

            conversation_id = conversation[0]
            title = conversation[1]

            if search and search.lower() not in title.lower():
               continue

            col1, col2 = st.columns([5, 1])

            with col1:

                if st.button(
                   f"💬 {title}",
                   key=f"chat_{conversation_id}",
                   use_container_width=True
                ):

                   st.session_state.conversation_id = conversation_id

                   rows = load_messages(conversation_id)

                   st.session_state.messages = [
                      {
                        "role": role,
                        "content": message
                      }
                      for role, message in rows
                   ]

                   st.rerun()

            with col2:

              with st.popover("⋮"):

                new_title = st.text_input(
                    "Rename",
                    value=title,
                    key=f"rename_{conversation_id}"
                )

                if st.button(
                     "Save",
                    key=f"save_{conversation_id}"
                ):

                    rename_conversation(
                       conversation_id,
                       new_title
                    )

                    st.rerun()

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{conversation_id}"
                ):

                    delete_conversation(conversation_id)

                    if st.session_state.conversation_id == conversation_id:

                       st.session_state.messages = []
                       st.session_state.conversation_id = create_new_conversation()

                    st.rerun()
    return page