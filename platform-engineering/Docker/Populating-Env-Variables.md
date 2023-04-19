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

  <img src="./Images/env-dockerfile.png" width="600" height="150"/>
         &nbsp;<br> 

### 4. Using `.env` file: 
* To pass environment variables in docker containers, there is one more way i.e. to have an `.env` file.
* Essentially, an `.env` file is a list of key pair values that set specific variables for a container deployment.
* A few things to keep in mind about .env files:
  - The .env file is used during the pre-processing step with docker-compose.yml files.
  - To pass variables from the .env file to the command, you use $ as in $DB_DATABASE.
  - ENV values are available via docker-build or run commands (using the $ as explained above).
  - ENV files allow you to pass multiple environment variables at once.
  - You can pass the .env file variables to the docker run command using the –env-file options, for example: $ docker run –env-file .env mysql:latest

* Let's create an `.env` file for our project. For that, go to project folder and create new file. Name it as `.env`.
* Now suppose we have to pass one variable "API_BACKEND_URL" having value as "http://localhost:5000". Let's add it to our .env file as: `BACKEND_API_URL=http://localhost:3456` and save the file.
* Now we will create a Dockerfile.
* Then build a docker image out of dockerfile and run that image with `--env-file`. For example: `$ docker run --env-file .env app1:2.0 `

  > **Note**: Make sure to use the full path to your .env file (if you’re not running the docker command from the same directory housing the file).

* Your container will deploy and be ready to use. You may go to docker-desktop and check inside your container for `env` variables.
  <img src="./Images/env-file.png" width="600" height="250"/>
         &nbsp;<br>


### 4. Using System Management Parameters: 

* If you want to run docker containers on AWS EC2 instance, you may store environment variables in System Management Parameters store.
* Then you may retrieve value of that parameter inside your EC2 instance (either in Userdata script or terminal of instance) and use it as environment variable to run a docker container.
* For this method, you need to have an AWS account and your user must have permissions to create & access all the required resources.
* Let's try an example. We will create a SSM parameter `dburl` to use as `DATABASE_URL` in backend container. For that follow these steps: 
  1. Login to your AWS Console.
  2. Go to `Services` --> `RDS`.
  3. Click on `Create Database`.
  4. Here select `Standard create`. Under engine options, select `mysql`. Then select `Free Tier` template.
  5. Then under credentials setting, set a new password and confirm it.
  6. Select instance type as `t3.micro` and allocate 10 GB storage. 
  7. Create new security group `db-1-sg`. Give initial database name as `userdb`.
  8. Keep rest of configurations as they are. And click on `Create Database`. 
  9. Now to create parameter, go to `services` --> `AWS Systems Manager` --> `Parameter Store`.
  10. Now click on `Create Parameter`.
  11. Assign a name to parameter. Then select `standard` tier. Select `String` type. 
  12. In `Value` field, write `mysql://<db-username>:<password>@<RDS-Endpoint>:3306/<db Name>`. And click on `Create Parameter`. 
    > **Note**: Here replace `db-username`, `password` and other things with your values.
  13. Now we have to create a role having permission to access RDS instance as well as System parameter. For that go to `Services` --> `IAM` --> `Roles`.
  14. Click on `Create role`. Select `AWS service` as entity type and `EC2` as use case. Click on `Next`.
  15. Here we have to attach policies to our role. Select `AmazonRDSReadOnlyAccess` and `AmazonSSMManagedInstanceCore` policies. Click on `Next`.
  16. Now give a name to role like `EC2-RDS-SSM-Role`. And click on `Create Role`.
  17. Finally we will launch our EC2 instance (ubuntu) with following userdata script: 
  ```
  #!/bin/bash
  apt-get update
  apt-get install -y docker.io

  usermod -aG docker ubuntu

  apt-get install -y awscli 
  ```
  18. Then login to your instance using `mobaxterm` and try to spin containers using following commands: 
  ```
    $ docker network create my-network
  ```
  ```
    $ docker run --name backend --network my-network -e DATABASE_URL="$(aws ssm get-parameter --region "ap-south-1" --name "dburl" --query Parameter.Value --output text)" -d priyankainflectionzone/backend-app:1.0 
  ```
  ```
    $ docker run -d --name app-container -p 3000:3000 --network my-network -e BACKEND_API_URL="http://backend:3456" priyankainflectionzone/frontend-app:2.0
  ```

  19. Now copy the public IP of EC2 instance, and paste it to browser with port no. 3000. as our frontend app is running on port 3000. You may see the index page of our application. 

    <img src="./Images/ssm-1.png" width="600" height="250"/>
         &nbsp;<br>


### 5. Using Kubernetes: 
* In kubernetes, you can set environment variables in Pod's container using the `env` field in the container spec.
* For example:
  ```
    spec:
      container:
        name: app-container
        image: app:1.0
        env:
         - name: VAR1
           value: "value1"
  ```

* But this not the proper way to poulate environment variables having sensitive data. 
* Kubernetes provides `ConfigMaps` and `Secrets` to manage application configuration data.
* `ConfigMaps` are used to store non-sensitive data while `Secrets` are used to store sensitive data.
* Both `ConfigMaps` and `Secrets` can be mounted as environment variables in a container.
* Let's take an example. Suppose we need to spin a container with mysql image. So we will save its usename and password as `Secrets` and db-name as `ConfigMap`.
* For that you need to start a minikube cluster on your system or you may use AWS EKS cluster too. In this example, I am using minikube cluster.
* So go to terminal and run command `minikube start`. It will create a local minikube cluster. 
* Now create a directory for storing our manifest and other config files.
* Then save db username and password as secrets using following commands:
```
 $ kubectl create secret generic mysqluser --from-literal=MYSQL_USER=admin
```
```
 $ kubectl create secret generic mysqlpassword --from-literal=MYSQL_PASSWORD=password
```
```
 $ kubectl create secret generic mysqlrootpassword --from-literal=MYSQL_ROOT_PASSWORD=password
```

* Now let's save database name as ConfigMap.
```
 $ kubectl create configmap dbname --from-literal=MYSQL_DATABASE=userdb
```
* Next create a manifest file `main.yml` describing Pod's configurations as: 
```
 apiVersion: v1
 kind: Pod
 metadata:
  name: envtest
  namespace: default
 spec:
  containers:
    - name: dbcontainer12345
      image: mysql:8.0
      ports:
        - containerPort: 3306
      env:
        - name: MYSQL_DATABASE
          valueFrom:
            configMapKeyRef:
              name: dbname
              key: MYSQL_DATABASE
        - name: MYSQL_USER
          valueFrom:
            secretKeyRef:
              name: mysqluser
              key: MYSQL_USER
        - name: MYSQL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysqlpassword
              key: MYSQL_PASSWORD
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysqlrootpassword
              key: MYSQL_ROOT_PASSWORD
```
* Go to terminal and run command: `$ kubectl apply -f main.yml`. And you may see your Pod is created with mentioned container having all environment variables which you have set.

* If you run command `$ kubectl describe pod <podname>`, you may see in the `Environment` field of container specs, all env variables are passed.