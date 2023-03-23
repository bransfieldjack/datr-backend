FROM python:3.10
ENV PYTHONUNBUFFERED=1
COPY . /code/
WORKDIR /code
RUN pip install pipenv
RUN apt update
RUN apt install nodejs -y
RUN apt install npm -y
RUN pipenv install --system --deploy --ignore-pipfile