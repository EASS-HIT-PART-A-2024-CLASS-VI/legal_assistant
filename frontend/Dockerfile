FROM python:3.12-slim


WORKDIR /app
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install "poetry>=1.7.0"

COPY src/ src/
COPY src/images/ images/
COPY src/.streamlit .streamlit/

RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-interaction --no-ansi --verbose --no-root

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
