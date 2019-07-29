# Introduction

This is sample code for running App Mesh on ECS Fargate

# Getting Started

## Prerequisites

- Install latest [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/installing.html).

- Build and push the flask api and gateway images using setup-ecr.sh from within /api/ and api-gateway/
- Configure aws-cli to support Appmesh APIs
- Change the profile variable and default region variable in bash files.

## Cloudformation template for ECS, VPC and App Mesh

- Setup VPC

```
$ aws cloudformation create-stack --stack-name flask-sample --template-body file://ecs-vpc.yaml --profile YOUR_PROFILE --region YOUR_REGION
```

- Setup Mesh

```
$ aws cloudformation create-stack --stack-name flask-app-mesh --template-body file://ecs-app-mesh.yaml --profile YOUR_PROFILE --region YOUR_REGION
```

- Setup ECS Cluster
  Change AWS_DEFAULT_REGION and AWS_PROFILE variables in ecs-services-stack.sh, then run

```
$ bash ecs-services-stack.sh
```

## Apps

Once VPC and ECS cluster are setup you can deploy applications and configure mesh.

## Building api

In /api directory, Change AWS_DEFAULT_REGION and AWS_PROFILE variables in .sh files

```
$ bash setup-ecr.sh && bash setup-task-def.sh
```

## Building api

In /api-gateway directory, Change AWS_DEFAULT_REGION and AWS_PROFILE variables in .sh files

```
$ bash setup-ecr.sh && bash setup-task-def.sh
```
