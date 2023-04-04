# Dockerize a Full-stack application with Node.js, MySQL and Nginx

* **Objective** 
    * In this tutorial, we will dockerize an already built full stack application that uses Svelte as front-end, node.js as a backend service and MySQL as the application database.
    * We will also add NGINX as a reverse-proxy in this application and dockerize the whole application using docer compose.
    * We are having a simple application that uses node.js for a server that will process all requests to either add, get,  update or delete users from a database.
    * Here we need to create two separate dockerfiles for frontend and backend services. And then we will add NGINX configuration file and then we will dockerize NGINX as well. 
    * To combine the whole application and spin all the containers at the same time, we will use docker compose.
    * One may find the source code for this application here: https://github.com/Priyanka-Inflectionzone/docker-compose-nginx-demo 

* **Steps:**
    1. Create a dockerfile for backend server. 
        - Create a new file inside backend application folder and name it Dockerfile. 
        - Add following to this file.

    ```
       FROM node:18-alpine3.16 
       EXPOSE 3456
       WORKDIR /app 
       RUN apk add bash
       COPY package*.json /app/
       COPY tsconfig.json /app/
       RUN npm install 
       COPY src ./src/
       RUN npx prisma generate
       COPY . .
       CMD ["npm", "run", "start:migrate"] 
    ```
    

    2. Create a dockerfile for frontend.
        - Create a new file in frontend folder and name it Dockerfile.
        - Add following lines to this file.

    ```
       FROM node:18-alpine3.16
       EXPOSE 3000
       WORKDIR /app
       RUN apk add bash
       COPY package*.json /app/
       COPY tsconfig.json /app/
       RUN npm install
       RUN npm run build
       COPY . .
       CMD ["node", "index.js"]
    ```

    3. Setting up NGINX server. 
        - Create an "nginx" folder. Here, we will write the Nginx server proxy configurations to power up frontend application. 
        - Inside the Nginx folder, create a default.conf file.
        - Add the following into it: 

    ```
       upstream api {
         server frontend:3000;
       }

       server {
          listen 80;

          location / {
             proxy_pass http://api;
          }
       }

    ```

    4. Create Nginx server dockerfile.
        - Inside the Nginx folder, create a Dockerfile and include the following to pull the Nginx image and execute the default.conf file.

    ```
      FROM nginx:1.18.0
      EXPOSE 80
      COPY ./default.conf /etc/nginx/conf.d/default.conf 

    ```
       
    5. Create a docker-compose file.
        - We are now all set to spin up everything together with the docker-compose.yml.
        - In the project root directory, create a docker-compose.yml file.
        - Add following to it.

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
            - 80:80 
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


    6. Run and test containerized application.
        - Everything is now ready.
        - In project root directory, execute the following command to run the docker-compose.yml file.

            `docker compose up --build -d`

        - This will build and run all the containers in Docker.

        <img src="./Images/docker1.png" width="600" height="230"/>
         &nbsp;<br>

        - To start interacting with the application, open http://localhost:80/ on a browser. You may add user using "/user" route. 
        
        &nbsp;<br>
        <img src="./Images/output1.png" width="600" height="230"/>
         &nbsp;<br>

        - You can access the Adminer using route http://localhost:8000 

         &nbsp;<br>
        <img src="./Images/output2.png" width="600" height="230"/>
         &nbsp;<br>



