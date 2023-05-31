# Terraform Code to Setup AWS Infra for EKS Cluster

## Objective
* Setup AWS infrastructure for EKS cluster using Terraform. 

## Prerequisites 
To create AWS infrastructure using terraform, one should have
1. An AWS account
2. AWS CLI installed and configured with IAM user credentials
3. Terraform installed. (If want to install Terraform please refer installation steps from this [document](./terraform-ec2.md))

## Define Infrastructure
1. Create a folder at your desired location. Create a new file inside that folder and name it as `main.tf`.
2. Open this folder with `VS Code` or any other code editor. Open `main.tf`. Start defining resources.
3. First define Terraform configurations as :
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
4. Next define providers i.e. `aws` and `kubernetes` using following lines of code:
    ```
    provider "aws" {
        region = "ap-south-1"
    }
    ```
    ```
    provider "kubernetes" {
        host                   = data.aws_eks_cluster.cluster.endpoint
        cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
        exec {
            api_version = "client.authentication.k8s.io/v1beta1"
            args        = ["eks", "get-token", "--cluster-name", aws_eks_cluster.cluster.id]
            command     = "aws"
        }
    } 
    ```
5. In this tutorial, we will create following AWS resources: 
    1. VPC & subnets
    2. Internet Gateway, Route Tables and their associations
    3. IAM role for EKS cluster and appropriate policy attachments
    4. Security groups for Application Load balancer and EKS cluster
    5. EKS Cluster
    6. IAM role for node-group and policies to attach
    7. Node group
    8. Kubernetes namespace, deployment and service resources
    9. Application load balancer, target group and listener
    10. Web-ACl and its association with load balancer

