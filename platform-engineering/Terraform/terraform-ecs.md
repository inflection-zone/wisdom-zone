# Terraform to Setup AWS Infra for ECS Cluster

## Objective
* Setup AWS infrastructure for ECS cluster using Terraform.

## Prerequisites 
To create AWS infrastructure using terraform, one should have
1. An AWS account
2. AWS CLI installed and configured with IAM user credentials
3. Terraform installed. (If want to install Terraform please refer installation steps from this [document](./terraform-ec2.md))

## Define Infrastructure
1. Create a folder at your desired location. Create a new file inside that folder and name it as `main.tf`.
2. Open this folder with `VS Code` or any other code editor. Open `main.tf`. Start defining resources.
3. In this tutorial, we will create following AWS resources: 
    1. VPC & subnets
    2. Internet Gateway, Route Tables and their associations
    3. Service-discovery namespace
    4. Cloudwatch log group
    5. ECS cluster
    6. Application load balancer, target group, listener and security group for load balancer
    7. Security groups for services and RDS database instance 
    8. Subnet group for database and RDS instance for MySQL database
    9. Task Execution IAM role with various IAM policies attached
    10. Task definition for backend service, service-discovery service resource for backend and backend service
    11. Task definition for frontend service, service-discovery service resource for frontend and frontend service 
    12. WAF Web-ACL and Web-ACL association with load balancer 

4. Let's start with code. First define terraform configurations as:
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
5. Now define provider. In this case it is `aws`.
    ```
    provider "aws" {
        region = "ap-south-1"
    }
    ```
6. Now start defining infrastructure. First write code for VPC and its subnets:
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
        map_public_ip_on_launch = true

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

8. Next, create http-namespace for service discovery as:
    ```
    resource "aws_service_discovery_http_namespace" "stagging-namespace" {
        name        = "stagging-namespace.local"
        description = "stagging-namespace"
    }
    ```
9. Now we will define cloudwatch log-group for ECS cluster:
    ```
    resource "aws_cloudwatch_log_group" "ecs-cluster-logs" {
        name = "ecs-cluster-logs"
        tags = {
            Environment = "stagging"
        }
    }
    ``` 
10. Next we need to create ECS Cluster. We will name it as `Demo-Cluster`
    ```
    resource "aws_ecs_cluster" "demo" {
        name = "demo-cluster"
        setting {
            name  = "containerInsights"
            value = "enabled"
        }
        configuration {
            execute_command_configuration {
            logging = "OVERRIDE"
            log_configuration {
                cloud_watch_encryption_enabled = true
                cloud_watch_log_group_name     = aws_cloudwatch_log_group.ecs-cluster-logs.name
            }
            }
        }
        service_connect_defaults {
            namespace = aws_service_discovery_http_namespace.stagging-namespace.arn
        }
    }
    ```
11. Now we will define load balancer and its supporting resources like target group, listener, security group for load balancer.
    ```
    resource "aws_security_group" "alb-security-group" {
        name        = "alb-sg"
        description = "Allow HTTP inbound traffic"
        vpc_id      = aws_vpc.deft-source-vpc.id
        ingress {
            description = "HTTP from internet"
            from_port   = 80
            to_port     = 80
            protocol    = "tcp"
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
            Name = "alb-sg"
        }
    }
    ```
    ```
    resource "aws_lb" "ecs-lb" {
        name               = "ecs-lb"
        internal           = false
        load_balancer_type = "application"
        security_groups    = [aws_security_group.alb-security-group.id]
        subnets            = [aws_subnet.dev-public-subnet.id, aws_subnet.dev-private-subnet.id]
    }
    ```
    ```
    resource "aws_lb_target_group" "ecs-lb-target-group" {
        name        = "ecs-lb-target-group"
        port        = 3000
        protocol    = "HTTP"
        target_type = "ip"
        vpc_id      = aws_vpc.deft-source-vpc.id
        health_check {
            healthy_threshold   = 5
            interval            = 50
            path                = "/"
            matcher             = "200"
            protocol            = "HTTP"
            port                = "3000"
            timeout             = 30
            unhealthy_threshold = 5
        }
    }
    ```
    ```
    resource "aws_lb_listener" "front_end" {
        load_balancer_arn = aws_lb.ecs-lb.arn
        port              = "80"
        protocol          = "HTTP"

        default_action {
            type             = "forward"
            target_group_arn = aws_lb_target_group.ecs-lb-target-group.arn
        }
    } 
    ```
