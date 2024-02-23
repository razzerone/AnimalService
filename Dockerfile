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
  POETRY_VERSION=1.7.1

RUN python -m pip install --no-cache-dir poetry==$POETRY_VERSION \
    && poetry config virtualenvs.create false

WORKDIR /app/

COPY ["./poetry.lock", "./pyproject.toml", "./"]

RUN poetry install --no-interaction --no-ansi

COPY . /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]