from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from controllers.load_audio_from_url import load_audio_from_url
from controllers.waveform_to_mel import waveform_to_mel
from controllers.pad_or_truncate import pad_or_truncate
from controllers.mel_to_tensor import mel_to_tensor

app = FastAPI()

@app.get("/health")
def test():
  return {"message": "FastAPI is runing successfully."}

class InferenceRequest(BaseModel):
  audio_url: str
  language: str

class InferenceResponse(BaseModel):
  label: str
  confidence: float

import torch.nn as nn
import torch.nn.functional as F

class AudioCNN(nn.Module):
  def __init__(self):
      super().__init__()

      self.conv = nn.Sequential(
          nn.Conv2d(1, 16, kernel_size=3, padding=1),
          nn.ReLU(),
          nn.MaxPool2d(2),   # (16, 64, 150)

          nn.Conv2d(16, 32, kernel_size=3, padding=1),
          nn.ReLU(),
          nn.MaxPool2d(2)    # (32, 32, 75)
      )

      self.fc = nn.Sequential(
          nn.Linear(32 * 32 * 75, 128),
          nn.ReLU(),
          nn.Linear(128, 2)  # 2 classes: Human, AI
      )

  def forward(self, x):
      x = self.conv(x)
      x = x.view(x.size(0), -1)  # flatten
      x = self.fc(x)
      return x

model = AudioCNN()
model.eval()  # inference mode


import torch

@app.post("/infer", response_model=InferenceResponse)
def infer(request: InferenceRequest):
  try:
      audio, sr = load_audio_from_url(request.audio_url)
      mel = waveform_to_mel(audio, sr)
      mel = pad_or_truncate(mel, max_len=300)
      mel_tensor = mel_to_tensor(mel)
  except ValueError as e:
      raise HTTPException(status_code=400, detail=str(e))

  with torch.no_grad():
      logits = model(mel_tensor)
      probs = torch.softmax(logits, dim=1)

  ai_prob = probs[0][1].item()  # index 1 = AI
  label = "AI" if ai_prob >= 0.5 else "Human"

  return {
      "label": label,
      "confidence": round(ai_prob, 3)
  }

