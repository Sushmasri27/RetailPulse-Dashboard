import whisper
import tempfile
import os

# Load the model only once
model = whisper.load_model("small")


def speech_to_text(audio_bytes):
    try:
        # Save the audio exactly as received
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
            f.write(audio_bytes)
            temp_path = f.name

        result = model.transcribe(
            temp_path,
            language="en",
            fp16=False
        )

        text = result["text"].strip()

        os.remove(temp_path)

        print("Recognized:", text)

        return text

    except Exception as e:
        print("Speech Error:", e)
        return ""