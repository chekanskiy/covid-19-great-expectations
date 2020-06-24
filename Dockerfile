FROM python:3.7-slim-buster

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        git \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

RUN pip install \
        great_expectations \
        sqlalchemy

COPY great_expectations/metric_store.py /usr/local/lib/python3.7/site-packages/great_expectations/data_context/store/metric_store.py
COPY . /
WORKDIR /