FROM python:3.10 AS base

WORKDIR /app/src

RUN useradd -m ugc_user

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt \
&& mkdir /app/logs

COPY ./src /app/src

COPY ./.env /app/src/.env

RUN chown -R ugc_user:ugc_user /app

USER ugc_user

ENV PATH=$PATH:/home/ugc_user/.local/bin

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "-k", "uvicorn_worker.UvicornWorker", "--forwarded-allow-ips", "*"]
