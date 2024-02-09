#!/usr/bin/env bash

sudo apt install -y python3-pip
sudo apt install -y nginx
sudo apt install -y virtualenv

# Install chromedriver
sudo wget -N https://chromedriver.storage.googleapis.com/117.0.5938.132/chromedriver_linux64.zip -P ~/
sudo unzip ~/chromedriver_linux64.zip -d ~/
sudo rm ~/chromedriver_linux64.zip
sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
sudo chown ubuntu:ubuntu /usr/local/bin/chromedriver
sudo chmod 0755 /usr/local/bin/chromedriver

# Install Google Chrome
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install -y google-chrome-stable
