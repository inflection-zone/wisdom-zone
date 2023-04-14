# Automated Nginx Reverse Proxy for Docker Containers

## Objective
* Auto-generate NGINX reverse-proxy configs for docker container.

## Prerequisites
* Docker should be installed on your system.

## Overview
* In this tutorial, we are going to generate NGINX reverse-proxy configs for docker container.
* For this purpose, we will run an already created docker image `priyankainflectionzone/frontend-app:2.0`. 
* For generating configs automatically, we are going to use a docker image [jwilder/nginx-proxy](https://hub.docker.com/r/jwilder/nginx-proxy).
* For more information about this, please go through Jason Wilder's blog: http://jasonwilder.com/blog/2014/03/25/automated-nginx-reverse-proxy-for-docker/ 

> **Note**: The containers being proxied must expose the port to be proxied, either by using the EXPOSE directive in their Dockerfile or by using the --expose flag to docker run or docker create and be in the same network. 

## Steps:
1. Open your windows terminal app. First run a docker container using our application docker image with a VIRTUAL_HOST environment variable as: 
    ```
    $ docker run -d --name app-container -p 3000:3000 -e VIRTUAL_HOST=localhost priyankainflectionzone/frontend-app:2.0
    ```
2. Then check in the browser if you app displays on port 3000. using `http://localhost:3000`. You may see the following screen:

     <img src="./Images/auto-1.png" width="600" height="230"/>
         &nbsp;<br>

3. Now come back to terminal and run another container using `nginx-proxy` image.
    ```
    $ docker run -d -p 80:80 -v /var/run/docker.sock:/tmp/docker.sock -t jwilder/nginx-proxy
    ```

4. You may check list of containers running by using command 
    ```
    $ docker ps
    ```
5. Now you may browse `http://localhost:80` and see that the same application running on port 80. That means NGINX has redirected requests coming on port 80 to our application port. 

    <img src="./Images/auto-2.png" width="600" height="230"/>
         &nbsp;<br>

6. Now if you check inside nginx-container, you may see that default.conf file is automatically generated and having reverse-proxy configs for our app-container. Follow these steps to check: 
     - Run command to step into container: 
    ` $ docker exec -it <container-id/name> /bin/bash`
    - Then go to path `etc/nginx/conf.d` and list the directory contents using `ls`. It will show `default.conf`.
    - Now use command `$ cat default.conf ` to see the contents of conf file. You may see the following configs: 

    <img src="./Images/config.png" width="600" height="230"/>
         &nbsp;<br