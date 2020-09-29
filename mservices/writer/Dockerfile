FROM python:3.7-slim  AS build-env

COPY writer.py requirements.txt /app/
WORKDIR /app

RUN pip install -t packages --upgrade pip && \
    pip install -t packages --upgrade -r requirements.txt

FROM gcr.io/distroless/python3-debian10
COPY --from=build-env /app /app

WORKDIR /app
ENV PYTHONPATH=/app/packages
CMD [ "packages/bin/gunicorn", "-w 3", "-b :80", "--access-logfile=-", "writer:app" ]
