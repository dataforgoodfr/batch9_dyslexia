import requests
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dyslexia.app import get_results
from pdf2image import convert_from_bytes
import numpy as np

app = FastAPI(title="OCR API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ocr_file/")
async def ocr_file(file: UploadFile = File(...)):
    data = await file.read()

    if file.filename.endswith('.pdf'):
        data = convert_from_bytes(data)[0]
        data = np.array(data)

    return get_results(data)


@app.post("/ocr_url/")
async def ocr_url(url: str):
    return get_results(url)
