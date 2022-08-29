FROM python:3.10.0

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app

COPY Car.csv /usr/src/app

RUN pip install -r requirements.txt

COPY app.py .


EXPOSE 8000

CMD ["uvicorn", "app:app", "--reload"]