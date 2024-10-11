# Terraform EKS Deployment

### Prerequisites
1. AWS Account with an IAM User with administrative permissions.
2. Terraform installed.
3. Kubectl & Kubens installed.

---

## Using Terraform Modules to provision AWS Infrastructure

1. Create the Terraform project.
2. Download the [modules](https://github.com/sahilphule/terraform/tree/master) folder and copy it inside the above created terraform project.
3. Create *provider.tf* file inside above created terraform project.
4. Inside *provider.tf* file, define the following:
    - terraform
      - required_providers
    - provider
      - aws
5. The reference code is attached below.

```
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.64"
    }
  }
}

provider "aws" {
  region = local.aws_region
  # shared_config_files = ["~/.aws/config"]
  shared_credentials_files = ["~/.aws/credentials"]
}
```

6. The definition of *provider.tf* file is complete.
7. Create the *main.tf* file.
8. Inside *main.tf* file, call the following modules:
    - vpc
    - rds
    - eks
9. The reference code is attached below.

```
module "vpc" {
  source = "./modules/vpc"

  vpc-properties = local.vpc-properties
}

module "rds" {
  source = "./modules/rds"

  vpc-id              = local.vpc-id
  vpc-public-subnets  = local.vpc-public-subnets
  vpc-private-subnets = local.vpc-private-subnets
  database-properties = local.database-properties
  bastion-properties  = local.bastion-properties

  depends_on = [
    module.vpc
  ]
}

module "eks" {
  source = "./modules/eks"

  vpc-public-subnets  = local.vpc-public-subnets
  vpc-private-subnets = local.vpc-private-subnets

  eks-properties = local.eks-properties

  depends_on = [
    module.rds
  ]
}
```

10. *main.tf* file definition is completed.
11. Now we will create *locals.tf* file.
12. Define the following variables:
    - aws_region  
    - vpc-properties
        - availability-zones
        - vpc-cidr-block
        - vpc-subnet-count
        - vpc-public-subnet-cidr-blocks
        - vpc-private-subnet-cidr-blocks
        - vpc-tag-value
        - vpc-public-subnet-tag-value
        - vpc-private-subnet-tag-value
        - vpc-igw-tag-value
    - vpc-id
    - vpc-public-subnets
    - vpc-private-subnets
    - database-properties
        - identifier
        - allocated-storage
        - engine
        - engine-version
        - instance-class
        - skip-final-snapshot
        - publicly-accessible
        - db-username
        - db-password
        - db-sg-tag-value
        - db-tag-value
    - bastion-properties
        - count
        - instance-type
        - bastion-host-public-key
        - bastion-host-sg-tag-value
        - bastion-host-tag-value
    - eks-properties
        - eks-cluster-role-name
        - eks-cluster-name
        - eks-node-role-name
        - eks-node-group-name
        - eks-instance-types
        - eks-service-port
13. The reference code is attached below.

```
locals {

  aws_region = "ap-south-1"

  # vpc variables
  vpc-properties = {
    availability-zones = [
      "ap-south-1a",
      "ap-south-1b",
      "ap-south-1c"
    ]
    vpc-cidr-block = "10.0.0.0/16"
    vpc-subnet-count = {
      "public"  = 2,
      "private" = 2
    }
    vpc-public-subnet-cidr-blocks = [
      "10.0.1.0/24",
      "10.0.2.0/24",
      "10.0.3.0/24",
      "10.0.4.0/24"
    ]
    vpc-private-subnet-cidr-blocks = [
      "10.0.101.0/24",
      "10.0.102.0/24",
      "10.0.103.0/24",
      "10.0.104.0/24"
    ]

    vpc-tag-value                = ""
    vpc-public-subnet-tag-value  = ""
    vpc-private-subnet-tag-value = ""
    vpc-igw-tag-value            = ""
  }

  vpc-id              = module.vpc.vpc-id
  vpc-public-subnets  = module.vpc.vpc-public-subnets
  vpc-private-subnets = module.vpc.vpc-private-subnets

  # rds variables
  database-properties = {
    identifier          = ""
    allocated-storage   = 20
    engine              = "mysql"
    engine-version      = "8.0.35"
    instance-class      = "db.t3.micro"
    skip-final-snapshot = true
    publicly-accessible = false

    db-username = ""
    db-password = ""

    db-sg-tag-value = ""
    db-tag-value    = ""
  }

  bastion-properties = {
    count                   = 1
    instance-type           = "t2.micro"
    bastion-host-public-key = "~/.ssh/bastion-key.pub"

    bastion-host-sg-tag-value = ""
    bastion-host-tag-value    = ""
  }

  # eks variables
  eks-properties = {
    eks-cluster-role-name = ""
    eks-cluster-name      = ""
    eks-node-role-name    = ""
    eks-node-group-name   = ""
    eks-instance-types = [
      "t2.medium"
    ]
    eks-service-port = 
  }
}
```

14. The definition of *locals.tf* file is complete.
15. Now we will create *outputs.tf* file.
16. Define the following outputs:
    - DB_HOST
    - bastion-host-ip
17. The reference code is attached below.

```
output "DB_HOST" {
  description = "db host address"
  value       = module.rds.DB_HOST
}

output "bastion-host-ip" {
  description = "bastion host ip address"
  value       = module.rds.bastion-host-ip
}
```

18. The definition of *outputs.tf* file is complete.

---
---

## Provisioning the Infrastructure
Now we will provision the infrastructure by applying the above-created configuration files.

> Make sure AWS CLI is configured with appropriate AWS user credentials with enough permissions.

### Steps:
1. Open the PowerShell.
2. Change the directory to the above-created Terraform Project.
3. Run the `terraform init` to initialize the *terraform*.  
4. Run the `terraform fmt --recursive` to format the syntax of the files.
5. Run the `terraform validate` to validate the configuration files.
6. Run the `terraform plan` to plan the resources to be created.
7. Run the `terraform apply` and if prompted, type `yes` to provision the infrastructure.
8. Head to the AWS console, and verify the created resources.

---

<br>
<br>
<br>
<br>
<br>
<br>

## Screenshots of Provisioned Infrastructure

---

#### VPC Image
![vpc image](./images/vpc.png)

---

#### RDS Image
![rds image](./images/rds.png)

---

<br>
<br>
<br>
<br>
<br>
<br>
<br>

#### EKS Cluster Image
![eks cluster image](./images/cluster.png)

---

#### EKS Node Group Image
![eks nodegroup image](./images/node-group.png)

---

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

#### EKS Nodes Image
![eks nodes image](./images/nodes.png)

---

## Connect to EKS Cluster from powershell

1. Open new powershell window
2. Run the following command to configure local kubectl with eks cluster  
    `aws eks --region "region-name" update-kubeconfig --name "cluster-name"`  
    Substitute *region-name* and *cluster-name* with the above defined values.
3. Now apply the kubernetes manifest files of the application.
4. To list them all, run `kubectl get all`
5. If Load Balancer type Service is created then try accessing the External IP of that service in the browser.

---

## Connect to RDS database through Bastion Host
1. Open MySQL Workbench.
2. Click Add Connection.
3. Select connection method as **Standard TCP/IP over SSH**
4. In SSH Hostname, enter *bastion-host-ip:22* where bastion-host-ip is received from Terraform Output.
5. In SSH Username, enter *ec2-user*.
6. In SSH Key File, select *bastion-key.pem* file passed in above local.tf file.
7. In MySQL Hostname, enter *DB_HOST* where DB_HOST is received from Terraform Output.
8. In Password section, select *Store in Vault*, and enter the password passed in local.tf file.
9. Click *OK* and open the connection.
10. Now you can run mysql commands to access databases, and verify the successful connection of *eks-nodes*.

---

<br>
<br>
<br>

#### MySQL Workbench Image
![eks nodes image](./images/workbench.png)

---

## Destroy the provisioned infrastructure

1. Delete all the kubernetes resources.
2. To destroy infrastructure, run `terraform destroy` & if prompted, type `yes`.
3. Infrastructure will be destroyed

---