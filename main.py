from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
  return {"Hello World"}

""" git branch -M main """