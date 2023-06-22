FROM python:3.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .

RUN pip3 install poetry
RUN poetry install

CMD ["poetry", "run", "python3", "-m", "exchange"]
