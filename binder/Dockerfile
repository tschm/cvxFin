# Set the base image to Ubuntu
FROM lobnek/jupyter:v2.5

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

# install scikit
USER root

RUN conda install -c conda-forge scikit-learn && \
    conda clean --all

USER $NB_USER

COPY ./work ${WORK}

