FROM nbgallery/jupyter-alpine

# PYTHON DATA SCIENCE PACKAGES
ARG REQ_FILE='requirements.txt'
COPY ${REQ_FILE} /tmp/${REQ_FILE}

RUN min-apk openblas-dev && \
echo "**** install requirements ****" && \
    min-pip3 -r /tmp/${REQ_FILE}

ARG MY_USER=vibrent
ARG NB_UID="1000"
ARG NB_GID="1000"

# Configure environment
ENV SHELL=/bin/bash \
    NB_USER=$MY_USER \
    NB_UID=$NB_UID \
    NB_GID=$NB_GID \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    KERNEL=/usr/share/jupyter/kernels

ENV HOME=/home/$NB_USER
# Setup work directory for backward-compatibility
RUN addgroup -S $NB_GID  \
    && adduser -u $NB_UID -S $NB_USER -G $NB_GID \
    && mkdir $HOME/work \
    && chown -R $NB_USER:$NB_GID $HOME \
    # remove extra kernels
    && cd $KERNEL && rm -rf c cpp go javascript octave pig python2 ruby spark_*

USER $NB_UID
WORKDIR $HOME

EXPOSE 8888

# Configure container startup
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["start-notebook.sh"]

# Add local files as late as possible to avoid cache busting
COPY start.sh /usr/local/bin/
COPY start-notebook.sh /usr/local/bin/
COPY start-singleuser.sh /usr/local/bin/
COPY jupyter_notebook_config.py /etc/jupyter/
