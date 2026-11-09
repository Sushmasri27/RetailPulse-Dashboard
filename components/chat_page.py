import streamlit as st
from image_chat import analyze_image
from streamlit_javascript import st_javascript
from document_reader import read_pdf, read_docx, read_txt
from chatbot import stream_response, generate_chat_title
from rag import (
    store_document,
    search_document,
    has_documents,
    clear_documents
)
from sentiment import analyze_sentiment
from database import (
    save_message,
    update_conversation_title
)
from utils import export_chat_txt, export_chat_pdf
from speech_input import speech_to_text
from streamlit_mic_recorder import mic_recorder

def show_chat_page():

    # Initialize messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "document_text" not in st.session_state:
        st.session_state.document_text = ""

    if "document_names" not in st.session_state:
        st.session_state.document_names = [] 
    st.title("🤖 Dynamic AI Assistant")
    use_documents = st.toggle(
        "📄 Use uploaded documents",
        value=False
    )
    st.markdown("""
    <style>

    div[data-testid="stTextInput"] input{

        border-radius:30px;

        padding:12px;

        font-size:17px;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- Export Entire Chat ---------------- #

    if st.session_state.messages:

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "📄 Export Chat (TXT)",
                data=export_chat_txt(st.session_state.messages),
                file_name="chat_history.txt",
                mime="text/plain"
            )

        with col2:
            st.download_button(
                "📕 Export Chat (PDF)",
                data=export_chat_pdf(st.session_state.messages),
                file_name="chat_history.pdf",
                mime="application/pdf"
            )

    # ---------------- Welcome Message ---------------- #

    if len(st.session_state.messages) == 0:

        st.info("""
👋 Welcome!

I can help you with:

- Answer questions
- Explain programming
- Summarize documents
- Write code
- Brainstorm ideas

Type a message below to begin.
""")

    # ---------------- Display Chat History ---------------- #

    for i, message in enumerate(st.session_state.messages):

        avatar = "👤" if message["role"] == "user" else "🤖"

        with st.chat_message(message["role"], avatar=avatar):

            st.markdown(message["content"])

            if message["role"] == "assistant":

                c1, c2, c3 = st.columns([1, 1, 1])

                with c1:

                    if st.button("📋 Copy", key=f"copy_{i}"):

                        js = f"""
                        navigator.clipboard.writeText({repr(message["content"])});
                        """

                        st_javascript(js)
                        st.success("Copied!")

                with c2:

                    st.download_button(
                        "📄 Download",
                        data=message["content"],
                        file_name=f"response_{i}.txt",
                        mime="text/plain",
                        key=f"download_{i}"
                    )

                with c3:

                    if st.button("🔄 Regenerate", key=f"regen_{i}"):

                        st.session_state.messages = st.session_state.messages[:i]
                        st.rerun()

        # ---------------- Voice Input ---------------- #


    c1, c2, c3, c4 = st.columns([1, 10, 1, 1])

    with c1:
       with st.popover("➕"):

           st.write("### Attach Files")

           uploaded_docs = st.file_uploader(
              "📄 Upload Documents",
              type=["pdf", "docx", "txt"],
              accept_multiple_files=True,
              key="documents"
            )
           if uploaded_docs:

               st.session_state.document_text = ""
               st.session_state.document_names = []

               for file in uploaded_docs:

                   st.session_state.document_names.append(file.name)

                   if file.name.endswith(".pdf"):

                       pdf_pages = read_pdf(file)

                       store_document(pdf_pages, file.name)


                   elif file.name.endswith(".docx"):
                      st.session_state.document_text += read_docx(file)

                   elif file.name.endswith(".txt"):
                      st.session_state.document_text += read_txt(file)
               
               st.success(f"✅ {len(uploaded_docs)} document(s) uploaded successfully!")

           uploaded_images = st.file_uploader(
               "🖼 Upload Images",
               type=["png", "jpg", "jpeg"],
               accept_multiple_files=True,
               key="images"
            )
           import tempfile

           image_paths = []

           if uploaded_images:

              for image in uploaded_images:

                temp = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".png"
                )

                temp.write(image.read())
                temp.close()

                image_paths.append(temp.name)

              st.success(f"✅ {len(uploaded_images)} image(s) uploaded!") 

           picture = st.camera_input("📷 Take Photo")
           camera_image_path = None

           if picture:

            temp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".png"
            )

            temp.write(picture.read())
            temp.close()

            camera_image_path = temp.name

            st.success("📷 Camera image captured!")
           if st.session_state.document_names:
              st.info("📎 Attached: " + ", ".join(st.session_state.document_names))

              if st.button("🗑️ Clear Documents"):
                 clear_documents()
                 st.session_state.document_names = []
                 st.rerun()

    with c2:
        prompt = st.text_input(
            "",
            placeholder="Ask anything...",
            label_visibility="collapsed",
            key="chat_input"
        )

    with c3:

        audio = mic_recorder(
            start_prompt="🎤",
            stop_prompt="⏹",
            just_once=True,
            key="mic"
        )

    with c4:

        send_clicked = st.button(
            "➤",
            use_container_width=True
        )
        # ---------------- Attachment Menu ---------------- #

    

    # Use microphone input if available
    if audio:

    # Show the complete audio information

      audio_bytes = audio.get("bytes")

      if audio_bytes:

        with st.spinner("🎤 Transcribing..."):

            voice_text = speech_to_text(audio_bytes)

            if voice_text:
                prompt = voice_text
                st.success(f"You said: {voice_text}")
            else:
                st.warning("Couldn't recognize your speech. Please try again.")

    if not (send_clicked or audio):
        return

    if not prompt:
      return

    # Create messages for AI
    messages_for_ai = st.session_state.messages.copy()

    if use_documents and has_documents():
       search_result = search_document(prompt)

       relevant_text = search_result["text"]

       source_chunks = search_result["chunks"]

       source_metadata = search_result["metadata"]
       ai_prompt = f"""
Use ONLY the following extracted document content to answer.

    {relevant_text}

    User Question:
    {prompt}
    """

    else:
        ai_prompt = prompt

    # Save only the user's question in chat history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Create AI messages
    messages_for_ai.append(
        {
            "role": "user",
            "content": ai_prompt
        }
    )

    if len(st.session_state.messages) == 1:

       title = generate_chat_title(prompt)
       if len(title) > 20:
            title = title[:20] + "..."

       update_conversation_title(
            st.session_state.conversation_id,
            title
        )
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # ---------------- AI Response ---------------- #

    with st.chat_message("assistant", avatar="🤖"):

        placeholder = st.empty()
        full_response = ""

        if image_paths:

           full_response = analyze_image(
               image_paths[0],
               prompt
            )
           placeholder.markdown(full_response)

        elif camera_image_path:

            full_response = analyze_image(
                camera_image_path,
                prompt
            )

            placeholder.markdown(full_response)

        else:

            for chunk in stream_response(messages_for_ai):
                full_response += chunk
                placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

    # ---------------- Save Assistant Response ---------------- #

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )
    if use_documents and has_documents():

       st.markdown("### 📄 Sources")

       shown = set()

       for meta in source_metadata:

           if meta is None:
               continue

           source = f"{meta['file']} — Page {meta['page']}"

           if source not in shown:
               shown.add(source)
               st.write(f"📄 {source}")

    sentiment = analyze_sentiment(prompt)

    save_message(
        st.session_state.conversation_id,
        "user",
        prompt,
        sentiment
    )

    save_message(
        st.session_state.conversation_id,
        "assistant",
        full_response,
        sentiment
    ) 