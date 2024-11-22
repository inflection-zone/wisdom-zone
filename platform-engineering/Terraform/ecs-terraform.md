# Terraform ECS Deployment

### Prerequisites
1. AWS Account with an IAM User with administrative permissions.
2. Terraform installed.

We will provision cloud infrastructure for deploying VPC, S3, RDS, ECR, & ECS Cluster using individual terraform modules.

---
---

## Terraform Modules

#### Create Terraform Project

---

## VPC Module
Let's start with the VPC module.
1. Create *vpc* folder.
2. Inside *vpc* folder create *main.tf* file.
3. Create resources for the following:  
    - aws_vpc
    - for public
      - aws_subnet
      - aws_internet_gateway
      - aws_route_table
      - aws_route
      - aws_route_table_association
    - for private
      - aws_subnet
      - aws_route_table
      - aws_route_table_association
      - aws_db_subnet_group
4. The reference code is attached below:

```
resource "aws_vpc" "vpc" {
  cidr_block           = var.vpc-cidr-block
  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_subnet" "vpc-public-subnet" {
  vpc_id                  = aws_vpc.vpc.id
  count                   = var.vpc-subnet-count.public
  cidr_block              = var.vpc-public-subnet-cidr-blocks[count.index]
  availability_zone       = var.availability-zones[count.index]
  map_public_ip_on_launch = true
}

resource "aws_subnet" "vpc-private-subnet" {
  vpc_id            = aws_vpc.vpc.id
  count             = var.vpc-subnet-count.private
  cidr_block        = var.vpc-private-subnet-cidr-blocks[count.index]
  availability_zone = var.availability-zones[count.index]
}

resource "aws_internet_gateway" "vpc-igw" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_route_table" "vpc-public-rtb" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_route" "default-route" {
  route_table_id         = aws_route_table.vpc-public-rtb.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.vpc-igw.id
}

resource "aws_route_table_association" "public-rtb-assoc" {
  route_table_id = aws_route_table.vpc-public-rtb.id
  count          = var.vpc-subnet-count.public
  subnet_id      = aws_subnet.vpc-public-subnet[count.index].id
}

resource "aws_route_table" "vpc-private-rtb" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_route_table_association" "private-rtb-assoc" {
  route_table_id = aws_route_table.vpc-private-rtb.id
  count          = var.vpc-subnet-count.private
  subnet_id      = aws_subnet.vpc-private-subnet[count.index].id
}

resource "aws_db_subnet_group" "vpc-db-subnet-group" {
  name        = "db subnet group"
  description = "db subnet group for rean"
  subnet_ids  = [for subnet in aws_subnet.vpc-private-subnet : subnet.id]
}
```

5. Now the main definition for VPC has been created.
6. Now we will create *variables.tf* file inside *vpc* folder for declaring variables.
7. Declare the following variables:
    - availability-zones
    - vpc-cidr-block
    - vpc-subnet-count
    - vpc-public-subnet-cidr-blocks
    - vpc-private-subnet-cidr-blocks
8. The reference code is attached below.

```
variable "availability-zones" {
  description = "region AZs"
  type        = list(string)
}

variable "vpc-cidr-block" {
  description = "CIDR block for VPC"
  type        = string
}

variable "vpc-subnet-count" {
  description = "Number of Subnets"
  type        = map(number)
}

variable "vpc-public-subnet-cidr-blocks" {
  description = "Available CIDR blocks for public subnets"
  type        = list(string)
}

variable "vpc-private-subnet-cidr-blocks" {
  description = "Available CIDR blocks for private subnets"
  type        = list(string)
}
```

9. We have completed declaring variables for the VPC module.
10. Now we will declare outputs for the VPC module.
11. Create *outputs.tf* file inside the same *vpc* folder.
12. Add the following output:
    - vpc-id
    - vpc-private-subnets
    - vpc-public-subnets
    - vpc-db-subnet-group-id
13. The reference code is attached below.

```
output "vpc-id" {
  value = aws_vpc.vpc.id
}

output "vpc-private-subnets" {
  value = aws_subnet.vpc-private-subnet
}

output "vpc-public-subnets" {
  value = aws_subnet.vpc-public-subnet
}

output "vpc-db-subnet-group-id" {
  value = aws_db_subnet_group.vpc-db-subnet-group.id
}
```

