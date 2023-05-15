# Credential Management through Pulumi


## AWS Secret Manager

### Overview of AWS Secrets Manager
* AWS Secrets Manager helps you manage, retrieve, and rotate database credentials, application credentials, OAuth tokens, API keys, and other secrets throughout their lifecycles. Many AWS services that use secrets store them in Secrets Manager. 
* Secrets Manager helps you improve your security posture, because you no longer need hard-coded credentials in application source code. 
* Storing the credentials in Secrets Manager helps avoid possible compromise by anyone who can inspect your application or the components.
* You can replace hard-coded credentials with a runtime call to the Secrets Manager service to retrieve credentials dynamically when you need them. 

### Create and retrieve Secret using Pulumi code
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


## Hashicorp Vault 

### Overview of Hashicorp Vault
* HashiCorp Vault is an identity-based secrets and encryption management system. 
* It is designed to help organizations manage access to secrets and transmit them safely within an organization. 
* `Secrets` are defined as any form of sensitive credentials that need to be tightly controlled and monitored and can be used to unlock sensitive information. Secrets could be in the form of passwords, API keys, SSH keys, RSA tokens, or OTP.
* Vault validates and authorizes clients (users, machines, apps) before providing them access to secrets or stored sensitive data. 
<img src="./Images/vault1.png" width="600" />
     &nbsp;<br>

### Uses of Vault: 
1. Secret management:
    - Static Secrets
    - Dynamic Secrets
