FROM ubuntu:18.04

RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository -y ppa:alex-p/tesseract-ocr
RUN apt-get update && apt-get install -y tesseract-ocr-all

RUN wget -P /usr/share/tesseract-ocr/4.00/tessdata/ https://github.com/tesseract-ocr/tessdata/raw/master/fra.traineddata
RUN wget -P /usr/share/tesseract-ocr/4.00/tessdata/ https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata

COPY dyslexia /deploy/
COPY tests /deploy/
COPY requirements.txt /deploy/
COPY setup.py /deploy/
COPY app.py /deploy/

WORKDIR /deploy/

RUN pip install . --no-cache-dir

EXPOSE 8080

ENTRYPOINT uvicorn app:app --host 0.0.0.0 --port 8080 --workers 1