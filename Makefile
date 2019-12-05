# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

include .env

.DEFAULT_GOAL=build

network:
	@docker network inspect $(DOCKER_NETWORK_NAME) >/dev/null 2>&1 || docker network create $(DOCKER_NETWORK_NAME)

volumes:
	@docker volume inspect $(DATA_VOLUME_HOST) >/dev/null 2>&1 || docker volume create --name $(DATA_VOLUME_HOST)
	@docker volume inspect $(DB_VOLUME_HOST) >/dev/null 2>&1 || docker volume create --name $(DB_VOLUME_HOST)

shared-volume:
	@[ -d $(SHARED_DIR) ] || (sudo mkdir -p $(SHARED_DIR) && sudo chmod 777 $(SHARED_DIR))
	@docker volume inspect $(SHARED_VOLUME_NAME) >/dev/null 2>&1 || docker volume create --opt type=none \
																																      --opt device=$(SHARED_DIR) \
																																      --opt o=bind \
																																			--name $(SHARED_VOLUME_NAME)

secrets/postgres.env:
	@echo "Generating postgres password in $@"
	@echo "POSTGRES_PASSWORD=$(shell openssl rand -hex 32)" > $@

secrets/jupyterhub.crt:
	@echo "Need an SSL certificate in secrets/jupyterhub.crt"
	@exit 1

secrets/jupyterhub.key:
	@echo "Need an SSL key in secrets/jupyterhub.key"
	@exit 1

userlist:
	@echo "Add usernames, one per line, to ./userlist, such as:"
	@echo "    zoe admin"
	@echo "    wash"
	@exit 1

# Do not require cert/key files if SECRETS_VOLUME defined
secrets_volume = $(shell echo $(SECRETS_VOLUME))
ifeq ($(secrets_volume),)
	cert_files=secrets/jupyterhub.crt secrets/jupyterhub.key
else
	cert_files=
endif

check-files: userlist $(cert_files) secrets/postgres.env

gen-cert:
	@mkdir -p secrets
	@openssl req -x509 -nodes -newkey rsa:2048 -keyout jupyterhub.key -out jupyterhub.crt \
	-subj "/C=us/ST=va/L=fairfax/O=vibrent/OU= /CN= "
	@mv jupyterhub.crt jupyterhub.key secrets/

notebook_image: pull singleuser/Dockerfile
	docker build  -t $(LOCAL_NOTEBOOK_IMAGE) --build-arg MY_USER=$(MY_USER) \
		singleuser

build: gen-cert check-files network volumes shared-volume
	docker-compose build

.PHONY: network volumes check-files pull notebook_image build
