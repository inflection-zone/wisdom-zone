# Pulumi code to create AWS infra for dev env

* Create new folder and initiate new pulumi project in it. Run following commands in your terminal.
    `$ mkdir pulumi-dev && cd pulumi-dev`
    `$ pulumi new aws-typescript` 

* Open folder in Visual Studio Code. Start editing index.ts file as given below in this document.

* First step is to import necessary modules. For that write following lines:
    ```
        import * as pulumi from "@pulumi/pulumi";
        import * as aws from "@pulumi/aws";
    ```
&nbsp;<br>

* Then we will write code to create a VPC. For that we will use CIDR block: 10.0.0.0/16. Line of code are as following:
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

* Then we will create subnets. We will have two subnets i.e. public and private. We will launch our EC2 instance in public subnet and have our RDS in private subnet. We will choose two differnt availability zones for these two subnets. The CIDR block for public subnet will be "10.0.0.0/24" & for private subnet it will be "10.0.1.0/24". 
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

* The next task is to create Internet Gateway. Write following code for it.
    ```
        const gw = new aws.ec2.InternetGateway("dev-igw", {
            vpcId: main.id,
            tags: {
                 Name: "dev-igw",
            },
        });
    ``` 
&nbsp;<br> 

* Next we need to create two route tables & their association to subnets. We will create "public-rt" and "private-rt" for public & private subnets accordingly. 

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

* For subnet association refer following code.
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

* Then we will create a security group for our EC2 instance. We will open these port numbers: 22 (SSH), 80 (HTTP), 3000 (frontend service). 
     ```
        const devSG = new aws.ec2.SecurityGroup("dev-sg", {
        description: "EC2 Security Group",
        vpcId: main.id,
        ingress: [ 
            { description: "Allow traffic to frontend-app", fromPort: 3000, toPort: 3000, protocol: "tcp", cidrBlocks: ["0.0.0.0/0"]},
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

