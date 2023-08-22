FROM python:3.9

WORKDIR /code

COPY ./ /code/

RUN --mount=type=cache,target=/root/.cache/pip pip install .

CMD ["python", "-m", "uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]