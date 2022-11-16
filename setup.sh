#!/bin/bash
import subprocess

RED='\e[1;31m'
okegreen='\033[92m'

echo -e "${okegreen}Beginning setup..."

unamestr="$(uname)"
if [[ "$unamestr" == "Linux" ]]; then
  echo "Platform is Linux."
  platform="linux"
else
  echo "Unrecognized platform. Script currently only supports Linux"
  exit 1
fi
echo "Checking Dependencies..."

sudo apt-get install python3 -y >/dev/null
sudo apt-get install python3-pip -y >/dev/null

pip3 install --upgrade awscli >/dev/null
pip3 install boto3 >/dev/null
echo "Configuring AWS CLI - Please have Access / Secret Keys ready!"
echo -e "💀 ${RED} WARNING: It is NOT best practice to use access keys for your root account. \n please ensure you set up a separate account that has Administrator access instead!"

echo -e $okegreen
aws configure

echo -e "Setup Completed Successfully!"