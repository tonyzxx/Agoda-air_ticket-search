#!/bin/bash
TAG='1.0.2'
IMAGE_NAME="ticket-search:${TAG}"

docker build -t ${IMAGE_NAME} .
