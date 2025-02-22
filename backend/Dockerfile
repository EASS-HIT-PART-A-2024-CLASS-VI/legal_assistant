FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install "poetry>=1.7.0"

COPY src/ src/

ENV PYTHONPATH=/app/src
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-interaction --no-ansi --verbose --no-root

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--loop", "asyncio"]
