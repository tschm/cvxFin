# Set the base image to Ubuntu
FROM continuumio/miniconda3 as builder

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@gmail.com"

RUN conda install -q -y pandas=0.24.1 scikit-learn

# install the new cvxpy?
RUN conda install -c conda-forge cvxpy=1.0.14

ADD ./cvxFin /cvx/cvxFin
WORKDIR cvx


#### Here the test-configuration

FROM builder as test

# We install flask here to test some
RUN pip install --no-cache-dir httpretty pytest pytest-cov pytest-html sphinx

COPY ./test            /cvx/test
COPY ./sphinx.sh       /cvx/sphinx.sh

CMD py.test --cov=cvxFin  --cov-report html:artifacts/html-coverage --cov-report term --html=artifacts/html-report/report.html test
