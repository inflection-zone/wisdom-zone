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

    <img src="install1.png" width="600" height="300"/>

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

- Check status of nginx service using `systemctl status nginx`(or `service nginx status`).
- If inactive, start nginx service using `systemctl start nginx`.
- To check processes running on nginx use `ps aux | grep nginx`. It will display master & no. of worker processes running.
- To see and change configurations check nginx.conf file using `vi /etc/nginx/nginx.conf`.