14. Now we have completed defining the **VPC Module**.

---
---

## S3 Module
We will use S3 to store and access .env files for ecs containers.
1. Create *s3* folder.
2. Inside *s3* folder, create *main.tf* file.
3. Define the following resources:
    - aws_s3_bucket
4. The reference code is attached below.

```
resource "aws_s3_bucket" "s3-bucket" {
  bucket        = var.s3-bucket-name
  force_destroy = true
}
```

5. We have completed defining *main.tf* file.
6. Now create *variables.tf* file.
7. Define the following variables:
    - s3-bucket-name
8. The reference code is attached below:

```
variable "s3-bucket-name" {
  description = "s3 bucket name"
  type        = string
}
```

9. *variables.tf* file has been declared.
10. Now create *output.tf* file.
11. Inside *output.tf* file, define the following outputs:
    - s3-bucket-id
12. The reference code is attached below.

```
output "s3-bucket-id" {
  description = "s3 bucket id"
  value       = aws_s3_bucket.s3-bucket.id
}
```

13. We have completed defining the **S3 Module**.

---
---

## RDS Module
For database storage, we will use MySQL RDS.  
1. Create *rds* folder.
2. Inside *rds* folder, create *main.tf* file.
3. Define the following resources:
    - aws_security_group
    - aws_db_instance
4. The reference code is provided below.

```
resource "aws_security_group" "db-sg" {
  name        = "db-sg"
  description = "db security group"
  vpc_id      = var.vpc-id
}

resource "aws_db_instance" "db" {
  allocated_storage      = var.database-properties.allocated-storage
  db_name                = var.database-properties.db-name
  engine                 = var.database-properties.engine
  engine_version         = var.database-properties.engine-version
  instance_class         = var.database-properties.instance-class
  username               = var.db-username
  password               = var.db-password
  db_subnet_group_name   = var.vpc-db-subnet-group-id
  vpc_security_group_ids = [aws_security_group.db-sg.id]
  publicly_accessible    = var.database-properties.publicly-accessible
  skip_final_snapshot    = var.database-properties.skip-final-snapshot
}
```

5. The definition of *main.tf* file is completed.
6. Now we will create *variables.tf* file.
7. Inside *variables.tf* define the following variables:
    - vpc-id
    - vpc-db-subnet-group-id
    - database-properties
    - db-username
    - db-password
8. The reference code is provided below.

```
variable "vpc-id" {
  description = "vpc id"
  type        = string
}

variable "vpc-db-subnet-group-id" {
  description = "db subnet group id"
  type        = string
}

variable "database-properties" {
  description = "database properties"
  type        = map(any)
}

variable "db-username" {
  description = "db username"
  type        = string
}

variable "db-password" {
  description = "db password"
  type        = string
}
```

9. Variables have been declared, now we will define the output.
10. Create *outputs.tf* file.
11. Inside the *outputs.tf* file, define the following output:
    - DB_HOST
12. Reference code has been provided below.

```
output "DB_HOST" {
  description = "rds db host address"
  value = aws_db_instance.db.address
}
```

13. Definition of **RDS Module** has been completed.

---
---

## ECR Module
Let's start with the ECR Module
1. Create *ecr* folder.
2. Inside *ecr* folder, create *main.tf* file.
3. In *main.tf* file, define the following resources:
    - aws_ecr_repository
4. The reference code is attached below.

```
resource "aws_ecr_repository" "ecr-repository" {
  name = var.ecr-repo-name
}
```

5. The definition of *main.tf* file is complete.
6. Now we will create *variables.tf* file and declare the following variables:
    - ecr-repo-name
7. The reference code is attached below.

```
variable "ecr-repo-name" {
  description = "ecr repository name"
  type        = string
}
```

8. The declaration of variables is completed.
9. Now we will create *outputs.tf* file and define the following output:
    - repository-url
10. The reference code is attached below.

```
output "repository-url" {
  description = "ecr repository url"
  value = aws_ecr_repository.ecr-repository.repository_url
}
```

