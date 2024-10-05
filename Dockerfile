FROM python:3.11.3
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt