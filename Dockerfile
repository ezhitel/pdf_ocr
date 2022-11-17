FROM ubuntu:22.04
RUN apt update
RUN apt install -y python3.10
RUN apt install -y python3-pip
RUN pip install opencv-python
RUN apt install -y tesseract-ocr
RUN apt install -y tesseract-ocr-rus
RUN pip install pytesseract
RUN apt install -y poppler-utils
RUN apt install -y git
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
RUN apt install -y python3-opencv
RUN git clone https://github.com/ezhitel/pdf_ocr.git
ENTRYPOINT ["python3", "./pdf_ocr/server.py"]
