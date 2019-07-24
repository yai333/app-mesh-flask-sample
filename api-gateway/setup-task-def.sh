#!/bin/bash

set -ex

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

AWS_DEFAULT_REGION="ap-southeast-2"
AWS_PROFILE="yiai"

cluster_stack_output=$(aws --profile "${AWS_PROFILE}" --region "${AWS_DEFAULT_REGION}" \
    cloudformation describe-stacks --stack-name "flask-sample" \
    | jq '.Stacks[].Outputs[]')

task_role_arn=($(echo $cluster_stack_output \
    | jq -r 'select(.OutputKey == "TaskIamRoleArn") | .OutputValue'))

echo ${task_role_arn}

execution_role_arn=($(echo $cluster_stack_output \
    | jq -r 'select(.OutputKey == "TaskExecutionIamRoleArn") | .OutputValue'))

ecs_service_log_group=($(echo $cluster_stack_output \
    | jq -r 'select(.OutputKey == "ECSServiceLogGroup") | .OutputValue'))

envoy_log_level="debug"

GATEWAY_IMAGE="$( aws ecr describe-repositories --repository-name flask-gateway --region ${AWS_DEFAULT_REGION} --profile ${AWS_PROFILE} --query '[repositories[0].repositoryUri]' --output text)"

#Gateway Task Definition
task_def_json=$(jq -n \
    --arg APP_IMAGE $GATEWAY_IMAGE \
    --arg SERVICE_LOG_GROUP $ecs_service_log_group \
    --arg TASK_ROLE_ARN $task_role_arn \
    --arg EXECUTION_ROLE_ARN $execution_role_arn \
    --arg ENVOY_LOG_LEVEL $envoy_log_level \
    -f "${DIR}/task-definition-gateway.json")

aws --profile "${AWS_PROFILE}" --region "${AWS_DEFAULT_REGION}" \
    ecs register-task-definition \
    --cli-input-json "$task_def_json"
