import whisper

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model


def transcribe_audio(audio_path: str) -> str:
    model = _get_model()
    result = model.transcribe(audio_path)
    return result["text"]