12. Next, we will define security groups for services and RDS instance as:
    ```
    resource "aws_security_group" "frontend-security-group" {
        name        = "frontend-sg"
        description = "Allow ALB traffic"
        vpc_id      = aws_vpc.deft-source-vpc.id
        ingress {
            description     = "Traffic from ALB"
            from_port       = 0
            to_port         = 0
            protocol        = "-1"
            security_groups = [aws_security_group.alb-security-group.id]
        }
        egress {
            from_port        = 0
            to_port          = 0
            protocol         = "-1"
            cidr_blocks      = ["0.0.0.0/0"]
            ipv6_cidr_blocks = ["::/0"]
        }
        tags = {
            Name = "frontend-sg"
        }
    }
    ```
    ```
    resource "aws_security_group" "backend-security-group" {
        name        = "backend-sg"
        description = "Allow frontend traffic"
        vpc_id      = aws_vpc.deft-source-vpc.id
        ingress {
            description     = "Traffic from frontend"
            from_port       = 0
            to_port         = 0
            protocol        = "-1"
            security_groups = [aws_security_group.frontend-security-group.id]
        }
        egress {
            from_port        = 0
            to_port          = 0
            protocol         = "-1"
            cidr_blocks      = ["0.0.0.0/0"]
            ipv6_cidr_blocks = ["::/0"]
        }
        tags = {
            Name = "backend-sg"
        }
    }
    ```
    ```
    resource "aws_security_group" "rds-security-group" {
        name        = "rds-sg"
        description = "Allow backend traffic"
        vpc_id      = aws_vpc.deft-source-vpc.id
        ingress {
            description     = "Traffic from backend"
            from_port       = 3306
            to_port         = 3306
            protocol        = "tcp"
            security_groups = [aws_security_group.backend-security-group.id]
        }
        egress {
            from_port        = 0
            to_port          = 0
            protocol         = "-1"
            cidr_blocks      = ["0.0.0.0/0"]
            ipv6_cidr_blocks = ["::/0"]
        }
        tags = {
            Name = "backend-sg"
        }
    }
    ```
13. Create Subnet-group for RDS instance and RDS instance using following code:
    ```
    resource "aws_db_subnet_group" "db-subnet-group" {
        name       = "db-subnet-group"
        subnet_ids = [aws_subnet.dev-private-subnet.id, aws_subnet.dev-public-subnet.id]
        tags = {
            Name = "DB subnet group"
        }
    }
    ```
    ```
    resource "aws_db_instance" "deft-source-db" {
        allocated_storage      = 10
        db_name                = "db"
        engine                 = "mysql"
        engine_version         = "8.0"
        instance_class         = "db.t3.micro"
        username               = "admin"
        password               = "password"
        db_subnet_group_name   = aws_db_subnet_group.db-subnet-group.name
        vpc_security_group_ids = [aws_security_group.rds-security-group.id]
        skip_final_snapshot    = true
    }
    ```
