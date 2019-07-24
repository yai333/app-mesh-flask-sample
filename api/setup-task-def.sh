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

#Api v1 Task Definition
v1_task_def_json=$(jq -n \
    --arg APP_IMAGE $GATEWAY_IMAGE \
    --arg SERVICE_LOG_GROUP $ecs_service_log_group \
    --arg TASK_ROLE_ARN $task_role_arn \
    --arg EXECUTION_ROLE_ARN $execution_role_arn \
    --arg ENVOY_LOG_LEVEL $envoy_log_level \
    --arg LOG_STREAM_PREFIX "api-v1" \
    --arg API_FAMILY "api-v1" \
    --arg VERSION "1" \
    --arg VIRTUAL_NODE "mesh/flask-mesh/virtualNode/api-v1-vn" \
    -f "${DIR}/task-definition.json")

aws --profile "${AWS_PROFILE}" --region "${AWS_DEFAULT_REGION}" \
    ecs register-task-definition \
    --cli-input-json "$v1_task_def_json"


#Api v2 Task Definition
v2_task_def_json=$(jq -n \
    --arg APP_IMAGE $GATEWAY_IMAGE \
    --arg SERVICE_LOG_GROUP $ecs_service_log_group \
    --arg TASK_ROLE_ARN $task_role_arn \
    --arg EXECUTION_ROLE_ARN $execution_role_arn \
    --arg ENVOY_LOG_LEVEL $envoy_log_level \
    --arg LOG_STREAM_PREFIX "api-v2" \
    --arg API_FAMILY "api-v2" \
    --arg VERSION "2" \
    --arg VIRTUAL_NODE "mesh/flask-mesh/virtualNode/api-v2-vn" \
    -f "${DIR}/task-definition.json")

aws --profile "${AWS_PROFILE}" --region "${AWS_DEFAULT_REGION}" \
    ecs register-task-definition \
    --cli-input-json "$v2_task_def_json"
