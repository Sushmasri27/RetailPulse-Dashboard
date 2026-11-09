import ollama


def get_response(messages, document_text=""):
    """
    messages = [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
    ]
    """

    chat_messages = []

    # System prompt
    if document_text:
        system_prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the uploaded documents.

Documents:

{document_text}

If the answer is not present in the documents, clearly say:
'I couldn't find that information in the uploaded documents.'
"""
    else:
        system_prompt = """
You are a helpful AI assistant.

Remember the previous conversation and answer naturally.

If the user asks things like:
- Explain briefly
- Give a short answer
- Continue
- Explain more
- Summarize

use the previous conversation as context.
"""

    chat_messages.append(
        {
            "role": "system",
            "content": system_prompt
        }
    )

    chat_messages.extend(messages)

    response = ollama.chat(
        model="llama3.2",
        messages=chat_messages
    )

    return response["message"]["content"]


def stream_response(messages, document_text=""):

    chat_messages = []

    if document_text:
        system_prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the uploaded documents.

Documents:

{document_text}

If the answer is not present in the documents, say:
'I couldn't find that information in the uploaded documents.'
"""
    else:
        system_prompt = """
You are a helpful AI assistant.

Remember the previous conversation while answering.
"""

    chat_messages.append(
        {
            "role": "system",
            "content": system_prompt
        }
    )

    chat_messages.extend(messages)

    stream = ollama.chat(
        model="llama3.2",
        messages=chat_messages,
        stream=True
    )

    for chunk in stream:
        yield chunk["message"]["content"]

def generate_chat_title(prompt):

    response = ollama.chat(
        model="llama3.2",
        messages=[
           {
               "role": "system",
                "content": (
                    "Generate a very short chat title. "
                    "Use only 2 or 3 words. "
                    "Return only the title. "
                    "Examples:\n"
                    "Explain Python decorators -> Python Decorators\n"
                    "Write Java program -> Java Program\n"
                    "Summarize this PDF -> PDF Summary\n"
                    "Describe this image -> Image Analysis"
                
                )
           },
           {
                "role": "user",
                "content": prompt
           }
        ]
    )

    return response["message"]["content"].strip()