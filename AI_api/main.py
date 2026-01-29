from fastapi import FastAPI;

app = FastAPI()

@app.get("/")
def test():
  return {"message": "fast api runing successfully"}