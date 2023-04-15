# Ways to populate environment variables in Docker containers

### 1. Docker Compose Environment Variables: 
* In docker compose, environment variables can be set in `docker-compose.yml` file using `environment` keyword.
* These variables can be passed to the container at runtime.
* Let's see how it works with an example. We have an already created application having frontend-service, backend-service, NGINX and mysql database. You may find the source code [here](https://github.com/Priyanka-Inflectionzone/docker-compose-nginx/blob/master/docker-compose.yaml).
* `docker-compose.yml` file has following configs:
```
version : "3.8"
services:
  mysqldb:
    image: mysql:8.0
    container_name: myuserdbcontainer
    command: --default-authentication-plugin=mysql_native_password
    restart: unless-stopped
    volumes: 
      - db:/var/lib/mysql
    ports:
      - 9906:3306
    expose:
      - 3306
    environment:
      MYSQL_DATABASE: db
      MYSQL_USER: admin
      MYSQL_PASSWORD: password
      MYSQL_ROOT_PASSWORD: password
      SERVICE_NAME: mysqldb
    networks:
      - internalnet

  nodeapp:
    container_name: node-service-container
    build: ./prisma-api-mysql
    image: node-service:1.0 
    command: bash -c 'while !</dev/tcp/mysqldb/3306; do sleep 20; done; npm run start:migrate' 
    ports:
      - 3456:3456
    expose:
      - 3456
    environment:
      DATABASE_URL: "mysql://admin:password@mysqldb:3306/db?schema=public" 
    depends_on:
      - mysqldb  
    networks:
      - internalnet

  frontend:
    container_name: frontend-container
    build: ./Svelete-skeleton
    image: frontend:1.0 
    ports:
      - 3000:3000
    expose:
      - 3000
    environment:
      BACKEND_API_URL: "http://nodeapp:3456" 
    depends_on:
      - mysqldb 
      - nodeapp 
    networks:
      - internalnet

  nginx:
    depends_on:
      - frontend
      - nodeapp
    restart: unless-stopped
    build:
      dockerfile: Dockerfile
      context: ./nginx
    ports:
      - "80:80" 
    networks:
      - internalnet

  adminer:
    image: adminer:latest
    restart: unless-stopped
    ports:
      - 8000:8080
    depends_on:
      - mysqldb
    environment:
      ADMINER_DEFAULT_SERVER: mysqldb
    networks:
      - internalnet

volumes: 
  db: 
  
networks:
  internalnet:
    driver: bridge 
```
* You may see in this file, we have set databse credentials as environment variables in first service configuration i.e. `mysqldb` service.
* Then for nodeapp service, `DATABASE_URL` is an environment variable, for frontend service, it is `BACKEND_API_URL` and for adminer, we have set `ADMINER_DEFAULT_SERVER` as environment variable. 
* Now when we run `Docker compose up --build -d`, the containers of all services spin up and given environment variables are passed to them.
* If you want to check these environment variables inside containers, open `docker desktop`. You may see your running containers here. Click on any one container, let's take database container. Then click on `Terminal` tab. It opens terminal inside container. Here run command `env`. You may see all the environments variables that we have set in `docker-compose.yml` file are present in container. In this way, you may check other containers too.
    <img src="./Images/dbContainer.png" width="600" height="230"/>
         &nbsp;<br>
    
    <img src="./Images/appContainer.png" width="600" height="230"/>
         &nbsp;<br>

    <img src="./Images/frontend.png" width="600" height="230"/>
         &nbsp;<br>

    <img src="./Images/adminer.png" width="600" height="230"/>
         &nbsp;<br>


### 2. Docker Run command using `-e` or `--env` flag: 

* While running container using `docker run` command, you can specify environment variables using `-e` or `--env` flag. 
* For example:
     `$ docker run -e VAR1=value1 -e VAR2=value2 <image-name>` 
     or
     `$ docker run --env VAR=value <image-name>` 

* You can also specify file containing environment variables using `--env-file`. For example:
    ` $ docker run --env-file <path-of-file> <image-name>` 

* Let's see it with example. Let's run a container using docker image which I have already created and stored to docker hub. Run the following command from your terminal:
    `$ docker run -p 3000:3000 -d -e BACKEND_API_URL="http://localhost:3001" priyankainflectionzone/frontend-app:2.0` 

* You may check running container using `$ docker ps` command.
    <img src="./Images/flag1.png" width="600" height="230"/>
         &nbsp;<br>

* Now go to docker desktop. Select your running container. Click on terminal and run command `env`. you may see environment variable you set in docker run command is present in the container.
    <img src="./Images/flag1-1.png" width="600" height="230"/>
         &nbsp;<br> 

### 3. Using Dockerfile: 

* We can pass environment variables in the Dockerfile as well. 
* `ENV` instruction is used to set environment variables in Dockerfile. For example: `ENV VAR1=value`
* These variables will be available to the container at runtime.
* Example configuration:
  -  Before we see how to pass environment variable values into a Dockerfile, let's build an example to test it out.
  - We'll create a simple bash script called `greetings.sh`, which uses an environment variable to print greetings to the console:
  ```
    #!/bin/sh

    echo Hello $name
  ```

  - Now we'll create a Dockerfile in the same directory:
  ```
    FROM alpine:latest

    ENV name Priya

    COPY greetings.sh .

    RUN chmod +x /greetings.sh

    CMD ["/greetings.sh"]
  ```

  - Now we'll build and run our image.
  ```
    $ docker build -t greetings .

    $ docker run greetings
  ```

  - Here is our console output:

  <img src="./Images/env-dockerfile.png" width="600" height="250"/>
         &nbsp;<br> 
