# Deploy service to Docker using docker-compose:

##Steps

1. Create a service with APIs.

2. Make sure your service is running successfully on local system.

3. Download & install docker on your system.

* Step 4: Create a Dockerfile inside your service folder with name "Dockerfile":
  (https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
  * Click on create new file.
  * Name it as "Dockerfile".
  * Add VS Code suggested extension for Docker.

  An example of a Dockerfile is given below:

```
FROM node:19-alpine3.16 AS builder
ADD . /app
RUN apk add bash
RUN apk add --update alpine-sdk
WORKDIR /app
COPY package*.json /app/
RUN npm install -g typescript
COPY src ./src
COPY tsconfig.json ./
RUN npm install
RUN npm run build

# RUN npm run build

FROM node:19-alpine3.16
RUN apk add bash
RUN apk add --update alpine-sdk
RUN apk update
RUN apk upgrade
ADD . /app
WORKDIR /app
COPY package*.json /app/
# RUN npm install pm2 -g
# RUN npm install sharp
COPY --from=builder ./app/dist/ .
EXPOSE 3000
CMD ["npm","run","start"]
```

* Step 5: Create a docker-compose file with yaml OR yml extension.(eg. docker-compose.yaml OR docker-compose.yml)
    (https://www.youtube.com/watch?v=_JNTTgRDyBQ One can refer this video tutorial for creating & running docker compose file for node.js app using mysql database.)

    Example of a docker-compose file:

```
services:
  mysqldb:
    image: mysql:8.0
    container_name: mysqlcontainer
    command: --default-authentication-plugin=mysql_native_password
    restart: unless-stopped
    volumes:
      - ./dbinit/init.sql:/docker-entrypoint-initdb.d/0_init.sql
      - $HOME/database:/var/lib/mysql
    ports:
      - 3306:3306
    expose:
      - 3306
    environment:
      MYSQL_DATABASE: schooldb
      MYSQL_USER: admin
      MYSQL_PASSWORD: letmein
      MYSQL_ROOT_PASSWORD: letmein
      SERVICE_TAGS: prod
      SERVICE_NAME: mysqldb
    networks:
      - internalnet

  nodeapp:
    container_name: school-service-container
    build: .
    image: school-service:1.0
    volumes:
      - $HOME/nodeapp:/code
    ports:
      - 3000:3000
    expose:
      - 3000
    environment:
      DB_HOST: mysqldb
      DB_PORT: 3306
      DB_USER: admin
      DB_PASSWORD: letmein
      DB_NAME: schooldb
      DB_CONNECTION_LIMIT: 20
      SERVICE_TAGS: prod
      SERVICE_NAME: school-service
      SERVER_PORT: 3000
    depends_on:
      - mysqldb
    networks:
      - internalnet
networks:
  internalnet:
    driver: bridge
  ```


* Step 6: Go to .env file and change database configuration variable values according to your docker-compose file.

* Step 7: Open terminal insde your service folder. Write command ```docker-compose up --build```.
  ("docker-compose up" command starts the containers. "--build" option build images before starting containers.)

* Step 8: You may see your built image & list of all other images using ```docker images``` or ```docker image ls``` command.

* Step 9: To see list of running containers, use "docker ps" command. To see list of all running and exited containers, use "docker ps -a" command.

* Step 10: You may access your containers using ```docker exec -it <container name> /bin/bash``` command.
  (If bash is not installed you may use ```docker exec -it <container name> /bin/sh```)

* Step 11: Inside database container, login to mysql using ```mysql -u<username> -p``` command. It will prompt you to enter password. \* After login you may see databases, tables, use other mysql commands.

* Step 12: Send API requests from postman and you can see changes in database in container as well.
