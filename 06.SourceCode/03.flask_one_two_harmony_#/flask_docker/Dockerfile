FROM python:3.9-alpine

WORKDIR usr/src/flask_app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get -y install \
     tesseract-ocr \
     #tesseract-ocr-jpn \
     libgl1-mesa-glx
RUN apt-get clean


# 3. install the required python library in Pip 
RUN pip install --upgrade pip; \
     pip install \
     opencv-contrib-python \
     pillow \
     pytesseract \
     flask \
     gunicorn
#     python3-flask

COPY ./flask_app .