11. The definition of *outputs.tf* file is complete.
12. We have completed creating the **ECR Module**.

---
---

## ECS Module
Let's start with the ECS Module
1. Create *ecs* folder.
2. Inside *ecs* folder create *data.tf* file.
3. In *data.tf* file, define the following data:
    - aws_iam_policy_document
4. The reference code is attached below.

```
data "aws_iam_policy_document" "assume-role-policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      identifiers = ["ecs-tasks.amazonaws.com"]
      type        = "Service"
    }
  }
}
```

5. Definition of *data.tf* file is completed.
6. Now we will define *main.tf* file.
7. Inside *ecs* folder create *main.tf* file.
8. In the *main.tf* file, define the following resources:
    - aws_ecs_cluster
    - aws_security_group for load balancer
    - aws_lb
    - aws_lb_target_group
    - aws_lb_listener
    - aws_iam_role for ecs-task-execution
    - aws_iam_role_policy_attachment
    - aws_ecs_task_definition
    - aws_security_group for service
    - aws_ecs_service
9. The reference Code is attached below.

```
resource "aws_ecs_cluster" "cluster" {
  name = var.cluster-name
}

resource "aws_security_group" "load-balancer-sg" {
  vpc_id = var.vpc-id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "application-load-balancer" {
  name               = var.application-load-balancer-name
  load_balancer_type = "application"
  security_groups    = [aws_security_group.load-balancer-sg.id]
  subnets = [
    for subnet in var.vpc-public-subnets : subnet.id
    # for subnet in var.vpc-private-subnets : subnet.id
  ]
}

resource "aws_lb_target_group" "target-group" {
  name        = var.target-group-name
  port        = var.container-port
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc-id
}

resource "aws_lb_listener" "listener" {
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.target-group.arn
  }

  load_balancer_arn = aws_lb.application-load-balancer.arn
  port              = "80"
  protocol          = "HTTP"
}

resource "aws_iam_role" "ecs-task-execution-role" {
  assume_role_policy = data.aws_iam_policy_document.assume-role-policy.json
  name               = var.ecs-task-execution-role-name
}

resource "aws_iam_role_policy_attachment" "ecs-task-execution-role-policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
  role       = aws_iam_role.ecs-task-execution-role.name
}

resource "aws_ecs_task_definition" "task" {
  family                   = var.task-family
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 512
  memory                   = 1024
  container_definitions    = <<DEFINITION
  [
    {
      "name": "${var.task-name}",
      "image": "${var.repo-url}",
      "cpu": 512,
      "memory": 1024,
      "essential": true,
      "portMappings": [
        {
          "containerPort": ${var.container-port},
          "hostPort": ${var.container-port}
        }
      ],
      "environment": [
        {
          "name": "S3_CONFIG_BUCKET",
          "value": "${var.s3-config-bucket}"
        },
        {
          "name": "S3_CONFIG_PATH",
          "value": "${var.s3-config-path}"
        }
      ]
    }
  ]
  DEFINITION
  execution_role_arn       = aws_iam_role.ecs-task-execution-role.arn
}

resource "aws_security_group" "service-security-group" {
  vpc_id = var.vpc-id
  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.load-balancer-sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_service" "service" {
  name            = var.service-name
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.task.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  load_balancer {
    container_name   = aws_ecs_task_definition.task.family
    container_port   = var.container-port
    target_group_arn = aws_lb_target_group.target-group.arn
  }

  network_configuration {
    subnets = [
      for subnet in var.vpc-public-subnets : subnet.id
      # for subnet in var.vpc-private-subnets : subnet.id
    ]

    assign_public_ip = true
    security_groups = [
      aws_security_group.service-security-group.id
    ]
  }
}
```

10. The *main.tf* file for ECS has been defined.
11. Now we will define variables.tf file.
12. Create *variables.tf* file inside *ecs* folder.
13. Define the following variables:
    - availability-zones
    - vpc-id
    - vpc-public-subnets
    - vpc-private-subnets
    - ecr-repo-url
    - repo-url
    - cluster-name
    - application-load-balancer-name
    - target-group-name
    - ecs-task-execution-role-name
    - task-family
    - task-name
    - container-name
    - container-port
    - s3-config-bucket
    - s3-config-path
    - service-name
