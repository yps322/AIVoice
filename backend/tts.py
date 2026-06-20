import edge_tts

async def speak(text, output_path="reply.mp3"):
    communicate = edge_tts.Communicate(
        text,
        "en-IN-NeerjaNeural"
    )

    await communicate.save(output_path)