6. Let's start defining AWS resources listed above. First we will create VPC and subnets as:
    ```
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
7. Then we need to create route tables and their association with appropriate subnets and an internet gateway.
    ```
    resource "aws_internet_gateway" "deft-source-igw" {
        vpc_id = aws_vpc.deft-source-vpc.id

        tags = {
            Name = "deft-source-igw"
        }
    }
    ```
    ```
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
    ```
    ```
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
    ```
    ```
    resource "aws_route_table_association" "public-rt-association" {
        subnet_id      = aws_subnet.dev-public-subnet.id
        route_table_id = aws_route_table.public-rt.id
    }
    ```
    ```
    resource "aws_route_table_association" "private-rt-association" {
        subnet_id      = aws_subnet.dev-private-subnet.id
        route_table_id = aws_route_table.private-rt.id
        }
    ```

8. In this step, we will create a cluster-role and attach cluster policy to it as:
    ```
    resource "aws_iam_role" "demo-cluster-role" {
        name = "cluster-role"

        assume_role_policy = <<POLICY
            {
            "Version": "2012-10-17",
            "Statement": [
                {
                "Effect": "Allow",
                "Principal": {
                    "Service": "eks.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
                }
            ]
            }
            POLICY
    }
    ```
    ```
    resource "aws_iam_role_policy_attachment" "amazon-eks-cluster-policy" {
        policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
        role       = aws_iam_role.demo-cluster-role.name
    }
    ```

9. Next we will define security groups for AWS ALB and EKS cluster using following code:
    ```
    resource "aws_security_group" "demo-alb-sg" {
        name        = "demo-alb-sg"
        description = "Allow Traffic from internet"
        vpc_id      = aws_vpc.deft-source-vpc.id

        ingress {
            description = "Traffic from internet"
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
    } 
    ```
    ```
    resource "aws_security_group" "demo-eks-sg" {
        name        = "demo-eks-sg"
        description = "Allow ALB Traffic"
        vpc_id      = aws_vpc.deft-source-vpc.id

        ingress {
            description     = "Traffic from ALB"
            from_port       = 0
            to_port         = 0
            protocol        = "-1"
            security_groups = [aws_security_group.demo-alb-sg.id]
        }

        egress {
            from_port        = 0
            to_port          = 0
            protocol         = "-1"
            cidr_blocks      = ["0.0.0.0/0"]
            ipv6_cidr_blocks = ["::/0"]
        }
    } 
    ```
10. Now define EKS Cluster as:
    ```
    resource "aws_eks_cluster" "cluster" {
        name     = "Demo-cluster"
        role_arn = aws_iam_role.demo-cluster-role.arn

        vpc_config {
            subnet_ids = [
            aws_subnet.dev-private-subnet.id,
            aws_subnet.dev-public-subnet.id
            ]
            security_group_ids = [aws_security_group.demo-eks-sg.id]
        }

        depends_on = [aws_iam_role_policy_attachment.amazon-eks-cluster-policy]
    } 
    ``` 
11. Next we will create IAM role for node-group and attach policies to it.
    ```
    resource "aws_iam_role" "nodes-role" {
        name = "eks-nodes-role"

        assume_role_policy = jsonencode({
            Statement = [{
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {
                Service = "ec2.amazonaws.com"
            }
            }]
            Version = "2012-10-17"
        })
    } 
    ``` 
    ```
    resource "aws_iam_role_policy_attachment" "amazon-eks-worker-node-policy" {
        policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
        role       = aws_iam_role.nodes-role.name
    }

    resource "aws_iam_role_policy_attachment" "amazon-eks-cni-policy" {
        policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
        role       = aws_iam_role.nodes-role.name
    }

    resource "aws_iam_role_policy_attachment" "amazon-ec2-container-registry-read-only" {
        policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
        role       = aws_iam_role.nodes-role.name
    }
    ```
    ```
    resource "aws_iam_policy" "aws-alb-policy" {
        policy = file("./alb_policy.json")
        name   = "ALBRegisterTargetsPolicy"
    }

    resource "aws_iam_role_policy_attachment" "alb-register-targets" {
        policy_arn = aws_iam_policy.aws-alb-policy.arn
        role       = aws_iam_role.nodes-role.name
    }
    ```
    Here we need to create a customized policy that allow our nodes to register targets in target group of ALB. For that purpose, create a file named `alb_policy.json` in current directory. And refer this file in above code to create `aws-alb-policy`. That file contains following code:
    ```
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "iam:CreateServiceLinkedRole"
                ],
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                        "iam:AWSServiceName": "elasticloadbalancing.amazonaws.com"
                    }
                }
            },
            {
                "Effect": "Allow",
                "Action": [
                    "elasticloadbalancing:RegisterTargets",
                    "elasticloadbalancing:DeregisterTargets"
                ],
                "Resource": "arn:aws:elasticloadbalancing:*:*:targetgroup/*/*"
            }
        ]
    }
    ```

12. Now we will create node group as:
    ```
    resource "aws_eks_node_group" "demo-node-group" {
        cluster_name    = aws_eks_cluster.cluster.name
        node_group_name = "demo-nodegroup"
        node_role_arn   = aws_iam_role.nodes-role.arn
        subnet_ids = [
            aws_subnet.dev-private-subnet.id,
            aws_subnet.dev-public-subnet.id
        ]
        ami_type       = "AL2_x86_64"
        capacity_type  = "ON_DEMAND"
        instance_types = ["t3.small"]
        scaling_config {
            desired_size = 2
            max_size     = 3
            min_size     = 2
        }
        update_config {
            max_unavailable = 1
        }

        depends_on = [
            aws_eks_cluster.cluster
        ]
    }
    ```

13. Then we will create namespace, deployment and kubenetes service as:
    ```    
    resource "kubernetes_namespace" "app-namespace" {
        metadata {
            name = "app-namespace"
        }
    }
    ```
    ```
    resource "kubernetes_deployment" "frontend" {
        metadata {
            name      = "frontend-deployment"
            namespace = kubernetes_namespace.app-namespace.metadata[0].name
            labels = {
            app = "frontend-app"
            }
        }
        spec {
            replicas = 1
            selector {
            match_labels = {
                app = "frontend-app"
            }
            }
            template {
                metadata {
                    labels = {
                    app = "frontend-app"
                    }
                }
                spec {
                    container {
                        name  = "frontend-container"
                        image = "623865992637.dkr.ecr.ap-south-1.amazonaws.com/demo:latest"
                        env {
                            name  = "BACKEND_API_URL"
                            value = "http://nodeapp:3456"
                        }
                    }
                }
            }
        }
        depends_on = [
        aws_eks_node_group.demo-node-group
        ]
    }
    ```
    ```
    resource "kubernetes_service" "frontend-service" {
        metadata {
            name      = "frontend"
            namespace = kubernetes_namespace.app-namespace.metadata[0].name
        }
        spec {
            type = "NodePort"
            port {
            port        = 3000
            target_port = 3000
            protocol    = "TCP"
            }
            selector = {
            app = "frontend-app"
            }
        }
        depends_on = [
            kubernetes_deployment.frontend
        ]
    }
    ```
14. Next we will create application load balancer and target group & listener for it
    ```
    resource "aws_lb" "demo-alb" {
        name               = "demo-alb"
        internal           = false
        load_balancer_type = "application"
        security_groups    = [aws_security_group.demo-alb-sg.id]
        subnets            = [aws_subnet.dev-private-subnet.id, aws_subnet.dev-public-subnet.id]
    }
    ```
    ```
    resource "aws_lb_target_group" "demo-alb-target-group" {
        name        = "demo-alb-target-group"
        port        = kubernetes_service.frontend-service.spec[0].port[0].node_port
        protocol    = "HTTP"
        target_type = "instance"
        vpc_id      = aws_vpc.deft-source-vpc.id
        health_check {
            healthy_threshold   = 5
            interval            = 50
            path                = "/"
            matcher             = "200"
            protocol            = "HTTP"
            port                = jsonencode(kubernetes_service.frontend-service.spec[0].port[0].node_port)
            timeout             = 30
            unhealthy_threshold = 5
        }
    }
    ```
    ```
    resource "aws_lb_listener" "front-end" {
        load_balancer_arn = aws_lb.demo-alb.arn
        port              = "80"
        protocol          = "HTTP"

        default_action {
            type             = "forward"
            target_group_arn = aws_lb_target_group.demo-alb-target-group.arn
        }
    }
    ```
15. In the last step, we will define WAF configurations as:
    ```
    resource "aws_wafv2_web_acl" "EKS-Web-ACL" {
        name  = "EKS-Web-ACL"
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
    resource "aws_wafv2_web_acl_association" "EKS-WAF-Association" {
        resource_arn = aws_lb.demo-alb.arn
        web_acl_arn  = aws_wafv2_web_acl.EKS-Web-ACL.arn
    }
    ```

16. Once done with infrastructure defining code, we need to deploy these infra resources on AWS. To do this, first open terminal and run command:
    ```
    $ terraform init
    ```
     This will initialize a terraform configuration directory. Initializing a configuration directory downloads and installs the providers defined in the configuration. 
    
17. Then to validate our configuration, run command:
    ```
    $ terraform validate
    ```
    If the configuration is valid it will return success message as ` Success! The configuration is valid.`

18. Once we get success message from validation command, we are all set to apply these configurations and deploy the resources on cloud. To do this, run command:
    ```
    $ terraform apply
    ```
    Before applying any changes, Terraform prints out the execution plan which describes the actions Terraform will take in order to change your infrastructure to match the configuration. Terraform will now pause and wait for your approval. So type `yes` at the confirmation prompt to proceed. 

19. On completion of apply process, login to AWS management console and verify deployed resources. Now we need to go to `EC2 dashboard`. Select `Instances`. Select any of running instances and go to `Security`. Select security group of the instance and click on `Edit inbound rule`. Click on `Add rule`. Select `All traffic` under type section then `custom` under source tab and in CIDR block field, select security group of load balancer. This rule will allow traffic from load balancer to nodes.

20. Now select `Target Groups` on `EC2 Dashboard`. Select target group created by terraform an click on `Register Targets`. On the next page select all running instances from mentioned VPC and click on `Include as pending below`. At the bottom right corner of the same page, click on `Register Targets`. You may see that the targets are registered at Target Group. Wait until state of the targets become `healthy`.

21. Once the targets are healthy, go to `Load Balancers`. Copy DNS of ALB created by terraform and paste it into browser. You may see index pade of your application.