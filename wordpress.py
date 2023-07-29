import subprocess
import docker
import os
import sys

def pip_install_requirements():
    with open("requirements.txt", 'w') as x:
       x.write('''
               docker
               ''')
    try:
        subprocess.run(['pip', 'install', '-r', requirements_file], check=True)
        print("Successfully installed the dependencies.")
    except subprocess.CalledProcessError as e:
        print("Error installing the dependencies:")
        print(e)
def check_docker_installed():
    try:
        subprocess.run(["docker", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def check_docker_compose_installed():
    try:
        subprocess.run(["docker","compose", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_docker():
    print("Docker not found. Installing Docker...")
    os.system("sudo apt-get update")
    os.system("sudo apt-get install -y docker.io")
    os.system("sudo systemctl start docker")
    os.system("sudo systemctl enable docker")

def install_docker_compose():
    print("Docker Compose not found. Installing Docker Compose...")
    os.system("sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose")
    os.system("sudo chmod +x /usr/local/bin/docker-compose")

def create_wordpress_site(site_name):
  """Creates a WordPress site using Docker.

  Args:
    site_name: The name of the WordPress site.

  Returns:
    A docker.DockerClient object.
  """

  client = docker.from_env()

  # Create the docker-compose file.
  #CHANGED DOCKER COMPOSE FILE FOR BETTER SECURITY
  docker_compose_file = """
version: '3.8'
services:
  db:
    image: mysql:5.7
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: my_root_password
      MYSQL_DATABASE: my_database
      MYSQL_USER: my_user
      MYSQL_PASSWORD: my_user_password
    # Don't expose the MySQL port to the host or public network
    # Ports will be accessible within the Docker network.
    ports:
      - "127.0.0.1:3306:3306"
    volumes:
      - db_data:/var/lib/mysql

  wordpress:
    depends_on:
      - db
    image: wordpress:5.8
    restart: always
    ports:
      - "80:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: my_user
      WORDPRESS_DB_PASSWORD: my_user_password
      WORDPRESS_DB_NAME: my_database
    volumes:
      - wp_data:/var/www/html

volumes:
  db_data:
  wp_data:

  """.format(site_name, site_name)

  with open("docker-compose.yml", "w") as f:
    f.write(docker_compose_file)
  boo=True
  x=0
  while boo==True:
    usr_inp=input("Enable/Disable/Delete the website. Or write Exit to escape the program").lower()
    if usr_inp=="enable":
      # Create the containers.
      subprocess.run(["docker","compose", "-f", "docker-compose.yml","up", "-d"])

      # Create the /etc/hosts entry.
      subprocess.run(["sudo", "echo", "127.0.0.1 {}".format(site_name), ">>", "/etc/hosts"])
      print("WordPress site created successfully. Open {} in a browser to view the site.".format(site_name))
      x=1
    elif (usr_inp== "disable" and x==1):
       subprocess.run(["docker","compose", "-f", "docker-compose.yml","down"])
       print("Wordpress disabled!!")
       x=0
    elif (usr_inp=="disable" and x==0):
       print("No containers to disable")
    elif usr_inp=="delete":
        if x==1:
          subprocess.run(["docker","compose", "-f", "docker-compose.yml","down", "--volumes"])
          print("Containers deleted")
        else:
           print("nothing to delete")
    elif usr_inp=="exit":
       return 0
    else:
       print("wrong command, retry")
  return client

def main():
  """Creates a WordPress site using the provided site name."""
  docker_installed = check_docker_installed()
  docker_compose_installed = check_docker_compose_installed()

  if not docker_installed:
      install_docker()
  else:
      print("Docker is already installed.")

  if not docker_compose_installed:
      install_docker_compose()
  else:
      print("Docker Compose is already installed.")
  site_name = input("Enter the name of the WordPress site: ")

  client = create_wordpress_site(site_name)
  
  

if __name__ == "__main__":
  if os.geteuid() != 0:
        print("This script requires root privileges. Please run it with sudo.")
        sys.exit(1)
  main()
