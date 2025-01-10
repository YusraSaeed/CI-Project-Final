FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 8001


CMD ["gunicorn","-c","config.py","src.main:app"]
