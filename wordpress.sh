#!/bin/bash

#function to install docker
docker_installer(){
		read -s -p "Please enter password for Sudo permissions: " PASSWORD
		#We need sudo super user rights to run installations properly 
		echo
		
		#Setting up docker repository
		if $1 == 1; then
			echo "$PASSWORD" | sudo -S apt update
			echo "$PASSWORD" | sudo -S apt install apt-transport-https ca-certificates curl software-properties-common
			echo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | "$PASSWORD" | sudo -S gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
			echo "$PASSWORD" | sudo -S chmod a+r /etc/apt/keyrings/docker.gpg
			echo \
		"deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
		"$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | "$PASSWORD" | \
		sudo -S tee /etc/apt/sources.list.d/docker.list > /dev/null

			#Download and install Docker Engine
			echo "$PASSWORD" | sudo -S apt update
			echo "$PASSWORD" | sudo -S apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
		elif $1 == 2; then
			echo "$PASSWORD" | sudo -S apt update
			echo "$PASSWORD" | sudo -S apt-get install docker-compose-plugin
		else
			echo "Error, exiting"
			exit
}

# Check or docker and Docker-compose
if command -v docker > dev/null; then
	echo "docker is present"
	if command -v docker compose version > dev/null; then
		echo "docker compose is also present"
	else 
		docker_installer 2
	fi 
else
	docker_installer 1
fi
