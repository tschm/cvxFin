# Set the base image to Ubuntu
FROM continuumio/miniconda3 as builder

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@gmail.com"

RUN conda install -q -y -c conda-forge pandas scikit-learn cvxpy && \
    conda clean --all

COPY . /tmp/cvx

RUN pip install --no-cache-dir /tmp/cvx && \
    rm -rf /tmp/cvx

FROM builder as test

# We install flask here to test some
RUN pip install --no-cache-dir httpretty pytest pytest-cov pytest-html sphinx

WORKDIR cvx

COPY test /cvx/test
CMD py.test --cov=cvxFin  --cov-report html:artifacts/html-coverage --cov-report term --html=artifacts/html-report/report.html /cvx/test
