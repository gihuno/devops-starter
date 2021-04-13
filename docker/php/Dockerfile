FROM gihuno/ubuntu:21.04

# Install Apache
RUN  apt-get -y update && apt-get install -y -q \
apache2

RUN a2enmod rewrite

# Install PHP 7.4
RUN LC_ALL=C.UTF-8 add-apt-repository ppa:ondrej/php

RUN  apt-get -y update && apt-get install -y -q \
php7.4 \
php7.4-xml \
php7.4-intl \
php7.4-mysql \
php7.4-curl \
php7.4-gd \
php7.4-mbstring \
php7.4-zip \
php7.4-simplexml \
libapache2-mod-php

RUN update-alternatives --set php /usr/bin/php7.4

RUN a2enmod php7.4

RUN service apache2 restart
