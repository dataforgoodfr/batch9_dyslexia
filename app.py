import requests
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dyslexia.preprocessing import get_results

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
    return get_results(file.file)


@app.post("/ocr_url/")
async def ocr_url(url: str):
    req = requests.get(url)

    file = io.BytesIO(req.content)

    res = get_results(file.file)

    file.close()

    return res
