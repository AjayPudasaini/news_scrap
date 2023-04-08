FROM python:3.8-slim-buster

WORKDIR /goal

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# CMD ["scrapy", "crawl", "theguardian"]
