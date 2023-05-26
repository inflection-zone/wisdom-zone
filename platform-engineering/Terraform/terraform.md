# Terraform Code to Setup AWS Infra

## Objective
* Setup AWS infrastructure using Terraform

## Overview of Terraform 
* HashiCorp Terraform is an infrastructure as code tool that lets you define both cloud and on-premises resources in human-readable configuration files.
* Terraform can manage low-level components like compute, storage, and networking resources, as well as high-level components like DNS entries and SaaS features. 
* As Terraform uses a simple syntax, it can provision infrastructure across multiple cloud and on-premises data centers, and can safely and efficiently re-provision infrastructure in response to configuration changes.
* The core Terraform workflow consists of three stages:
    - **Write**: You define resources, which may be across multiple cloud providers and services.
    - **Plan**: Terraform creates an execution plan describing the infrastructure it will create, update, or destroy based on the existing infrastructure and your configuration.
    - **Apply**: On approval, Terraform performs the proposed operations in the correct order, respecting any resource dependencies. For example, if you update the properties of a VPC and change the number of virtual machines in that VPC, Terraform will recreate the VPC before scaling the virtual machines.
* Terraform advantages:
    - **Manage any infrastructure**: It has thousands of providers to manage many different types of resources and services. 
    - **Track your infrastructure**: Terraform generates a plan and prompts you for your approval before modifying your infrastructure. It also keeps track of your real infrastructure in a state file, which acts as a source of truth for your environment.
    - **Automate changes**: You do not need to write step-by-step instructions to create resources as Terraform handles the underlying logic. Terraform builds a resource graph to determine resource dependencies and creates or modifies non-dependent resources in parallel. This allows Terraform to provision resources efficiently. 
    - **Standardize configurations**: Terraform supports reusable configuration components called `modules` that define configurable collections of infrastructure, saving time and encouraging best practices. 
    - **Collaborate**: Since your configuration is written in a file, you can commit it to a Version Control System (VCS) and use Terraform Cloud to efficiently manage Terraform workflows across teams. 

