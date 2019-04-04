# Set the base image to Ubuntu
FROM continuumio/miniconda3 as builder

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@gmail.com"

RUN conda install -q -y -c conda-forge pandas=0.24.1 scikit-learn cvxpy=1.0.14 && \
    conda clean --all


#### Here the test-configuration
FROM builder as test

COPY . /tmp/cvx

RUN pip install --no-cache-dir /tmp/cvx && \
    rm -rf /tmp/cvx

# We install flask here to test some
RUN pip install --no-cache-dir httpretty pytest pytest-cov pytest-html sphinx

WORKDIR cvx

CMD py.test --cov=cvxFin  --cov-report html:artifacts/html-coverage --cov-report term --html=artifacts/html-report/report.html test
