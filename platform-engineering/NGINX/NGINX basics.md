# Introduction To NGINX

- NGINX is an open-source software for web serving, reverse-proxying, caching, load balancing & media streaming.
- It is a high performance web server developed to facilitate the increasing needs of the modern web. It focuses on high performance, high concurrency, and low resource usage.
- In its initial release, NGINX functioned for HTTP web serving. Today, however, it also serves as a reverse proxy server for HTTP, HTTPS, SMTP, IMAP, POP3 protocols, on the other hand, it is also used for HTTP load balancer, HTTP cache, and email proxy for IMAP, POP3, and SMTP.

# Why NGINX

- NGINX is fast.
- Accelerates your application
- Has load balancers
- Affordable to install and maintain
- Easy to use
- Can get upgraded on fly
- Scaling capability
- Few resources requirement & consumption
- Multiple protocol support: HTTP, HTTPS, WEBSOCKET, IMAP, POP3, SMTP
- Video streaming using MP4/FLV/HDS/HLS
- Live streaming

# Architecture of NGINX

   <img src="NGINX architecture.png" width="600" height="250"/>

NGINX uses a predictable process model that is tuned to the available hardware resources:

- The **master** process performs the privileged operations such as reading configuration and binding to ports, and then creates a small number of child processes (the next three types).
- The **cache loader** process runs at startup to load the disk based cache into memory, and then exits. It is scheduled conservatively, so its resource demands are low.
- The **cache manager** process runs periodically and prunes entries from the disk caches to keep them within the configured sizes.
- The **worker** processes do all of the work! They handle network connections, read and write content to disk, and communicate with upstream servers.

# Install NGINX

