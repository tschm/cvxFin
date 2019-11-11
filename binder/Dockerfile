# Set the base image to Ubuntu
FROM tschm/docker:release-0.4

RUN pip install --no-cache-dir scikit-learn

COPY --chown=jovyan:100 . /tmp/cvx

RUN pip install --no-cache-dir /tmp/cvx && \
    rm -r /tmp/cvx

COPY --chown=jovyan:100 ./work ${WORK}

