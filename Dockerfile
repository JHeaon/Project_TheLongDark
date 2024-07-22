FROM python:3.12

COPY . /project/

WORKDIR /project/

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000