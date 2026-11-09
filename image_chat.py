import ollama

def analyze_image(image_path, prompt):

    response = ollama.chat(
        model="llava",
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [image_path]
            }
        ]
    )

    return response["message"]["content"]