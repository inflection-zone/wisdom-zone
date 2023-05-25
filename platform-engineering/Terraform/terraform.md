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

