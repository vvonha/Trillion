# 1. Based on the Docker image of the latest of Python3, 
FROM python:3.8

COPY . ./mywork
WORKDIR ./mywork

# 2. tesseract and dependent libraries to install in Apt, 
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
     flask

ENTRYPOINT ["/usr/bin/tail", "-f", "/dev/null"]
# CMD ["python3", "app.py"]
