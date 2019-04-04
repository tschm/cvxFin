# Set the base image to Ubuntu
FROM lobnek/jupyter:v2.8

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"


RUN pip install --no-cache-dir scikit-learn

COPY --chown=beakerx:beakerx . /tmp/cvx

RUN pip install --no-cache-dir /tmp/cvx && \
    rm -r /tmp/cvx

COPY --chown=beakerx:beakerx ./work ${WORK}

