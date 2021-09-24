FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /purchase-manager

RUN apt-get update && \
    apt-get install gcc -y

COPY poetry.lock pyproject.toml ./
RUN pip install poetry && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev


COPY . /purchase-manager

CMD poetry run aerich upgrade && \
    poetry run uvicorn --host=0.0.0.0 app.main:app
