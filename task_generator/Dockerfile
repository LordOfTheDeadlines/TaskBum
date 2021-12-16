FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /task_generator
WORKDIR /task_generator
COPY . /task_generator
COPY requirements.txt /task_generator
RUN pip install -r requirements.txt