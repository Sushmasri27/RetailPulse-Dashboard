import streamlit as st

from chatbot import get_response
from document_reader import (
    read_pdf,
    read_docx,
    read_txt
)


def show_document_page():

    st.title("📄 AI Document Assistant")

    uploaded_file = st.file_uploader(
        "Upload PDF, DOCX or TXT",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file is None:
        return

    if uploaded_file.name.endswith(".pdf"):
        document_text = read_pdf(uploaded_file)

    elif uploaded_file.name.endswith(".docx"):
        document_text = read_docx(uploaded_file)

    else:
        document_text = read_txt(uploaded_file)

    st.success("Document uploaded successfully!")

    st.subheader("Preview")

    st.text_area(
        "",
        document_text[:3000],
        height=250
    )

    question = st.text_input(
        "Ask a question about the document"
    )

    if st.button("Ask AI"):

        with st.spinner("Thinking..."):

            messages = [
                {
                    "role": "user",
                    "content": question
                }
            ]

            answer = get_response(
                messages,
                document_text
            )

        st.subheader("Answer")

        st.write(answer)