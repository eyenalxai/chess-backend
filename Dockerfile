FROM python

ENV PYTHONUNBUFFERED 1
ENV PYTHONOPTIMIZE 1

WORKDIR /code

RUN apt update && apt install -y curl

RUN pip install poetry

ENV PATH /root/.local/bin:$PATH

COPY ./poetry.lock /code/poetry.lock
COPY ./pyproject.toml /code/pyproject.toml

RUN poetry install --without dev

COPY ./app /code/app
COPY main.py /code/main.py

RUN curl -o /code/app/util/stockfish https://sitemap-storage.ams3.cdn.digitaloceanspaces.com/stuff/stockfish
RUN chmod +x /code/app/util/stockfish
RUN chmod 777 /code/app/util/stockfish

ENV PORT ${PORT}
ENV ALLOWED_ORIGIN ${ALLOWED_ORIGIN}

ARG EXPOSE_PORT=${PORT}
EXPOSE ${EXPOSE_PORT}

CMD ["poetry", "run", "python", "main.py"]