1.  Install Oracle VM Virtualbox. (Download it from https://www.virtualbox.org , according to your OS.)
2.  Download Ubuntu ISO desktop image from https://ubuntu.com/download/desktop. (Download LTS version).
3.  Inside Virtualbox, click on New. You will see following screen.

     <img src="InstallStep1.png" width="600" height="300"/>

        - Give proper name to your VM in 'Name' field.
        - Select downloaded Ubuntu ISO image at “ISO Image” field.
        - Click on Next

    &nbsp;<br>

4.  You will see thr screen as :

    <img src="install2.png" width="600" height="300"/>

        - Give Username & password of your choice. Click on Next

    &nbsp;<br>

5.  Next you have to configure your VM’s hardware configs.

    <img src="install3.png" width="600" height="300"/>

        - Select at least 2GB RAM & 1 Processor. Click on Next.
        - Select Create a Virtual Hard Disk. Click Next & Finish

    &nbsp;<br>

6.  Then go to Settings tab => Network => Adapter1 => Select Bridged Adapter
    <img src="install4.png" width="600" height="300"/>

&nbsp;<br> 7. Start VM & login with password. 8. Update VM with `sudo apt-get update`. (You may continue with existing user or switch to root user using `su root` & enter password. If root user you need not to write “sudo” keyword before every command.) 9. Install NGINX using `apt-get install nginx` command.

- Once completed, check version using `nginx -v`.
- You may also check in browser whether nginx is installed properly on your VM using following steps:

  - Check IP address of your VM using “ip addr” command.
  - Hit this IP in the browser & you may get response like:

   <img src="nginxRes1.png" width="600" height="300"/>

&nbsp;<br>

- Check status of Nginx service using `systemctl status nginx`(or `service nginx status`).
- If inactive, start Nginx service using `systemctl start nginx`.
- To check processes running on Nginx use `ps aux | grep nginx`. It will display master & no. of worker processes running.
- To see and change configurations check nginx.conf file using `vi /etc/nginx/nginx.conf`.
- Use the following command to test the Nginx configuration for any syntax or system errors:
  `nginx -t`
  The output will look something like this:

  <img src="nginx-t.png" width="600" height="300"/>
  &nbsp;<br>

# NGINX Directives & Contexts

- Configuration options in Nginx are known as directives.
- Nginx consists of modules that are controlled by directives defined in the configuration file.
- Directives are divided into two parts:
  1. **Simple Directive**:
     A simple directive consists of the name and parameters separated by spaces and ends with a semicolon ( ; )
  2. **Block Directive**:
     The structure of block directive is similar to the simple directive, but instead of semicolon, it ends with a set of additional instructions surrounded by curly braces ({ and }).
     If a block directive can have other directives inside the braces, then it is known as context. Eg. Events, http, location, and server.
- In Nginx configuration file, we will notice that the configurations are organized in a tree-like structure surrounded by curly braces i.e. "{" and "}". These locations surrounded by braces is called **context** for placing configuration directive.
- This is the section where we can declare directives. It is similar to the scope in a programming language.
- Context can be nested within other contexts, creating a context hierarchy.
- Types of contexts:

  - **Main/ Global Context**:
    - The main context is placed at the beginning of the core Nginx configuration file. The directives for this context cannot be inherited in any other context and therefore can't be overridden.
    - The main context is used to configure details that affect the entire application on a basic level. Some common details that are configured in the main context are the user and group to run the worker processes as, the total number of workers, and the file to save the main process ID. The default error file for the entire application can be set at the main context level.
  - **Events Context**:
    - The events context sets global options for connection processing. There can be only one event context defined within Nginx configuration.
    - Nginx uses an event-based connection processing model, so the directive defined within this context determines how worker processes should handle connections.
  - **HTTP context**:

    - The HTTP context is used to hold the directives for handling HTTP or HTTPS traffic.

  - **Server Context**:
    - The server context is declared within the http context.
    - The server context is used to define the Nginx virtual host settings.
    - There can be multiple server contexts inside the HTTP context.
    - The directives inside the server context handle the processing of requests for resources associated with a particular domain or IP address.
  - **Location Context**:
    - It define directives to handle the request of the client. When any request for resource arrives at Nginx, it will try to match the URI (Uniform Resource Identifier) to one of the locations and handle it accordingly.
    - Multiple location contexts can be defined within the server blocks. Moreover, a location context can also be nested inside another location context.

- Directives placed in the configuration file outside of any contexts are considered to be in the main context.
- The 'events' and 'http' directives reside in the 'main' context, 'server' resides in 'http' and 'location' in the 'server' context.

# Understanding Configuration File

Here is an example of nginx.conf file:

<img src="nginx.conf.png" width="600" height="300"/>

&nbsp;<br>

- The first three lines of the file are in main/global context.

  - Here, the first directive i.e. `worker_processes auto;` shows how many worker processes are running. You may change it by replacing "auto" with your desired value.
  - The PID file stores the main process ID of the nginx process

- The “events” context is contained within the “main” context. `worker_connections` directive in events context tells how many max. connections a worker process can have

- When configuring Nginx as a web server or reverse proxy, the “http” context will hold the majority of the configuration. This context will contain all of the directives and other contexts necessary to define how the program will handle HTTP or HTTPS connections.

  - Some of the directives that are defined in http contexts are: control the default locations for access and error logs (access_log and error_log), configure asynchronous I/O for file operations (aio, sendfile, and directio), and configure the server’s statuses when errors occur (error_page).
  - Other directives configure compression (gzip and gzip_disable), the rules that Nginx will follow to try to optimize packets and system calls (sendfile, tcp_nodelay, and tcp_nopush).
  - Additional directives configure an application-level document root and index files (root and index) and set up the various hash tables that are used to store different types of data (_\_hash_bucket_size and _\_hash_max_size for server_names, types, and variables).

- The “server” context is declared within the “http” context. The reason for allowing multiple declarations of the server context is that each instance defines a specific virtual server to handle client requests. You can have as many server blocks as you need, each of which can handle a specific subset of connections.

  - The directives which decide if a server block will be used to answer a request are:

    - **listen**: The ip address / port combination that this server block is designed to respond to. If a request is made by a client that matches these values, this block will potentially be selected to handle the connection.
    - **server_name**: This directive is the other component used to select a server block for processing. If there are multiple server blocks with listen directives of the same specificity that can handle the request, Nginx will parse the “Host” header of the request and match it against this directive.

- The next context is the location context. Multiple location contexts can be defined, each location is used to handle a certain type of client request, and each location is selected by virtue of matching the location definition against the client request through a selection algorithm. Location blocks live within server contexts and, unlike server blocks, can be nested inside one another.
