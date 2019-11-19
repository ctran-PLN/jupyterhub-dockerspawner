FROM alpine:latest

# PYTHON DATA SCIENCE PACKAGES
ARG REQ_FILE='requirements.txt'
COPY ${REQ_FILE} /tmp/${REQ_FILE}

RUN apk update \
&& apk add \
    ca-certificates \
    libstdc++ \
    python3 \
    tini \
&& apk add --virtual=build_dependencies \
    cmake \
    gcc \
    g++ \
    make \
    musl-dev \
    python3-dev \
    libressl-dev \
    libffi-dev \
    build-base \
    openblas-dev freetype-dev pkgconfig gfortran \
&& ln -s /usr/include/locale.h /usr/include/xlocale.h \
&& python3 -m pip --no-cache-dir install -r /tmp/${REQ_FILE} \
&& jupyter nbextension enable --py widgetsnbextension \
&& apk del --purge -r build_dependencies \
&& rm -rf /var/cache/apk/* \
&& jupyter nbextension enable --py widgetsnbextension

ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="1000"

# Configure environment
ENV SHELL=/bin/bash \
    NB_USER=$NB_USER \
    NB_UID=$NB_UID \
    NB_GID=$NB_GID \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV HOME=/home/$NB_USER

# Setup work directory for backward-compatibility
RUN apk add --no-cache --upgrade bash \
    && addgroup -g $NB_GID -S $NB_USER \
    && adduser -u $NB_UID -S $NB_USER  \
    && mkdir $HOME/work \
    && chown -R $NB_USER:$NB_GID /home/$NB_USER

USER $NB_UID
WORKDIR $HOME

EXPOSE 8888

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start-notebook.sh"]

# Add local files as late as possible to avoid cache busting
COPY start.sh /usr/local/bin/
COPY start-notebook.sh /usr/local/bin/
COPY start-singleuser.sh /usr/local/bin/
COPY jupyter_notebook_config.py /etc/jupyter/
