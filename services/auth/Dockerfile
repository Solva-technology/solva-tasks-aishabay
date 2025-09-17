FROM python:3.12-slim

RUN apt-get update && apt-get install -y

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1

COPY requirements ./requirements

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements/base.txt

COPY . /usr/src/app/services/auth

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
