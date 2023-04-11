# Pulumi code to launch AWS EC2 instance with script 
* In this tutorial, we will write a pulumi code for an EC2 instance with userdata script. 
* The launched instance will have docker and docker compose installed on it and also able to clone git repository and run the containers. 
* Let's start the tutorial step by step:
    1. Create a new folder and start pulumi project in that repository using following commands on your terminal. Here we will select aws-region: 'ap-south-1'
    `$ mkdir pulumi-demo && cd pulumi-demo`
    `$ pulumi new aws-typescript` 
&nbsp;<br>
    2. After completing project setup, open the folder using Visual Studio code. Open file 'index.ts'. Clear all the unnecessary lines from code. First we have to import necessary modules as- 
    `import * as pulumi from "@pulumi/pulumi";`
    `import * as aws from "@pulumi/aws";` 
&nbsp;<br>
    3. Then we will create a VPC using following code.

    ```
        const main = new aws.ec2.Vpc("my-vpc", {
        cidrBlock: "10.0.0.0/16",
        instanceTenancy: "default",
        tags: {
            Name: "my-vpc",
         },
        });
    ```
    &nbsp;<br>
    
    4. Next we have to create two subnets in two different availablity zones. 
    ```
        const publicSubnet = new aws.ec2.Subnet("my-public-subnet", {
            vpcId: main.id,
            cidrBlock: "10.0.1.0/24",
            availabilityZone: "ap-south-1c",
            mapPublicIpOnLaunch: true,
            tags: {
                Name: "my-public-subnet",
             },
        }); 
        const privateSubnet = new aws.ec2.Subnet("my-private-subnet", {
            vpcId: main.id,
            cidrBlock: "10.0.2.0/24",
            availabilityZone: "ap-south-1b",
            tags: {
                 Name: "my-private-subnet",
            },
        }); 

    ```
    &nbsp;<br>
    
    5. Now we will configure internet gateway to connect vpc to outside network.
    ```
        const gw = new aws.ec2.InternetGateway("dev-igw", {
            vpcId: main.id,
            tags: {
                 Name: "dev-igw",
            },
        });
    ``` 
    &nbsp;<br>

    6. Next we will create two route tables and then we will associate two subnets to them.
    ```
        const publicRt = new aws.ec2.RouteTable("public-rt", 
         {  vpcId: main.id,
            routes: [
                {
                    cidrBlock: "0.0.0.0/0",
                    gatewayId: gw.id,
                },
        
            ],
            tags: {
                Name: "public-rt",
            },
        }); 

          const privateRt = new aws.ec2.RouteTable("private-rt", 
         {  vpcId: main.id,
            routes: [
                {
                    cidrBlock: "0.0.0.0/0",
                    gatewayId: gw.id,
                },
        
            ],
            tags: {
                Name: "private-rt",
            },
        });

    ```
    &nbsp;<br>

    7. Subnet association:
    ```
        const publicRtAssociation = new aws.ec2.RouteTableAssociation("public-rt-association", {
            subnetId: publicSubnet.id,
            routeTableId: publicRt.id,
        }); 

        const privateRtAssociation = new aws.ec2.RouteTableAssociation("private-rt-association", {
            subnetId: privateSubnet.id,
            routeTableId: privateRt.id,
        });

    ```
    &nbsp;<br>

    8. Then we will create a security group which will allow SSH, HTTP and HTTPS traffic.
    ```
        const devSG = new aws.ec2.SecurityGroup("dev-sg", {
        description: "EC2 Security Group",
        vpcId: main.id,
        ingress: [ 
            { description: "Allow HTTPS", fromPort: 443, toPort: 443, protocol: "tcp", cidrBlocks: ["0.0.0.0/0"]},
            { description: "Allow HTTP", fromPort: 80, toPort: 80, protocol: "tcp", cidrBlocks: ["0.0.0.0/0"]},
            { description: "Allow SSH", fromPort: 22, toPort: 22, protocol: "tcp", cidrBlocks: ["0.0.0.0/0"] } 
             ],
        egress: [
            { fromPort: 0, toPort: 0, protocol: "-1", cidrBlocks: ["0.0.0.0/0"], ipv6CidrBlocks: ["::/0"] }
            ],
        tags: {
             Name: "dev-sg",
            },
        }); 

    ```
    &nbsp;<br> 

    9. Here we will write userdata script to install docker & docker compose and also to clone a git repository to run containers using docker compose.
    ```
        const userData= 
        `#!/bin/bash
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
        mkdir Project && cd Project
        sudo git clone https://<github_username>:<github_PAT>@github.com/<github_username>/<repository name>.git 
        cd docker-compose-nginx
        docker compose up --build -d`;
    ``` 
    &nbsp;<br> 

    10. Now we will generate ssh key and add it to our pulumi code. So open terminal in same project folder and run following commands.
    &nbsp;<br>
        `$ ssh-keygen -t rsa -f rsa -m PEM` 
    &nbsp;<br>
    This will output two files 'rsa' and 'rsa.pub'. rsa is our private key and 'rsa.pub' is our public key. Then run following commands.

        `$ cat rsa.pub | pulumi config set publickey --`

        `$ car rsa | pulumi config set privatekey --secret --`

     &nbsp;<br> 

    11. Then we will write code to add public and private key.
    ```
        let keyName: pulumi.Input<string> | undefined = config.get("keyName");
        const publicKey = config.get("publicKey");

        const privateKey = config.requireSecret("privateKey").apply(key => {
            if (key.startsWith("-----BEGIN RSA PRIVATE KEY-----")) {
                return key;
            } else {
                return Buffer.from(key, "base64").toString("ascii");
            }
        }); 

        if (!keyName) {
            if (!publicKey) {
                throw new Error("must provide one of `keyName` or `publicKey`");
            }
            const key = new aws.ec2.KeyPair("key", { publicKey });
            keyName = key.keyName;
        }

    ```
    &nbsp;<br> 

    12. Finally write code to create EC2 instance. 
    ```
        const server = new aws.ec2.Instance("web-server", {
            instanceType: "t2.micro",
            vpcSecurityGroupIds: [ devSG.id ], // reference the security group resource above
            ami: "ami-02eb7a4783e7e9317",
            subnetId: publicSubnet.id,
            keyName: keyName,
            userData: userData,
        }); 
    ```
    &nbsp;<br> 

    13. Now open terminal and run command `pulumi update`. You may see the list of resources to be created. Then select yes when asked whether to create these resources. Finally you may see that your resources are creating. 

    14. You may login to your AWS console to verify the created resources. You may also connect to your EC2 instance to check running application containers. For that you have to open mobaxterm (or putty) from your system. Copy the public IP of instance and paste it to login from mobaxterm. Then write username "ubuntu". Go to advanced ssh settings. Here add your private key (i.e. rsa) file located on your system. And you will be logged into instance.

    




    
 




    
 
