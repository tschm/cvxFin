# Set the base image to Ubuntu
FROM continuumio/miniconda3

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@gmail.com"

RUN conda install -q -y pandas=0.18.1 #cvxopt=1.1.8
# cvxopt doesn't work well with anaconda

# install the new cvxpy?
RUN conda install -c cvxgrp cvxpy

ADD . /cvxFin
WORKDIR cvxFin


