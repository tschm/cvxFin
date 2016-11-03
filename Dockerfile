# Set the base image to Ubuntu
FROM continuumio/miniconda3

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@gmail.com"

RUN conda install -q -y pandas=0.18.1

# install the new cvxpy?
RUN conda install -q -y -c cvxgrp cvxpy

ADD . /cvxFin
WORKDIR cvxFin


