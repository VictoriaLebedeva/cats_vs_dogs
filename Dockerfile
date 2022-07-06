<<<<<<< HEAD
FROM python:3.8-slim-buster

RUN pip install poetry

WORKDIR "/animal_classificator"

COPY ["pyproject.toml", "./"]

RUN poetry install --no-interaction --no-ansi
COPY . .

EXPOSE 9696

=======
FROM python:3.8-slim-buster

RUN pip install poetry

WORKDIR "/animal_classificator"

COPY ["pyproject.toml", "./"]

RUN poetry install --no-interaction --no-ansi
COPY . .

EXPOSE 9696

>>>>>>> c7c4a211ca9139b1f540f869dcae4643943ed7a9
ENTRYPOINT  ["poetry", "run", "app" ]