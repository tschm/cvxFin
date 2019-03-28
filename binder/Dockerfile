# Set the base image to Ubuntu
FROM lobnek/jupyter:v2.8

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

# install scikit
#USER root

RUN pip install --no-cache-dir scikit-learn

#RUN conda install -c conda-forge scikit-learn && \
#    conda clean --all

#USER $NB_USER

COPY --chown=beakerx:beakerx ./work ${WORK}

