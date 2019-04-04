#!make
PROJECT_VERSION := $(shell python setup.py --version)

SHELL := /bin/bash
PACKAGE := cvxFin
IMAGE := tschm/cvxfin

# needed to get the ${PORT} environment variable
include .env
export

.PHONY: help build test teamcity jupyter graph doc tag hub

.DEFAULT: help

help:
	@echo "make build"
	@echo "       Build the docker image."
	@echo "make test"
	@echo "       Build the docker image for testing and run them."
	@echo "make teamcity"
	@echo "       Run tests, build a dependency graph and construct the documentation."
	@echo "make jupyter"
	@echo "       Start the Jupyter server."
	@echo "make graph"
	@echo "       Build a dependency graph."
	@echo "make doc"
	@echo "       Construct the documentation."
	@echo "make tag"
	@echo "       Make a tag on Github."
	@echo "make hub"
	@echo "       Push Docker Image to DockerHub."


build:
	docker-compose build jupyter
	docker-compose build cvxfin

test:
	mkdir -p artifacts
	docker-compose -f docker-compose.test.yml build sut
	docker-compose -f docker-compose.test.yml run sut

teamcity: test graph doc

jupyter: build
	echo "http://localhost:${PORT}"
	docker-compose up jupyter

graph: test
	mkdir -p ${PWD}/artifacts/graph

	docker run --rm --mount type=bind,source=${PWD}/${PACKAGE},target=/pyan/${PACKAGE},readonly \
		   tschm/pyan:latest python pyan.py ${PACKAGE}/**/*.py -V --uses --defines --colored --dot --nested-groups > graph.dot

	# remove all the private nodes...
	grep -vE "____" graph.dot > graph2.dot

	docker run --rm -v ${PWD}/graph2.dot:/pyan/graph.dot:ro \
		   tschm/pyan:latest dot -Tsvg /pyan/graph.dot > artifacts/graph/graph.svg

	rm graph.dot graph2.dot

doc: test
	docker-compose -f docker-compose.test.yml run sut sphinx-build /source artifacts/build

tag: test
	git tag -a ${PROJECT_VERSION} -m "new tag"
	git push --tags

hub: tag
	docker build --tag ${IMAGE}:latest --no-cache --target builder .
	docker push ${IMAGE}:latest
	docker tag ${IMAGE}:latest ${IMAGE}:${PROJECT_VERSION}
	docker push ${IMAGE}:${PROJECT_VERSION}
	docker rmi -f ${IMAGE}:${PROJECT_VERSION}
