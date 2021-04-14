FROM gihuno/php:8.0

# Install Python
RUN  apt-get -y update && apt-get install -y -q \
python3 \
python3-pip

#Install AWS-CLI
RUN pip3 install --upgrade pip
ENV PYTHONIOENCODING=UTF-8
RUN pip3 install awscli

# Install AWS boto3 for python usage.
RUN pip3 install boto3

# This environment variables allow python's print function to output to docker logs automatically.
ENV PYTHONUNBUFFERED=1

RUN echo "ServerName localhost" | tee /etc/apache2/conf-available/servername.conf

RUN a2enconf servername

RUN echo "ErrorLog /dev/stderr" | tee /etc/apache2/conf-available/logging.conf
RUN echo "TransferLog /dev/stdout" | tee /etc/apache2/conf-available/logging.conf

RUN a2enconf logging

RUN echo "<IfModule mpm_prefork_module>" >> "/etc/apache2/apache2.conf"
RUN echo "StartServers             5" >> "/etc/apache2/apache2.conf"
RUN echo "ServerLimit             1024" >> "/etc/apache2/apache2.conf"
RUN echo "MaxClients             1024" >> "/etc/apache2/apache2.conf"
RUN echo "MinSpareServers          5" >> "/etc/apache2/apache2.conf"
RUN echo "MaxSpareServers         10" >> "/etc/apache2/apache2.conf"
RUN echo "MaxRequestWorkers      1024" >> "/etc/apache2/apache2.conf"
RUN echo "MaxConnectionsPerChild   0" >> "/etc/apache2/apache2.conf"
RUN echo "</IfModule>" >> "/etc/apache2/apache2.conf"

COPY retrieve-zip-from-s3.py /var/retrieve-zip-from-s3.py
RUN chmod a+x /var/retrieve-zip-from-s3.py

COPY entrypoint.py /var/entrypoint.py
RUN chmod a+x /var/entrypoint.py

ENTRYPOINT python3 /var/entrypoint.py
