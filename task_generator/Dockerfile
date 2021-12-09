FROM python:3.8

ENV PYTHONUNBUFFERED 1
#
#RUN pactl load-module module-pipe-source source_name=virtmic file=/task_generator/virtmic format=s16le rate=16000 channels=1
#RUN pactl set-default-source virtmic

RUN mkdir /task_generator
WORKDIR /task_generator
COPY . /task_generator
COPY requirements.txt /task_generator
RUN pip install -r requirements.txt