14. Define `task execution role` and attach appropriate policies to it. Then we will assign this role to task definitions.
    ```
    resource "aws_iam_role" "task-execution-role" {
        name = "task-execution-role"
        assume_role_policy = jsonencode({
            Version = "2012-10-17"
            Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Principal = {
                Service = "ecs-tasks.amazonaws.com"
                }
            },
            ]
        })

        tags = {
            Name = "task-execution-role"
        }
    }
    ```
    ```
    resource "aws_iam_role_policy_attachment" "task-policy-attach" {
        role       = aws_iam_role.task-execution-role.name
        policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
    }
    ```
    ```
    resource "aws_iam_role_policy_attachment" "ecr-policy-attach" {
        role       = aws_iam_role.task-execution-role.name
        policy_arn = "arn:aws:iam::policy/ECR_FullAccess"
    }
    ```
    ```
    resource "aws_iam_role_policy_attachment" "cloudmap-policy-attach" {
        role       = aws_iam_role.task-execution-role.name
        policy_arn = "arn:aws:iam::aws:policy/AWSCloudMapFullAccess"
    }
    ```
    ```
    data "aws_iam_policy_document" "service-connect-policy-document" {
        statement {
            effect = "Allow"
            actions = [
            "appmesh: *",
            "servicediscovery:ListNamespaces",
            "servicediscovery:ListServices",
            "servicediscovery:ListInstances"
            ]
            resources = ["*"]
        }
    }
    ```
    ```
    resource "aws_iam_policy" "service-connect-policy" {
        name   = "service-connect-policy"
        policy = data.aws_iam_policy_document.service-connect-policy-document.json
    }
    ```
    ```
    resource "aws_iam_role_policy_attachment" "service-connect-policy-attach" {
        role       = aws_iam_role.task-execution-role.name
        policy_arn = aws_iam_policy.service-connect-policy.arn
    }
    ```

15. Let's define backend task definition and service as:
    ```
    resource "aws_ecs_task_definition" "backend-service-taskdef" {
        family                   = "backend"
        execution_role_arn       = aws_iam_role.task-execution-role.arn
        task_role_arn            = aws_iam_role.task-execution-role.arn
        network_mode             = "awsvpc"
        requires_compatibilities = ["FARGATE"]
        cpu                      = 256
        memory                   = 512
        container_definitions = jsonencode([
            {
            name      = "backend"
            image     = "<YOUR_BACKEND_APP_IMAGE_HERE>"
            essential = true
            portMappings = [
                {
                containerPort = 3456
                hostPort      = 3456
                protocol      = "tcp"
                name          = "backend-service-port"
                }
            ]
            Environment = [{
                name  = "DATABASE_URL",
                value = "mysql://admin:password@${aws_db_instance.deft-source-db.endpoint}/db"
            }]
            }
        ])
        depends_on = [aws_db_instance.deft-source-db]
    }
    ```
    ```
    resource "aws_service_discovery_service" "service-a" {
        name         = "backend-service"
        namespace_id = aws_service_discovery_http_namespace.stagging-namespace.id
    }
    ```
    ```
    resource "aws_ecs_service" "backend-service" {
        name            = "backend-service"
        cluster         = aws_ecs_cluster.demo.id
        task_definition = aws_ecs_task_definition.backend-service-taskdef.arn
        desired_count   = 1
        launch_type     = "FARGATE"
        network_configuration {
            subnets          = [aws_subnet.dev-public-subnet.id, aws_subnet.dev-private-subnet.id]
            assign_public_ip = true
            security_groups  = [aws_security_group.backend-security-group.id]
        }
        service_connect_configuration {
            enabled   = true
            namespace = aws_service_discovery_http_namespace.stagging-namespace.arn
            service {
            client_alias {
                dns_name = "backend-service.${aws_service_discovery_http_namespace.stagging-namespace.name}"
                port     = 3456
            }
            port_name = "backend-service-port"
            }
        }
        service_registries {
            registry_arn = aws_service_discovery_service.service-a.arn
        }
    }
    ```

