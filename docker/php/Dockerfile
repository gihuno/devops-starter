FROM gihuno/ubuntu:20.04

# Install Apache
RUN  apt-get -y update && apt-get install -y -q \
apache2

RUN a2enmod rewrite

# Install PHP 8.0
RUN LC_ALL=C.UTF-8 add-apt-repository ppa:ondrej/php

RUN  apt-get -y update && apt-get install -y -q \
php8.0 \
php8.0-xml \
php8.0-intl \
php8.0-mysql \
php8.0-curl \
php8.0-gd \
php8.0-mbstring \
php8.0-zip \
php8.0-simplexml \
libapache2-mod-php

RUN update-alternatives --set php /usr/bin/php8.0

RUN a2enmod php8.0

RUN service apache2 restart
