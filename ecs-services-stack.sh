#!/bin/bash

set -ex

AWS_DEFAULT_REGION="ap-southeast-2"
AWS_PROFILE="yiai"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

task_api_arn=$(aws ecs list-task-definitions --family-prefix api \
--region ${AWS_DEFAULT_REGION} --profile ${AWS_PROFILE} \
--sort DESC \
--query '[taskDefinitionArns[0]]' --output text)

task_api_v2_arn=$(aws ecs list-task-definitions --family-prefix api-v2 \
 --region ${AWS_DEFAULT_REGION} --profile ${AWS_PROFILE} \
 --sort DESC \
 --query '[taskDefinitionArns[0]]' --output text)

task_gateway_arn=$(aws ecs list-task-definitions --family-prefix gateway \
--region ${AWS_DEFAULT_REGION} --profile ${AWS_PROFILE} \
--sort DESC \
--query '[taskDefinitionArns[0]]' --output text)

aws cloudformation --region ${AWS_DEFAULT_REGION} --profile ${AWS_PROFILE} \
    deploy --stack-name "flask-ecs-service" \
    --capabilities CAPABILITY_IAM \
    --template-file "${DIR}/ecs-services.yaml"  \
    --parameter-overrides \
    GatewayTaskDefinition="${task_gateway_arn}" \
    ApiV1TaskDefinition="${task_api_arn}" \
    ApiV2TaskDefinition="${task_api_v2_arn}"
