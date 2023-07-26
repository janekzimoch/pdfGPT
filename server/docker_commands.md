# here are some docker commands that are useful for running containers

### build an image

docker build -t pdfgpt_server .

### run a container

docker run -d --name pdfgpt_server -p 5328:5328 pdfgpt_server

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
