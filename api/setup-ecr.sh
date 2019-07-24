#!/bin/bash

set -ex
AWS_DEFAULT_REGION="ap-southeast-2"
AWS_PROFILE="yiai"

docker build -t flask-api .

API_IMAGE="$( aws ecr create-repository --repository-name flask-api --region ${AWS_DEFAULT_REGION} --profile ${AWS_PROFILE} --query '[repository.repositoryUri]' --output text)"

docker tag flask-api ${API_IMAGE}

$(aws ecr get-login --no-include-email --region ${AWS_DEFAULT_REGION}  --profile ${AWS_PROFILE})

docker push ${API_IMAGE}
