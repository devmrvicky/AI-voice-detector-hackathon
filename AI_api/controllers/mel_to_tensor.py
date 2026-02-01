import torch

def mel_to_tensor(mel):
    """
    Output shape: (1, 1, 128, 300)
    """
    tensor = torch.tensor(mel, dtype=torch.float32)
    tensor = tensor.unsqueeze(0)  # batch dimension
    tensor = tensor.unsqueeze(0)  # channel dimension
    return tensor