16. Next define frontend task definition and service as: 
    ```
    resource "aws_ecs_task_definition" "frontend-service-taskdef" {
        family                   = "frontend"
        execution_role_arn       = aws_iam_role.task-execution-role.arn
        task_role_arn            = aws_iam_role.task-execution-role.arn
        network_mode             = "awsvpc"
        requires_compatibilities = ["FARGATE"]
        cpu                      = 256
        memory                   = 512
        container_definitions = jsonencode([
            {
            name      = "frontend"
            image     = "<YOUR_FRONTEND_APP_IMAGE_HERE>"
            essential = true
            portMappings = [
                {
                containerPort = 3000
                hostPort      = 3000
                protocol      = "tcp"
                }
            ]
            Environment = [{
                name  = "BACKEND_API_URL",
                value = "http://backend-service.${aws_service_discovery_http_namespace.stagging-namespace.name}:3456"
            }]
            }
        ])
        depends_on = [aws_ecs_service.backend-service]
    }
    ```
    ```
    resource "aws_service_discovery_service" "service-b" {
        name         = "frontend-service"
        namespace_id = aws_service_discovery_http_namespace.stagging-namespace.id
    }
    ```
    ```
    resource "aws_ecs_service" "frontend-service" {
        name            = "frontend-service"
        cluster         = aws_ecs_cluster.demo.id
        task_definition = aws_ecs_task_definition.frontend-service-taskdef.arn
        desired_count   = 1
        launch_type     = "FARGATE"
        network_configuration {
            subnets          = [aws_subnet.dev-public-subnet.id]
            assign_public_ip = true
            security_groups  = [aws_security_group.frontend-security-group.id]
        }
        service_connect_configuration {
            enabled   = true
            namespace = aws_service_discovery_http_namespace.stagging-namespace.arn
        }
        service_registries {
            registry_arn = aws_service_discovery_service.service-b.arn
        }
        load_balancer {
            target_group_arn = aws_lb_target_group.ecs-lb-target-group.arn
            container_name   = "frontend"
            container_port   = 3000
        }
        depends_on = [aws_ecs_service.backend-service, aws_lb.ecs-lb]
    }
    ```
17. In the next step we will define AWS WAF configurations. Let's first create Web-ACL and then associate with load balancer resource. To do this use following code:
    ```
    resource "aws_wafv2_web_acl" "ECS-Web-ACL" {
        name  = "ECS-Web-ACL"
        scope = "REGIONAL"
        default_action {
            allow {}
        }
        rule {
            name     = "rule-1"
            priority = 1
            action {
            allow {}
            }
            statement {
            geo_match_statement {
                country_codes = ["IN"]
            }
            }
            visibility_config {
            cloudwatch_metrics_enabled = true
            metric_name                = "rule-1-metric"
            sampled_requests_enabled   = true
            }
        }
        visibility_config {
            cloudwatch_metrics_enabled = true
            metric_name                = "rule-1-metric"
            sampled_requests_enabled   = true
        }

    }
    ```
    ```
    resource "aws_wafv2_web_acl_association" "ECS-WAF-Association" {
        resource_arn = aws_lb.ecs-lb.arn
        web_acl_arn  = aws_wafv2_web_acl.ECS-Web-ACL.arn
    }
    ```

18. Infrastructure definitions are completed. Now we need to deploy these resources on AWS. To do this, first open terminal and run command:
    ```
    $ terraform init
    ```
     This will initialize a terraform configuration directory. Initializing a configuration directory downloads and installs the providers defined in the configuration.
    
19. Then to validate our configuration, run command:
    ```
    $ terraform validate
    ```
    If the configuration is valid it will return success message as ` Success! The configuration is valid.`

20. Once we get success message from validation command, we are all set to apply these configurations and deploy the resources on cloud. To do this, run command:
    ```
    $ terraform apply
    ```
    Before applying any changes, Terraform prints out the execution plan which describes the actions Terraform will take in order to change your infrastructure to match the configuration. Terraform will now pause and wait for your approval. So type `yes` at the confirmation prompt to proceed.
21. We are now having our resources on cloud. To verify deployment, login to AWS Account. Go to `EC2 dashboard`. Select `Load Balancers`. You may see a load balancer is created by terraform. Copy its `DNS Name` and paste in the browser. You may see the index page of your application. Now you may test your whole application here. 
