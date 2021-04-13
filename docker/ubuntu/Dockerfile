FROM ubuntu:21.04

# Set the timezone right at the beginning so that the ntp installation can proceed
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get -y update && apt-get -y install software-properties-common \
apt-transport-https \
ca-certificates \
ntp

ENV PATH "$PATH:~/.local/bin:/usr/local/bin"
