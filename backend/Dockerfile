FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

RUN mkdir files logs

CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8000", "app:app"]