14. The reference code is attached below.

```
variable "availability-zones" {
  description = "ap-south-1 AZs"
  type        = list(string)
}

variable "vpc-id" {
  description = "vpc id"
  type        = string
}

variable "vpc-public-subnets" {
  description = "vpc public subnets"
  type        = list(any)
}

# variable "vpc-private-subnets" {
#   description = "vpc private subnets"
#   type        = list(any)
# }

# variable "ecr-repo-url" {
#   description = "ecr repo url"
#   type        = string
# }

variable "repo-url" {
  description = "docker hub repo url"
  type        = string
}

variable "cluster-name" {
  description = "cluster name"
  type        = string
}

variable "application-load-balancer-name" {
  description = "application load balancer name"
  type        = string
}

variable "target-group-name" {
  description = "target group name"
  type        = string
}

variable "ecs-task-execution-role-name" {
  description = "ecs task execution role name"
  type        = string
}

variable "task-family" {
  description = "ecs task family"
  type        = string
}

variable "task-name" {
  description = "task name"
  type        = string
}

variable "container-name" {
  description = "task name"
  type        = string
}

variable "container-port" {
  description = "container port"
  type        = string
}

variable "s3-config-bucket" {
  description = ".env bucket name"
  type        = string
}

variable "s3-config-path" {
  description = ".env file path in s3 bucket"
  type        = string
}

variable "service-name" {
  description = "service name"
  type        = string
}
```

15. We have completed defining the **ECS Module**.

---
---

## Using defined modules

Now we will use the above-defined modules to create the configuration files.  
Inside the above-created Terraform project, 
1. Create *provider.tf* file.
2. Inside *provider.tf*, define the following:
    - terraform
      - required_providers
    - provider
      - docker
      - aws
3. The reference code is attached below.

```
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.20.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.64"
    }
  }
}

provider "docker" {}

provider "aws" {
  region = var.aws_region
  # shared_config_files = ["~/.aws/config"]
  shared_credentials_files = ["~/.aws/credentials"]
}
```

4. The definition of *provider.tf* file is complete.
5. Now we will create *variables.tf* file.
6. Inside the *variables.tf* file, we will declare the following variable:
    - aws_region
7. The reference code is attached below.

```
variable "aws_region" {
  description = "AWS cloud formation region"
  type        = string
}
```

8. The definition of *variables.tf* is complete.
9. Create a *terraform.tfvars* file and define the following variables:
    - aws_region
10. The reference code is attached below.

```
aws_region = "ap-south-1"
```

11. The definition of *terraform.tfvars* is complete.
12. Create the *main.tf* file.
13. Inside *main.tf* file, call the following modules:
    - vpc
    - s3
    - rds
    - ecs
14. Also define the following s3 resource for uploading local .env file:
    - aws_s3_object
15. The reference code is attached below.

```
module "vpc" {
  source                         = "./modules/vpc"
  vpc-cidr-block                 = local.vpc-cidr-block
  vpc-subnet-count               = local.vpc-subnet-count
  vpc-public-subnet-cidr-blocks  = local.vpc-public-subnet-cidr-blocks
  vpc-private-subnet-cidr-blocks = local.vpc-private-subnet-cidr-blocks
  availability-zones             = local.availability-zones
}

# module "ecr-repo" {
#   source        = "./modules/ecr"
#   ecr-repo-name = local.ecr-repo-name
# }

module "s3" {
  source = "./modules/s3"

  s3-bucket-name = local.s3-bucket-name
}

resource "aws_s3_object" "env-file" {
  bucket = local.s3-bucket-id
  key    = "awards/env.config"
  source = "../compose/.env"
  etag   = filemd5("../compose/.env")
}

module "rds" {
  source = "./modules/rds"

  vpc-id                 = local.vpc-id
  vpc-db-subnet-group-id = local.vpc-db-subnet-group-id
  database-properties    = local.database-properties
  db-username            = local.db-username
  db-password            = local.db-password
}

module "ecs" {
  source = "./modules/ecs"

  vpc-id = local.vpc-id
  # vpc-private-subnets = local.vpc-private-subnets
  vpc-public-subnets = local.vpc-public-subnets
  availability-zones = local.availability-zones

  # ecr-repo-url = module.ecr-repo.repository-url
  repo-url = local.repo-url

  application-load-balancer-name = local.application-load-balancer-name
  target-group-name              = local.target-group-name
  cluster-name                   = local.cluster-name
  ecs-task-execution-role-name   = local.ecs-task-execution-role-name
  task-family                    = local.task-family
  task-name                      = local.task-name
  container-name                 = local.container-name
  container-port                 = local.container-port
  s3-config-bucket               = local.s3-config-bucket
  s3-config-path                 = local.s3-config-path
  service-name                   = local.service-name
}
```

