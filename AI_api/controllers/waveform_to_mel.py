import numpy as np
import librosa

def waveform_to_mel(audio, sr):
    mel_spec = librosa.feature.melspectrogram(
        y=audio,
        sr=sr,
        n_fft=1024,
        hop_length=512,
        n_mels=128,
        fmin=0,
        fmax=sr // 2
    )

    # Convert power → decibel (log scale)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

    return mel_spec_db
