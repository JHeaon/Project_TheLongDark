FROM python:3.12

COPY . /project/

WORKDIR /project/

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

EXPOSE 8000
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]