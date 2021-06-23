FROM ubuntu:18.04
RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository -y ppa:alex-p/tesseract-ocr-devel
RUN apt-get update && apt-get install -y tesseract-ocr && apt-get install -y libtesseract-dev

RUN apt-get install -y libgl1-mesa-glx

RUN apt-get install -y wget

RUN wget -P /usr/share/tesseract-ocr/4.00/tessdata/ https://github.com/tesseract-ocr/tessdata/raw/master/fra.traineddata
RUN wget -P /usr/share/tesseract-ocr/4.00/tessdata/ https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata

RUN apt-get install -y python3-pip

COPY dyslexia /deploy/dyslexia
COPY tests /deploy/tests
COPY requirements.txt /deploy/
COPY setup.py /deploy/
COPY app.py /deploy/

WORKDIR /deploy/

RUN python3 -m pip install --upgrade pip --no-cache-dir
RUN python3 -m pip install . --no-cache-dir

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

RUN tesseract --version

CMD python3 -m uvicorn app:app --host 0.0.0.0 --port $PORT --workers 1
