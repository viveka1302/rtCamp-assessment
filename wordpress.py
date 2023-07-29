import subprocess
import docker

def create_wordpress_site(site_name):
  """Creates a WordPress site using Docker.

  Args:
    site_name: The name of the WordPress site.

  Returns:
    A docker.DockerClient object.
  """

  client = docker.from_env()

  # Create the docker-compose file.
  docker_compose_file = """
version: '3'
services:
  db:
    image: mysql:latest
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: {}
      MYSQL_USER: user
      MYSQL_PASSWORD: password
  wordpress:
    depends_on:
      - db
    image: wordpress:latest
    restart: always
    ports:
      - 80:80
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: user
      WORDPRESS_DB_PASSWORD: password
      WORDPRESS_DB_NAME: {}
  """.format(site_name, site_name)

  with open("docker-compose.yml", "w") as f:
    f.write(docker_compose_file)

  # Create the containers.
  subprocess.run(["docker","compose", "-f", "docker-compose.yml","up"])

  # Create the /etc/hosts entry.
  subprocess.run(["sudo", "echo", "127.0.0.1 {}".format(site_name), ">>", "/etc/hosts"])

  return client

def main():
  """Creates a WordPress site using the provided site name."""

  site_name = input("Enter the name of the WordPress site: ")

  client = create_wordpress_site(site_name)

  print("WordPress site created successfully. Open {} in a browser to view the site.".format(site_name))

if __name__ == "__main__":
  main()