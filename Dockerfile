FROM python:3.7.7-slim-stretch as builder

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@gmail.com"

COPY . /tmp/cvx

RUN buildDeps='gcc g++' && \
    apt-get update && apt-get install -y $buildDeps --no-install-recommends && \
    pip install --no-cache-dir -r /tmp/cvx/requirements.txt && \
    #pip install --no-cache-dir /tmp/cvx && \
    rm -r /tmp/cvx && \
    apt-get purge -y --auto-remove $buildDeps


COPY ./cvxFin /cvx/cvxFin

FROM builder as test

# We install flask here to test some
RUN pip install --no-cache-dir httpretty pytest pytest-cov pytest-html sphinx

WORKDIR cvx

COPY test /cvx/test

CMD py.test --cov=cvxFin  --cov-report html:artifacts/html-coverage --cov-report term --html=artifacts/html-report/report.html test
