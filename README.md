# app-mesh-flask-sample

eval \$(aws ecr get-login --region ap-southeast-2)

docker build -t ecs-fask-gateway:latest .

docker run -it -d -p 3000:3000 ecs-fask-gateway:latest /bin/bash
