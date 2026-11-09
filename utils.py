from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io


def export_chat_txt(messages):
    text = ""

    for msg in messages:
        role = "You" if msg["role"] == "user" else "AI"

        text += f"{role}: {msg['content']}\n\n"

    return text


def export_chat_pdf(messages):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    for msg in messages:

        role = "You" if msg["role"] == "user" else "AI"

        story.append(
            Paragraph(
                f"<b>{role}:</b> {msg['content']}",
                styles["Normal"]
            )
        )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf