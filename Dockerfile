ARG PYTHON_VERSION=3.12
ARG BASE_DISTRO=slim-bookworm

FROM python:${PYTHON_VERSION}-${BASE_DISTRO}
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.7.1

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app/
COPY ["./poetry.lock", "./pyproject.toml", "./"]

RUN /usr/local/poetry install --no-interaction --no-ansi

COPY . /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]