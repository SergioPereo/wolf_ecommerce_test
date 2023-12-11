# 
FROM python:3.9

# 
WORKDIR /code

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
CMD sleep 10 && uvicorn app.main:app --host 0.0.0.0 --port 80
