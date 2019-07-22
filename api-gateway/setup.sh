#!/bin/bash

set -ex

docker build -t flask-gateway .

GATEWAY_IMAGE="$( aws ecr create-repository --repository-name flask-gateway --region ap-southeast-2 --profile yiai --query '[repository.repositoryUri]' --output text)"

docker tag flask-gateway ${GATEWAY_IMAGE}

$(aws ecr get-login --no-include-email --region ap-southeast-2 --profile yiai)

docker push ${GATEWAY_IMAGE}
