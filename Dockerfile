FROM python:3.10

WORKDIR /app

COPY app/ ./app/
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "app/crawl.py"]
