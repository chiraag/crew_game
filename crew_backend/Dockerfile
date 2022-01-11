FROM python:3.8

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/

ARG APP_ENV=${APP_ENV:-prod}
ENV APP_ENV=${APP_ENV}

RUN bash -c "if [ $APP_ENV == 'dev' ] ; then poetry install -E gmail --no-root ; else poetry install -E gmail -E prod --no-root --no-dev ; fi"

COPY ./scripts/start.sh /start.sh
RUN chmod +x /start.sh

COPY ./crew_backend /app/crew_backend

