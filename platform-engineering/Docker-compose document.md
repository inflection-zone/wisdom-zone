# Deploy service to Docker using docker-compose:

* STEP 1: Create a service with APIs.

* Step 2: Make sure your service is running successfully on local system.

* Step 3: Download & install docker on your system.

* Step 4: Create a Dockerfile inside your service folder with name "Dockerfile":
  (https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
  * Click on create new file.
  * Name it as "Dockerfile".
  * Add VS Code suggested extension for Docker.

* Step 5: Create a docker-compose file with yaml OR yml extension.(eg. docker-compose.yaml OR docker-compose.yml)
    (https://www.youtube.com/watch?v=_JNTTgRDyBQ One can refer this video tutorial for creating & running docker compose file for node.js app using mysql database.)

* Step 6: Go to .env file and change database configuration variable values according to your docker-compose file.

* Step 7: Open terminal insde your service folder. Write command ```docker-compose up --build```.
  ("docker-compose up" command starts the containers. "--build" option build images before starting containers.)

* Step 8: You may see your built image & list of all other images using ```docker images``` or ```docker image ls``` command.

* Step 9: To see list of running containers, use "docker ps" command. To see list of all running and exited containers, use "docker ps -a" command.

* Step 10: You may access your containers using ```docker exec -it <container name> /bin/bash``` command.
  (If bash is not installed you may use ```docker exec -it <container name> /bin/sh```)

* Step 11: Inside database container, login to mysql using ```mysql -u<username> -p``` command. It will prompt you to enter password. \* After login you may see databases, tables, use other mysql commands.

* Step 12: Send API requests from postman and you can see changes in database in container as well.
