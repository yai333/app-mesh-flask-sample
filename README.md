# app-mesh-flask-sample

eval \$(aws ecr get-login --region ap-southeast-2 --profile yiai)

docker build -t flask-gateway .
docker run -p 3000:3000 -e API_ENDPOINT=http://localhost --rm flask-gateway

docker tag flask-gateway \$( aws ecr create-repository --repository-name flask-gateway --region ap-southeast-2 --profile yiai --query '[repository.repositoryUri]' --output text)

docker build -t flask-api .
docker run -p 3000:3000 -e API_VERSION=1 --rm flask-api

docker tag flask-api \$( aws ecr create-repository --repository-name flask-api --region ap-southeast-2 --profile yiai --query '[repository.repositoryUri]' --output text)

aws cloudformation describe-stacks --stack-name flask-sample --profile yiai --region ap-southeast-2

aws ecs register-task-definition --cli-input-json file://task_definition_v1.json --profile yiai --region ap-southeast-2
