# Pulumi Code to Use AWS Secrets Manager

## Overview of AWS Secrets Manager
* AWS Secrets Manager helps you manage, retrieve, and rotate database credentials, application credentials, OAuth tokens, API keys, and other secrets throughout their lifecycles. Many AWS services that use secrets store them in Secrets Manager. 
* Secrets Manager helps you improve your security posture, because you no longer need hard-coded credentials in application source code. 
* Storing the credentials in Secrets Manager helps avoid possible compromise by anyone who can inspect your application or the components.
* You can replace hard-coded credentials with a runtime call to the Secrets Manager service to retrieve credentials dynamically when you need them. 

## Create and retrieve Secret using Pulumi code
* In this tutorial, we will write a simple pulumi code to understand how to create a secret in AWS Secrets Manager and how to retrieve it. 
* To create new pulumi project, you need to follow steps given in `Sample-Example-1` [here](./Pulumi%20Document.md).
* Let's create Pulumi code with following steps: 
1. Code to create a VPC:
```
    const main = new aws.ec2.Vpc("dev-vpc", {
        cidrBlock: "10.0.0.0/16",
        instanceTenancy: "default",
        tags: {
            Name: "dev-vpc",
        },
    });
```
2. Subnets: We will create two subnets in two different availability zones.
```
    const publicSubnet = new aws.ec2.Subnet("dev-public-subnet", {
        vpcId: main.id,
        cidrBlock: "10.0.1.0/24",
        availabilityZone: "ap-south-1c",
        mapPublicIpOnLaunch: true,
        tags: {
            Name: "dev-public-subnet",
        },
    });

    const privateSubnet = new aws.ec2.Subnet("dev-private-subnet", {
        vpcId: main.id,
        cidrBlock: "10.0.2.0/24",
        availabilityZone: "ap-south-1b",
        tags: {
            Name: "dev-private-subnet",
        },
    });
```
3. Internet Gateway: 
```
    const gw = new aws.ec2.InternetGateway("dev-igw", {
        vpcId: main.id,
        tags: {
            Name: "dev-igw",
        },
    });
```
4. Route Tables and their subnet associations: 
```
    const publicRt = new aws.ec2.RouteTable("dev-public-rt", {
        vpcId: main.id,
        routes: [
            {
                cidrBlock: "0.0.0.0/0",
                gatewayId: gw.id,
            },     
        ],
        tags: {
            Name: "dev-public-rt",
        },
    });

    const privateRt = new aws.ec2.RouteTable("dev-private-rt", {
        vpcId: main.id,
        routes: [
            {
                cidrBlock: "0.0.0.0/0",
                gatewayId: gw.id,
            }
        ],
        tags: {
            Name: "dev-private-rt",
        },
    }); 

    const publicRtAssociation = new aws.ec2.RouteTableAssociation("public-rt-association", {
        subnetId: publicSubnet.id,
        routeTableId: publicRt.id,
    }); 

    const privateRtAssociation = new aws.ec2.RouteTableAssociation("private-rt-association", {
        subnetId: privateSubnet.id,
        routeTableId: privateRt.id,
    });
```
5. EC2 Security Group: 
```
    const devSG = new aws.ec2.SecurityGroup("dev-sg", {
        description: "EC2 Security Group",
        vpcId: main.id,
        ingress: [{
            description: "Allow HTTPS",
            fromPort: 443,
            toPort: 443,
            protocol: "tcp",
            cidrBlocks: ["0.0.0.0/0"],
        },
        {
            description: "Allow HTTP",
            fromPort: 80,
            toPort: 80,
            protocol: "tcp",
            cidrBlocks: ["0.0.0.0/0"],
        },
        {
            description: "Allow SSH",
            fromPort: 22,
            toPort: 22,
            protocol: "tcp",
            cidrBlocks: ["0.0.0.0/0"],
        }],

        egress: [{
            fromPort: 0,
            toPort: 0,
            protocol: "-1",
            cidrBlocks: ["0.0.0.0/0"],
            ipv6CidrBlocks: ["::/0"],
        }],
        tags: {
            Name: "dev-sg",
        },
    });
``` 