* For more information, please refer official [Terraform Documentation](https://developer.hashicorp.com/terraform/intro) and to get providers, go to [Terraform Registry](https://registry.terraform.io/?product_intent=terraform&utm_source=WEBSITE&utm_medium=WEB_IO&utm_offer=ARTICLE_PAGE&utm_content=DOCS)

## Installation
* To use Terraform you will need to install it. HashiCorp distributes Terraform as a [binary package](https://developer.hashicorp.com/terraform/downloads). You can also install Terraform using popular package managers. 
* Here are the steps to install Terraform on Windows using Chocolaty:
    1. Open `Windows Powershell` as administrator.
    2. Run command :
        ```
        choco install terraform
        ``` 
        This will install `Terraform Package` on your system.
    3. Once completed, verify the installation by running command: 
        ```
        terraform -version
        ```
        If you get version number of Terraform, that means you have installed it successfully.

## Setup Infrastructure
### Prerequisites: 
To create AWS infrastructure using terraform, one should have
1. An AWS account
2. AWS CLI installed and configured with IAM user credentials
3. Terraform installed

### Define Infrastructure
1. Create a folder at your desired location. Create a new file inside that folder and name it as `main.tf`. (**Note**: `.tf` is extention for terraform config file)
2. Open this folder with `VS Code`. Open `main.tf`. Start defining resources. 
3. First we define Terraform configurations as :
    ```
    terraform {
        required_providers {
            aws = {
            source  = "hashicorp/aws"
            version = "~> 4.16"
            }
        }

        required_version = ">= 1.2.0"
    }
    ```
4. Next we define provider using following lines of code:
    ```
    provider "aws" {
        region = "ap-south-1"
    }
    ```
5. In this tutorial, we will create following AWS resources: 
    1. VPC & subnets
    2. Internet Gateway, Route Tables and their associations
    3. Key-pair
    4. Security Group
    5. IAM role and instance profile
    6. EC2 Instance
    7. SSM Parameter

6. Lets see code snippets for all those resources one by one. First to create VPC and its subnets, use following lines of code:
    ```
    resource "aws_vpc" "deft-source-vpc" {
        cidr_block       = "10.0.0.0/16"
        instance_tenancy = "default"
        tags = {
            Name = "deft-source-vpc"
        }
    }

    resource "aws_subnet" "dev-public-subnet" {
        vpc_id                  = aws_vpc.deft-source-vpc.id
        cidr_block              = "10.0.1.0/24"
        availability_zone       = "ap-south-1a"
        map_public_ip_on_launch = true
        tags = {
            Name = "dev-public-subnet"
        }
    }

    resource "aws_subnet" "dev-private-subnet" {
        vpc_id            = aws_vpc.deft-source-vpc.id
        cidr_block        = "10.0.2.0/24"
        availability_zone = "ap-south-1b"
        tags = {
            Name = "dev-private-subnet"
        }
    }
    ``` 
7. Next to create internet gateway, route tables and their association with particular subnets, write code as: 
    ```
    resource "aws_internet_gateway" "deft-source-igw" {
        vpc_id = aws_vpc.deft-source-vpc.id

        tags = {
            Name = "deft-source-igw"
        }
        }

    resource "aws_route_table" "public-rt" {
        vpc_id = aws_vpc.deft-source-vpc.id
        route {
            cidr_block = "0.0.0.0/0"
            gateway_id = aws_internet_gateway.deft-source-igw.id
        }

        tags = {
            Name = "public-rt"
        }
        }

    resource "aws_route_table" "private-rt" {
        vpc_id = aws_vpc.deft-source-vpc.id
        route {
            cidr_block = "0.0.0.0/0"
            gateway_id = aws_internet_gateway.deft-source-igw.id
        }

        tags = {
            Name = "private-rt"
        }
        }

    resource "aws_route_table_association" "public-rt-association" {
        subnet_id      = aws_subnet.dev-public-subnet.id
        route_table_id = aws_route_table.public-rt.id
        }

    resource "aws_route_table_association" "private-rt-association" {
        subnet_id      = aws_subnet.dev-private-subnet.id
        route_table_id = aws_route_table.private-rt.id
        }
    ```
    Here, we have created two route tables i.e. public-rt & private-rt for two subnets and an internat gateway i.e. `dev-igw`.

8. To create key-pair, follow these steps: 
    1. Generate SSH key by running following command in terminal: 
        ```
        ssh-keygen -t rsa -f demokey -m PEM 
        ```
        This will output two files i.e `demokey` and `webkey.pub` inside your project directory. So `demokey` will be our private key and `webkey.pub` will be public key. 
    2. To create key pair we will use the generated public key file. Write code as:
        ```
        resource "aws_key_pair" "demokey" {
            key_name   = "demo-key"
            public_key = file("demokey.pub")
        }
        ```
9. Next we will create a security group for EC2 instance using code:
    ```
    resource "aws_security_group" "server-sg" {
        name        = "server-sg"
        description = "Allow All traffic"
        vpc_id      = aws_vpc.deft-source-vpc.id
        ingress {
            description = "All traffic from internet"
            from_port   = 0
            to_port     = 0
            protocol    = "-1"
            cidr_blocks = ["0.0.0.0/0"]
        }
        egress {
            from_port        = 0
            to_port          = 0
            protocol         = "-1"
            cidr_blocks      = ["0.0.0.0/0"]
            ipv6_cidr_blocks = ["::/0"]
        }

        tags = {
            Name = "server-sg"
        }
    }
    ``` 
    In this security group, we are allowing all traffic from internet. 

10. Our EC2 instance need permissions to access application images from ECR and also to access parameter store from SSM. For this purpose, we will create an `IAM Role` and attach appropriate policies to it. Then we will create an `IAM Instace Profile` using the role. 
    ```
    resource "aws_iam_role" "ec2-instance-role" {
        name = "ec2-instance-role"

        # Terraform's "jsonencode" function converts a
        # Terraform expression result to valid JSON syntax.
        assume_role_policy = jsonencode({
            Version = "2012-10-17"
            Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Sid    = ""
                Principal = {
                Service = "ec2.amazonaws.com"
                }
            },
            ]
        })
        tags = {
            Name = "ec2-instance-role"
        }
    }

    resource "aws_iam_role_policy_attachment" "ecr-policy-attach" {
        role       = aws_iam_role.ec2-instance-role.name
        policy_arn = "arn:aws:iam::<aws-account-id>:policy/ECR_FullAccess"
    }

    data "aws_iam_policy_document" "ssm-policy-document" {
        statement {
            effect = "Allow"
            actions = [
            "ssm:GetParameter",
            "ssm:GetParameters",
            "ssm:GetParametersByPath"
            ]
            resources = ["*"]
        }
    }

    resource "aws_iam_policy" "ssm-policy" {
        name        = "ssm-policy"
        description = "A ssm full access policy"
        policy      = data.aws_iam_policy_document.ssm-policy-document.json
    }

    resource "aws_iam_role_policy_attachment" "ssm-policy-attach" {
        role       = aws_iam_role.ec2-instance-role.name
        policy_arn = aws_iam_policy.ssm-policy.arn
    }

    resource "aws_iam_instance_profile" "dev-server-profile" {
        name = "dev-server-profile"
        role = aws_iam_role.ec2-instance-role.name
    }
    ```
    In above code, we have taken already created `ECR_FullAccess` policy and for SSM, we have created `Policy-document` and `Policy`. We have attached both the policies to role `ec2-instance-role`. At last we have created an instance profile resource using this role. 

11. We need to get `ubuntu` AMI which is available with AWS for our instance. To do this use following code:
    ```
    data "aws_ami" "ubuntu" {
        most_recent = true
        filter {
            name   = "name"
            values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
        }
        filter {
            name   = "virtualization-type"
            values = ["hvm"]
        }
        owners = ["amazon"]
    } 
    ```
12. Finally create EC2 instance as: 
    ```
    resource "aws_instance" "dev-server" {
        subnet_id            = aws_subnet.dev-public-subnet.id
        ami                  = data.aws_ami.ubuntu.id
        instance_type        = "t3.micro"
        key_name             = aws_key_pair.demokey.key_name
        security_groups      = [aws_security_group.server-sg.id]
        iam_instance_profile = aws_iam_instance_profile.dev-server-profile.name
        user_data            = file("init.sh")

        tags = {
            Name = "dev-server"
        }
    }
    ``` 
    Here, in the field of `user_data`, we have assign a file which contains userdata script for our instance. Here is the code inside `init.sh`:
    ```
    #!/bin/bash
    apt-get update
    apt-get install -y docker.io
    usermod -aG docker ubuntu
    chmod 666 /var/run/docker.sock
    apt-get install -y awscli 
    aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.ap-south-1.amazonaws.com 
    docker run -d --name app-container -p 3000:3000 -e VIRTUAL_HOST="$(aws ssm get-parameter --region "ap-south-1" --name "publicIP" --query Parameter.Value --output text)" -e BACKEND_API_URL="http://backend:3456" <aws-account-id>.dkr.ecr.ap-south-1.amazonaws.com/demo:latest
    docker run -d -p 80:80 --name nginx -v /var/run/docker.sock:/tmp/docker.sock -t jwilder/nginx-proxy 

    ``` 
    In this code, you may see that the value of a SSM parameter is given as env. variable while running docker conatiner. To store this parameter use following code: 
    ```
    resource "aws_ssm_parameter" "publicIp" {
        name  = "publicIp"
        type  = "String"
        value = aws_instance.dev-server.public_ip
    }

    ``` 

13. Once finished writing code, open terminal and run command to initialize the directory: 
    ```
    $ terraform init
    ```
    This will initialize a terraform configuration directory. Initializing a configuration directory downloads and installs the providers defined in the configuration, which in this case is the `aws` provider.
14. When project initialization is completed, Validate your configuration. The example configuration provided above is valid, so Terraform will return a success message: 
    ```
    $ terraform validate 
    Success! The configuration is valid.
    ```
15. Now, apply the configuration with following command :
    ```
    $ terraform apply
    ```
    Before it applies any changes, Terraform prints out the execution plan which describes the actions Terraform will take in order to change your infrastructure to match the configuration. Terraform will now pause and wait for your approval before proceeding. So type yes at the confirmation prompt to proceed. Executing the plan will take a few minutes since Terraform waits for the EC2 instance to become available.
16. We have now created infrastructure using Terraform. Visit the `EC2 console` and find new EC2 instance. Take its public IP and paste it in the browser. You may see the index page of frontend application.



