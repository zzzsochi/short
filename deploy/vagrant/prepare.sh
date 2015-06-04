#!/bin/bash

set -e

echo "Setup hostname"
hostname vagrant-short

echo "Some terminal fix"
export LC_ALL="C"
export DEBIAN_FRONTEND='noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" dist-upgrade'

echo "Update and install apt packages"
apt-get update
# apt-get -y upgrade
apt-get -y install \
    language-pack-ru-base \
    curl git htop iftop mercurial pydf vim zip zsh \
    python3 python3-dev \
    redis-server

echo "Update locale"
# export LC_ALL=`locale --all | grep -i ru_RU.utf`
update-locale "LC_ALL=`locale --all | grep -i ru_RU.utf`"