2. Identity-based access 
3. Data encryption 
4. Key Management
> **Note:** For information about vault and its use cases, please refer official documentation [here](https://developer.hashicorp.com/vault/docs).

### Installation Steps: 
* In this tutorial, we will install Hashicorp Vault on linux (Ubuntu). So the steps will be for linux OS only. If you are using different platform, please refer this [document](https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-install?in=vault%2Fgetting-started) 

* Steps:
    1. Add GPG for the package signing key.
    ```
    sudo apt update && sudo apt install gpg
    ```
    2. Add the HashiCorp GPG key.
    ```
    wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
    ```
    3. Verify the key's fingerprint. 
    ```
    gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint 
    ```
    4. Add the official HashiCorp Linux repository.
    ```
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list 
    ```
    5. Update and install.
    ```
    sudo apt update && sudo apt install vault 
    ```
### Working with Vault
* Now Vault is installed, so we will start server in development mode. For that run following command:
    ```
    vault server -dev
    ```
    We will get output as shown in below image. It will give you `VAULT_ADDR`, `Unseal Key` and `Root Token` for server.
    <img src="./Images/vault2.png" width="600" />
     &nbsp;<br>
* Now we need to set following environment variables:
    1. Vault Address:
    ```
    export VAULT_ADDR='http://127.0.0.1:8200'
    ```
    2. Vault Token:
    ```
    export VAULT_TOKEN="hvs.G1UmRzzOo6SC02Z0xxxxxxxx"
    ```
* Now we will see the status of server using following command:
    ```
    vault status
    ```
    It will give us details about server as:
    <img src="./Images/vault3.png" width="600" />
     &nbsp;<br>

* To list all vailable paths in secret engine, run following command:
    ```
    vault secrets list
    ```
    It will output all the paths availble by default in vault as
    <img src="./Images/vault4.png" width="600" />
     &nbsp;<br> 

> **Note:** Secrets engines are components which store, generate, or encrypt data. Secrets engines are enabled at a `path` in Vault. When a request comes to Vault, the router automatically routes anything with the route prefix to the secrets engine. To the user, secrets engines behave similar to a virtual filesystem, supporting operations like read, write, and delete. To know more about `Secrets Engine`, please refer [documentation](https://developer.hashicorp.com/vault/docs/secrets) 

* We can enable our own path in secret engine. To do so run command:
    ```
    vault secrets enable -path=YOUR_PATH_NAME_HERE kv
    ```
    In this command, `kv` is type of secret engine. It is abbreviation
of `key-value`. Please replace `YOUR_PATH_NAME_HERE` with the name of your path. It will give an message like `Success! Enabled the kv secrets engine at: dbsecrets/`. 
    To see whether the new path is added to the list, run command:
    ```
    vault secrets list
    ```
    You may see following output:
    <img src="./Images/vault5.png" width="600" />
     &nbsp;<br>

* Now we will store our secrets in secrets engine using our own path as:
    ```
    vault kv put dbsecrets/data username=dbuser
    ```
    You will see the message as `Success! Data written to: dbsecrets/data` 

* To read our secret please run following command:
    ```
    vault kv get dbsecrets/data 
    ```
    You may see all the secrets stored at path `dbsecrets/data`. 

* If you want to see the secret data in jason format, modify above command as:
    ```
    vault kv get -format=json dbsecrets/data
    ```
    You will get information about secrets in json format as:
    ```
    {
    "request_id": "5986ae41-a9e6-d2c3-2a81-bd45f4b17efd",
    "lease_id": "",
    "lease_duration": 2764800,
    "renewable": false,
    "data": {
        "username": "dbuser"
    },
    "warnings": null
    }
    ``` 
* To delete secrets from given path, you need to run command:
    ```
    vault kv delete dbsecrets/data 
    ```
    You will get output message like: `Success! Data deleted (if it existed) at: dbsecrets/data` 
    Now if we run read command again on the same path, you may see the message like: `No value found at dbsecrets/data` 
    <img src="./Images/vault5.png" width="600" />
     &nbsp;<br> 

### Access Vault through Pulumi
* First we need to login to server with our `Root Token`. This is token auth method. There are several auth methods supported by vault. To know more about auth, please refer [document](https://developer.hashicorp.com/vault/docs/concepts/auth).

* To login using root token, run following command: 
    ```
    vault login token:YOUR_ROOT_TOKEN
    ```
    If you forgot to copy token at the time of server start, you may generate new token using command:
    ```
    vault token create
    ```
    Then copy this token and paste in above command. You will be logged into vault-server. 
    To revoke unused root-tokens, run command:
    ```
    vault token revoke YOUR_UNUSED_TOKEN
    ```
    Please don't forget to replace `YOUR_ROOT_TOKEN` and `YOUR_UNUSED_TOKEN` with your appropriate token values. 

* To use one of paths of vault, we need to add a policy defining permissions to that particular path. So run command:
    ```
    vault policy write my-policy -  EOF
        path "secret/*" {
        capabilities = ["create","read", "update", "delete"]
        }
        EOF
    ```
    Here, we have enabled all the operations on path `secret/*`.

* Now we need to configure `Pulumi` with the vault-server credentials. Before that, we should setup new pulumi project using steps given in this [document](./Pulumi%20Document.md). Then run following commands in terminal:
    ```
    pulumi config set vaut:address VAULT_SERVER_ADDRESS
    ```
    ```
    pulumi config set vaut:token YOUR_TOKEN_HERE
    ```
    Here, we will replace `VAULT_SERVER_ADDRESS` with our server address i.e. `http://127.0.0.1:8200` and `YOUR_TOKEN_HERE` with our root token we just used for login to server.

* To use pulumi for storing & retrieving secrets from vault, we will use `@pulumi/vault` package. So we need to install it first using command:
    ```
    npm i @pulumi/vault
    ```

* Now replace code in `index.ts` file with our desired code. Following are code examples to store secrets to vault and retrieve them using pulumi-typescript:
    ```
    import * as pulumi from "@pulumi/pulumi";
    import * as aws from "@pulumi/aws";
    import * as vault from "@pulumi/vault";

    const dbSecret = new vault.generic.Secret("my-db-secret", {
         path: "secret/dbsecrets",
         dataJson: JSON.stringify({
             username: "dbuser",
             password: "password",
         }),
    });

    ```
    Using above code we can store database secrets like username and password to the vault at path `secret/dbsecrets`. Run command `pulumi up` to execute the code. You may check whether secrets are stored properly at given path by using command:
    ```
    vault kv get secret/dbsecrets
    ```  
* Now to retrieve stored secrets, use following code:
    ```
    const dbsecrets = vault.generic.getSecret({
        path: "secret/dbsecrets",
    });

    const dbusername = dbsecrets.then(secrets => secrets.data["username"]);
    const dbpassword = dbsecrets.then(secrets => secrets.data["password"]);

    ```
    Here we have stored retrieved values of username and password in constants `dbusername` and `dbpassword` so that we can use them while creating database instance like AWS RDS. 