16. *main.tf* file definition is completed.
17. Now we will create *locals.tf* file.
18. Define the following variables:
    - availability-zones
    - vpc-cidr-block
    - vpc-subnet-count
    - vpc-public-subnet-cidr-blocks
    - vpc-private-subnet-cidr-blocks
    - vpc-id
    - vpc-public-subnets
    - vpc-db-subnet-group-id
    - repo-url
    - s3-bucket-id
    - s3-bucket-name
    - database-properties
    - db-username
    - db-password
    - cluster-name
    - application-load-balancer-name
    - target-group-name
    - ecs-task-execution-role-name
    - task-family
    - task-name
    - container-name
    - container-port
    - s3-config-bucket
    - s3-config-path
    - service-name
19. The reference code is attached below.

```
locals {

  availability-zones = ["ap-south-1a", "ap-south-1b", "ap-south-1c"]

  # vpc variables
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

  vpc-id = module.vpc.vpc-id
  # vpc-private-subnets = module.vpc.vpc-private-subnets
  vpc-public-subnets     = module.vpc.vpc-public-subnets
  vpc-db-subnet-group-id = module.vpc.vpc-db-subnet-group-id

  # # ecr variables
  # ecr-repo-name = "awards"
  # ecs-repo-url  = module.ecr-repo.repository-url
  repo-url = "sahilphule0710/awards"

  # s3 variables
  s3-bucket-id   = module.s3.s3-bucket-id
  s3-bucket-name = "reancare-dev-bucket"

  # rds variables
  database-properties = {
    allocated-storage   = 20
    engine              = "mysql"
    engine-version      = "8.0.35"
    instance-class      = "db.t3.micro"
    db-name             = "awardsdb"
    skip-final-snapshot = true
    publicly-accessible = false
  }
  db-username = "admin"
  db-password = "password"

  # ecs variables
  cluster-name                   = "reancare-dev-cluster"
  application-load-balancer-name = "reancare-dev-alb"
  target-group-name              = "reancare-dev-alb-tg"
  ecs-task-execution-role-name   = "reancare-dev-task-execution-role"
  task-family                    = "reancare-dev-awards-task"
  task-name                      = "reancare-dev-awards-task"
  container-name                 = "awards-app-service"
  container-port                 = 1111
  s3-config-bucket               = "reancare-dev-bucket"
  s3-config-path                 = "awards"
  service-name                   = "reancare-dev-awards-service"
}
```

20. The definition of *locals.tf* file is complete.
21. Now we will create *outputs.tf* file.
22. Define the following outputs:
    - DB_HOST
23. The reference code is attached below.

```
output "DB_HOST" {
  description = "db host address"
  value       = module.rds.DB_HOST
}
```

24. The definition of *outputs.tf* file is complete.

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
9. Then,
    - Head towards EC2 dashboard.
    - Select *Load Balancers*, and select the created load balancer
    - Copy the DNS address.
    - Paste the address in the browser to access the application.

---
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
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

## Screenshots of provisioned infrastructure
---

#### VPC Image
![vpc image](./images/vpc.png)

---

#### S3 Image
![s3 image](./images/s3.png)

---

<br>
<br>

#### RDS Image
![rds image](./images/rds.png)

---

#### ECS Image
![ecs image](./images/ecs.png)

---

<br>
<br>
<br>
<br>

#### ALB Image
![alb image](./images/alb.png)

---