6. Now we will generate ssh key and add it to our pulumi code. So open terminal in same project folder and run following commands.
    ```
        $ ssh-keygen -t rsa -f rsa -m PEM
    ``` 
    This will output two files `rsa` and `rsa.pub`. rsa is our private key and 'rsa.pub' is our public key. Then run following commands.
    ```
        $ cat rsa.pub | pulumi config set publickey --

        $ cat rsa | pulumi config set privatekey --secret --
    ```
7. Then we will write code to add public and private key
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

8. Role to create and access secrets in secrets manager:
```
    const role = new aws.iam.Role("secret-manager-role", {
        assumeRolePolicy: JSON.stringify({
            Version: "2012-10-17",
            Statement: [{
                Action: "sts:AssumeRole",
                Principal: {
                    Service: "ec2.amazonaws.com",
                },
                Effect: "Allow",
                Sid: "",
            }],
        }),
    });

    new aws.iam.RolePolicyAttachment("secret-manager-policy-attachment", {
        policyArn: "arn:aws:iam::aws:policy/SecretsManagerReadWrite",
        role: role.name,
    });

    const instanceProfile = new aws.iam.InstanceProfile("myInstanceProfile", {
        name: "myProfile",
        role: role.name,
    });
```

9. Code to get AMI: 
```
    const ubuntu = aws.ec2.getAmi({
        mostRecent: true,
        filters: [
            {
                name: "name",
                values: ["ubuntu*-20.04-amd64-*"],
            },
            {
                name: "virtualization-type",
                values: ["hvm"],
            },
        ],
        owners: ["amazon"],
    });
```

10. Userdata Script: 
```
    const userData= 
    `#!/bin/bash
    apt-get update
    apt-get install -y docker.io
    usermod -aG docker ubuntu
    chmod 666 /var/run/docker.sock

    apt-get install -y awscli 

    docker run -d -p 3000:3000 -e VIRTUAL_HOST="$(aws secretsmanager get-secret-value --secret-id MySecret123 --region ap-south-1 --query SecretString --output text)"  priyankainflectionzone/frontend-app:3.0

    docker run -d -p 80:80 -v /var/run/docker.sock:/tmp/docker.sock -t jwilder/nginx-proxy `;
```

11. Code for EC2 instance:
```
    const server = new aws.ec2.Instance("dev-server", {
        instanceType: "t3.micro",
        vpcSecurityGroupIds: [ devSG.id ], 
        ami: ubuntu.then(ubuntu => ubuntu.id),
        subnetId: publicSubnet.id,
        keyName: keyName,
        iamInstanceProfile: instanceProfile.name,
        userData: userData,
        tags: {
                Name: "dev-server",
            },
    });
```

12. Code to create a secret and secretVersion:
```
    const publicIp = new aws.secretsmanager.Secret("myseversecret1", {
        name: "MySecret123",
        description: "A secret containing sensitive information.",
    });

    const secretVersion = new aws.secretsmanager.SecretVersion("SecretVersion", {
        secretId: publicIp.id,
        secretString: server.publicIp,
    });

```

* Now to test your application, login to your AWS account, Take public IP of EC2 instance and paste into browser. You will see the index page of your application.

* You may also inspect your containers. For that please follow the steps:
1. Take public Ip of instance. Open `Mobaxterm` app on your system. 
2. Select `Session`. On the next page, select `SSH`. 
3. Paste public IP of instance in `Remote Host` field. Specify user `ubuntu`. Then go to `Advanced SSH Settings`. Browse for private key used while launching the instance. And select `OK`
4. You are now logged into your instance. Run following command to see running containers:
    ```
        $ docker ps
    ``` 
5. Now to see whether you application container has retrieved secret value or not please run following command:
    ```
        $ docker exec -it <app-container-id/name> /bin/sh
    ```
6. You will be on bash terminal of your container. Now run following command to see environment variables: 
    ```
        # env
    ```
Here you may see the environment variable we passed while running container to which retrieved value of secret is assigned.