import requests;
from urllib.parse import urlparse;
import librosa
import io

def is_valid_url(url: str):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except Exception:
    return False

def load_audio_from_url(audio_url: str):
    try:
        response = requests.get(audio_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        raise ValueError("Failed to download audio")

    audio_bytes = io.BytesIO(response.content)

    try:
        audio, sr = librosa.load(
            audio_bytes,
            sr=16000,
            mono=True
        )
    except Exception:
        raise ValueError("Failed to decode audio")

    return audio, sr

