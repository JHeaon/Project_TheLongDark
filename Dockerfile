FROM python:3.12

COPY . /project/

WORKDIR /project/

RUN pip install -r requirements.txt

EXPOSE 8000
