#!/bin/bash

# For MacOS users - if you get a "failed to solve with frontend dockerfile.v0" error:
# set the following env variables (source: https://github.com/docker/buildx/issues/426)
# 
# export DOCKER_BUILDKIT=0
# export COMPOSE_DOCKER_CLI_BUILD=0

# Build
docker image build -f Dockerfile_producer -t producer .

# Run
docker run \
    -e FLASK_APP=producer \
    -p 5000:5000 \
    producer