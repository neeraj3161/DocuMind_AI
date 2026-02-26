from fastapi import FastAPI, UploadFile, UploadFile
import uuid
import shutil
import os

app = FastAPI(title="DocuMind AI")

@app.get("/")
def root():
    return {"message": "DocuMind AI is running"}

