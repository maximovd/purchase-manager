FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    apt-get install gcc -y

COPY poetry.lock pyproject.toml ./
RUN pip install poetry==1.1 && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev

COPY . ./

CMD poetry run aerich upgrade && \
    poetry run uvicorn --host=0.0.0.0 app.main:app
