#!/bin/bash

set -e

echo "cd src" >> /home/vagrant/.bashrc
echo "cd src" >> /home/vagrant/.zprofile


echo "Create python virtual environment"
pyvenv-3.4 --without-pip "/home/vagrant/env"
source "/home/vagrant/env/bin/activate"
echo 'source "/home/vagrant/env/bin/activate"' >> /home/vagrant/.bashrc
echo 'source "/home/vagrant/env/bin/activate"' >> /home/vagrant/.zprofile

echo "Get and install pip"
curl -s "https://bootstrap.pypa.io/get-pip.py" -o "/tmp/get-pip.py"
chmod +rx "/tmp/get-pip.py"
python "/tmp/get-pip.py"

echo "Install python packages"
cd "/home/vagrant/src"
pip install "git+http://github.com/zzzsochi/aiohttp_traversal.git"
pip install -e .
