FROM python:3.12
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./alembic /code/alembic
COPY ./alembic.ini /code/alembic.ini
COPY ./models /code/models
COPY ./app /code/app
CMD ["alembic", "upgrade", "head"]
CMD ["fastapi", "run", "app/main.py", "--port", $PORT]