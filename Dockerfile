FROM python:3.10

WORKDIR /app/web

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .