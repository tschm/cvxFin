# Set the base image to Ubuntu
FROM lobnek/jupyter:v2.3

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

# install cvxpy
USER root
RUN conda install -c conda-forge scikit-learn
USER $NB_USER

COPY ./work ${HOME}/work

