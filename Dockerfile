FROM python

ENV PYTHONUNBUFFERED 1
ENV PYTHONOPTIMIZE 1

WORKDIR /code

RUN apt update && apt install -y curl stockfish

RUN pip install poetry

ENV PATH /root/.local/bin:$PATH

COPY ./poetry.lock /code/poetry.lock
COPY ./pyproject.toml /code/pyproject.toml

RUN poetry install --without dev

COPY ./app /code/app
COPY main.py /code/main.py

ENV PORT ${PORT}
ENV ALLOWED_ORIGIN ${ALLOWED_ORIGIN}

ARG EXPOSE_PORT=${PORT}
EXPOSE ${EXPOSE_PORT}

CMD ["poetry", "run", "python", "main.py"]
