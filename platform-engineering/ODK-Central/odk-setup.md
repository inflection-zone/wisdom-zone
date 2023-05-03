# Setup ODK Server on AWS
## Prerequisites
* An AWS account
* Basics of Docker and docker commands.

## Steps To Launch An EC2 Instance
1. Login to your AWS account.
2. Search in services for `EC2`. Select `EC2` Service. Select your desired region (in this case `ap-south-1` i.e. `Mumbai`).
    <img src="../AWS/EC2-1.png" width="600" height="250"/>
     &nbsp;<br>

3. On EC2 Dashboard, click on `Instances`. Select `Launch Instances`.
    <img src="../AWS/EC2-2.png" width="600" height="250"/>
     &nbsp;<br>

4. Then you need to give specifications for your instance like its name, AMI, Instance type, storage etc. In our case, we've selected `Ubuntu 22.04 LTS` AMI and `t3.medium` instance type. We have associated 20GB of storage to it. 

5. For security group settings, open ports for `SSH(22)`, `HTTP(80)` and `HTTPS(443)`.

6. Then specify a `secret key-pair` for logging in to instance. If you already have a key, you may assign it to instancwe or you may create a new key-pair. 

    <img src="./Images/key-pair.png" width="600" height="250"/>
     &nbsp;<br>

7. We need to install `Docker`, `Docker Compose` and `git` in our instance. You may install all of them after launching the instance but in this tutorial, we will give following `Userdata` script to install them while launching the instance. 
    ```
    #!/bin/bash
    apt-get update
    apt-get install -y cloud-utils apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
    apt-get update
    apt-get install -y docker-ce
    usermod -aG docker ubuntu

    # Install docker-compose
    curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose 

    # Install git and clone git repository
    apt-get install git

    ```
8. Click on `Launch Instance`. Our server is ready.

## Create DNS for EC2 Instance
* Now you need to set up a domain name. We will do so, and then configure it so that it sends users to the server you created in the previous step.

* You'll need to do this for two reasons: a memorable name (like google.com) will be easier to remember and access than a pile of numbers, and you cannot get a security certificate without one. It is not currently possible to host Central within a subdirectory on another domain (so, my-website.com/my-odk-server is not possible, but my-odk-server.com is allowed, as is my-odk-server.my-website.com).

* If you already have a domain name, you may configure that but if you don't, you need to follow these steps to create one: 
    1. You can pay one of the many popular commercial domain registrars for a full domain name, like MyOdkCentralServer.com. Search for "domain registrar" to find one of these. These often cost as little as $3/year. 
    2. You can use a free DNS service: we recommend [FreeDNS](https://freedns.afraid.org/), which has run for a long time and has a good reputation. With it, you can get a free name, albeit with a fixed second half (like MyOdkCentralServer.dynet.com).
    3. I've selected `mooo.com` as domain and `myserverodk` as subdomain. So the whole DNS will be `myserverodk.mooo.com.` Then assign public IP of EC2 instance to this DNS.

## Install ODK Central
1. Login into instance using `Mobaxterm`. For this you will need to install `Mobaxterm` first (You may get it [here](https://mobaxterm.mobatek.net/download.html)). To login into server you need to follow these steps: 
    - Open `Mobaxterm`. Click on `Session`.
    - In the next window, click on `SSH`. 
    - Then paste public IP of instance in the field `Remote Host`. Specify user as `ubuntu`. 
    - Then click on `Advanced SSH Settings`. Select `Use Private Key`. Browse for `key-pair` used at the time of instnace launch. Click on `Ok`.
&nbsp;<br>

2. You will be logged in into instance. First check whether `Docker` & `Docker Compose` is installed on server. Use command: 
    ```
    $ docker --version && docker compose version
    ``` 

3. Next download the software. In the server window, type:
    ```
    $ git clone https://github.com/getodk/central
    ``` 
    and press Enter. It should think for some time and download many things.

4. Go into the new central folder:
    ```
    $ cd central
    ```

5. Get the latest client and server:
    ```
    $ git submodule update -i
    ```

6. Update settings. First, copy the settings template file so you can edit it:
    ```
    $ cp .env.template .env
    ```

7. Launch the `vi` text editing application and specify required settings: 
    ```
    $ vi .env
    ``` 
   - Change the `DOMAIN` line so that after the `=` is the domain name you registered above. As an example: `DOMAIN=myserverodk.mooo.com.` Do not include `http://` or `https://` in the domain.
    - Change the `SYSADMIN_EMAIL` line so that after the `=` is your own email address. The Let's Encrypt service will use this address only to notify you if something is wrong with your security certificate. 

    - Leave the rest of the settings alone. Press `esc` then `:wq!` to save the changes and quit.

        <img src="./Images/env.png" width="600" height="250"/>
 
8. Let the system know that you want the latest version of the database:
    ```
    $ touch ./files/allow-postgres14-upgrade
    ```
    This is mostly useful for upgrades but is also currently necessary for fresh installs.
&nbsp;<br>

9. Bundle everything together into a server. This will take a long time and generate quite a lot of text output. 
    ```
    $ docker compose build
    ```
    When it finishes, you should see some "Successfully built" type text and get your input prompt back.
&nbsp;<br> 

10. Start the server software. The first time you start it, it will take a while to set itself up. 
    ```
    $ docker compose up -d
    ```
&nbsp;<br>

11. See whether ODK has finished loading.
    ```
    $ docker compose ps
    ```
    Under the `Status` column, for the `central-nginx-1` row, you will want to see text that reads Up or Up (healthy). If you see Up (health: starting), give it a few minutes. If you see some other text, something has gone wrong. 
&nbsp;<br>

12. Visit your domain name in a web browser. If it's not accessible yet, you should continue waiting. Once it is accessible, check that you get the Central website. 

## Logging Into Central
Now, you have to create an Administrator account so that you can log into Central. To do this: 
1. Ensure that you are in the central folder on your server. If you have not closed your console session from earlier, you should be fine. If you have just logged back into it: 
    ```
    $ cd central
    ```


2. Create a new account. Make sure to substitute the email address that you want to use for this account.
    ```
    $ docker compose exec service odk-cmd --email <YOUREMAIL@ADDRESSHERE>.com user-create
    ``` 
    Press Enter, and you will be asked for a password for this new account.
&nbsp;<br>
3. Make the new account an administrator. 
    ```
    $ docker compose exec service odk-cmd --email <YOUREMAIL@ADDRESSHERE.com> user-promote
    ``` 
   <img src="./Images/admin-login.png" width="600" height="250"/>

4. Log into the Central website. Go to your domain name and enter in your new credentials. Once you have one administrator account, you do not have to go through this process again for future accounts: you can log into the website with your new account, and directly create new users that way.


