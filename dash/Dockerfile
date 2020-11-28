FROM python:3.8

RUN mkdir -p /dash_app
VOLUME /dash_app
WORKDIR /dash_app
COPY requirements.txt /dash_app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /dash_app
