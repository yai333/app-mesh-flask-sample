#!/bin/bash

set -ex

docker build -t flask-api .

API_IMAGE="$( aws ecr create-repository --repository-name flask-api --region ap-southeast-2 --profile yiai --query '[repository.repositoryUri]' --output text)"

docker tag flask-api ${API_IMAGE}

$(aws ecr get-login --no-include-email --region ap-southeast-2 --profile yiai)

docker push ${API_IMAGE}
