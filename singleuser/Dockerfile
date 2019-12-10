FROM frolvlad/alpine-miniconda3

# PYTHON DATA SCIENCE PACKAGES
ARG REQ_FILE='requirements.txt'
COPY ${REQ_FILE} /tmp/${REQ_FILE}

ARG MY_USER=vibrent

# Configure environment
ENV NB_USER ${MY_USER}
ENV NB_UID 1001
ENV NB_GID 1001
ENV HOME /home/$NB_USER
ENV CONDA_DIR /opt/conda
ENV PRE_COMMIT /etc/jupyter/pre-commit

USER root
RUN addgroup -S $NB_GID && \
    adduser -s /bin/bash -u $NB_UID -D $NB_USER && \
    mkdir $HOME/work && \
    chown -R $NB_USER:$NB_GID $HOME && \
    chown -R $NB_USER:$NB_GID $CONDA_DIR && \
    conda config --add channels conda-forge

# sys packages
RUN apk --update --no-cache add git bash

USER $NB_UID
RUN echo "install python requirements" && \
    while read requirement; \
          do conda install --yes $requirement; \
      done < /tmp/${REQ_FILE} && \
echo "clean tmp files" && \
    conda clean --all -f -y && \
    rm -rf /home/$NB_USER/.cache/yarn && \
nbdime extensions --enable

#RUN git clone https://github.com/ctran-vibrent/MSDS_462_final.git $HOME/test_git

USER $NB_UID
WORKDIR $HOME

EXPOSE 8888

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start-notebook.sh"]

# Add local files as late as possible to avoid cache busting
ADD config/pre-commit $PRE_COMMIT
COPY config/git-clone-hook $HOME/.profile
#USER root
#RUN chown $NB_USER:$NB_GID $HOME/.profile
#USER $NB_UID
COPY start.sh /usr/local/bin/
COPY start-notebook.sh /usr/local/bin/
COPY start-singleuser.sh /usr/local/bin/
#COPY jupyter_notebook_config.py /etc/jupyter/
