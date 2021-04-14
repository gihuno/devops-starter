docker build -t gihuno/ubuntu .

docker tag gihuno/ubuntu:latest gihuno/ubuntu:20.04

docker push gihuno/ubuntu:20.04
