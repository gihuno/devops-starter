docker build -t gihuno/php .

docker tag gihuno/php:latest gihuno/php:8.0

docker push gihuno/php:8.0
