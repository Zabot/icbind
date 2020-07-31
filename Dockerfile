FROM python:latest

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /tmp/icbind
RUN pip install /tmp/icbind
