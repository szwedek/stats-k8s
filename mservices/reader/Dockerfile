FROM python:2.7-slim  AS build-env

COPY reader.py requirements.txt /app/
WORKDIR /app

RUN pip install -t packages --upgrade pip && \
    pip install -t packages -r ./requirements.txt

FROM gcr.io/distroless/python2.7
COPY --from=build-env /app /app

WORKDIR /app
ENV PYTHONPATH=/app/packages
CMD [ "reader.py" ]
