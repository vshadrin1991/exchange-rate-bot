FROM python:3.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY exchange ./exchange
COPY poetry.lock pyproject.toml README.md ./

RUN pip3 install poetry
RUN poetry install

COPY .env ./.env
COPY localizations ./localizations

CMD ["poetry", "run", "python3", "-m", "exchange"]
