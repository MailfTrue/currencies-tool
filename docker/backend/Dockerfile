FROM python:3.10

RUN apt-get update && apt-get install -y wget wkhtmltopdf

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR app
COPY . .

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0
