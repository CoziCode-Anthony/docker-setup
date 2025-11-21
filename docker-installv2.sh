#!/bin/bash

#removing old docker items
sudo rm -f /etc/apt/sources.list.d/docker.list
sudo rm -f /etc/apt/keyrings/docker.gpg
sudo rm -f /etc/apt/trusted.gpg.d/docker.gpg

#adding new docker items
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/docker.gpg > /dev/null

echo "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/ubuntu noble stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

#updating
sudo apt update

#installing docker
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

#adding current user to docker group
user=$SUDO_USER
sudo usermod -aG docker "$user"

#logout
sleep 5
echo "We are going to log out now" 
sleep 10 
logout
