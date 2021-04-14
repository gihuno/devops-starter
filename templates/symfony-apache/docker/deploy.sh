docker build -t gihuno/symfony-apache .

docker tag gihuno/symfony-apache:latest gihuno/symfony-apache:5.2

docker push gihuno/symfony-apache:5.2
