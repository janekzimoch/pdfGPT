# here are some docker commands that are useful for running containers

### build an image

docker build -t pdfgpt_server_m1 .

### build image for linux processors to run on AWS

docker buildx build --platform=linux/amd64 -t pdfgpt_server .

### run a container

docker run -d --name pdfgpt_server_m1 -p 5328:5328 pdfgpt_server_m1

### get constant logs of the docekr

docker logs --follow pdfgpt_server_m1

### look at stats of images

docker stats

### inspect available images

docker images

### inspect running containers

docker ps

### inspect containers which were also stoped

docker ps -a

### retrive logs of a container

docker logs pdfgpt_server

### remove a docker container

docker rm CONTAINER_ID_OR_NAME

### remove a docker image

docker rmi pdfgpt_server

# Here is how to deploy your dockerized backend to AWS

### here is how to push docker image to ECR

1. authenticate your user
   1.1. aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 889024833665.dkr.ecr.eu-north-1.amazonaws.com
2. create private repository for the project's images in ECR
3. tag your docker image you want to push
   3.1. docker tag c67601cf2d4c 889024833665.dkr.ecr.eu-north-1.amazonaws.com/pdfgpt:latest
4. push the docker into ECR
   4.1. docker push 889024833665.dkr.ecr.eu-north-1.amazonaws.com/pdfgpt