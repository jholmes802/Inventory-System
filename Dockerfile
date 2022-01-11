# syntax=docker/dockerfile:1

FROM python:3.10

WORKDIR /app

RUN pip3 install "python-barcode[images]"

COPY . .

CMD ["python3", "/app/src/main_server.py"]