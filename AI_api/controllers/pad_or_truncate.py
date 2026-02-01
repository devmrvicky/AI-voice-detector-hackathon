import numpy as np

def pad_or_truncate(mel, max_len=300):
    """
    mel shape: (128, T)
    """
    current_len = mel.shape[1]

    if current_len > max_len:
        mel = mel[:, :max_len]
    else:
        pad_width = max_len - current_len
        mel = np.pad(
            mel,
            pad_width=((0, 0), (0, pad_width)),
            mode="constant"
        )

    return mel
