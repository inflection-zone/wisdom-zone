# AWS Terraform Modules

Create the **aws-modules** directory.

The folder structure for the above created directory is as follows:

```
aws-modules
├───ecr
│       main.tf
│       outputs.tf
│       variables.tf
│
├───ecs
│       data.tf
│       main.tf
│       variables.tf
│
├───eks
│       data.tf
│       main.tf
│       variables.tf
│
├───load-balancer
│       main.tf
│       outputs.tf
│       variables.tf
│
├───rds
│       data.tf
│       main.tf
│       outputs.tf
│       variables.tf
│
├───s3
│       main.tf
│       output.tf
│       variables.tf
│
└───vpc
        main.tf
        outputs.tf
        variables.tf
```

---

## VPC Module
Let's start with the VPC module.
1. Create *vpc* folder inside the above-created directory.
2. Inside *vpc* folder create *main.tf* file.
3. Define the following resources:
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
4. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/vpc/main.tf) for reference.
5. Now the *main.tf* file definition for *VPC* has been created.
6. Now we will create *variables.tf* file inside *vpc* folder for declaring variables.
7. Declare the following variables:
    - vpc-properties
8. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/vpc/variables.tf) for reference.
9. We have completed declaring variables for the *VPC module*.
10. Now we will declare outputs for the *VPC module*.
11. Create *outputs.tf* file and add the following outputs:
    - vpc-id
    - vpc-private-subnets
    - vpc-public-subnets
12. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/vpc/outputs.tf) for reference.
13. Now we have completed defining the **VPC Module**.

---

## S3 Module
We will use S3 to store and access .env files for ecs containers.
1. Create *s3* folder inside the *aws-modules* directory.
2. Inside it, create *main.tf* file & define the following resources:
    - aws_s3_bucket
    - aws_s3_bucket_versioning
3. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/s3/main.tf) for reference.
4. We have completed defining *main.tf* file.
5. Now create *variables.tf* file & declare the following variables:
    - s3-properties
6. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/s3/variables.tf) for reference:
7. The *variables.tf* file has been declared.
8. Now create *outputs.tf* file, inside it define the following outputs:
    - s3-bucket-id
9. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/s3/output.tf) for reference.
10. We have completed defining the **S3 Module**.

---

## RDS Module
For database, we will use MySQL RDS.  
1. Create *rds* folder inside the *aws-modules* directory.
2. Inside *rds* folder, create *data.tf* file.
3. Define the following data:
    - aws_ami
4. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/rds/data.tf) for reference.
5. We have completed defining the *data.tf* file.
6. Now create *main.tf* file & define the following resources:
    - for database
        - aws_db_subnet_group
        - aws_security_group
        - aws_db_instance
    - for bastion
        - aws_security_group
        - aws_key_pair
7. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/rds/main.tf) for reference.
8. The definition of *main.tf* file is completed.
9. Now we will create *variables.tf* file & inside it declare the following variables:
    - database-properties
    - bastion-properties
    - vpc-id
    - vpc-public-subnets
    - vpc-private-subnets
10. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/rds/variables.tf) for reference.
11. The *variables.tf* file have been declared.
12. Now we will define the outputs.
13. Create *outputs.tf* file.
14. Inside the *outputs.tf* file, define the following outputs:
    - DB_HOST
    - bastion-host-ip
15. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/rds/outputs.tf) for reference.
16. We have completed defining the **RDS Module**.

---

## ECR Module
Let's start with the ECR Module
1. Create *ecr* folder inside the above-created *aws-modules* directory.
2. Inside *ecr* folder, create *main.tf* file.
3. In *main.tf* file, define the following resources:
    - aws_ecr_repository
4. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/ecr/main.tf) for reference.
5. The definition of *main.tf* file is complete.
6. Now we will create *variables.tf* file and declare the following variables:
    - ecr-repository-name
7. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/ecr/variables.tf) for reference.
8. The declaration of *variables.tf* file is completed.
9. Now we will create *outputs.tf* file and define the following output:
    - repository-url
10. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/ecr/outputs.tf) for reference.
11. The definition of *outputs.tf* file is complete.
12. We have completed defining the **ECR Module**.

---

## Load Balancer Module
Let's start with the Load Balancer Module
1. Create *load-balancer* folder.
2. Inside *load-balancer* folder, create *main.tf* file & declare the following resources:
    - aws_security_group
    - aws_lb
    - aws_lb_target_group
    - aws_lb_listener
3. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/load-balancer/main.tf) for reference.
4. The *main.tf* file for Load Balancer Module has been defined.
5. Now we will define *variables.tf* file.
6. Create *variables.tf* file & declare the following variables:
    - load-balancer-properties
    - vpc-id
    - vpc-public-subnets
7. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/load-balancer/variables.tf) for reference.
8. The *variable.tf* file for Load Balancer Module has been defined.
9. Now we will define outputs.tf file.
10. Create *outputs.tf* file & define the following outputs:
    - load-balancer-sg-id
    - load-balancer-tg-arn
11. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/load-balancer/outputs.tf) for reference.
12. We have completed defining the **Load Balancer Module**.

---

## ECS Module
Let's start with the ECS Module
1. Create *ecs* folder in *aws-modules* directory.
2. Inside *ecs* folder, create *data.tf* file.
3. In *data.tf* file, define the following data:
    - aws_iam_policy_document
4. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/ecs/data.tf) for reference.
5. Definition of *data.tf* file is completed.
6. Now we will define *main.tf* file.
7. Inside *ecs* folder create *main.tf* file & define the following resources:
    - for cluster
        - aws_ecs_cluster
    - for task
        - aws_iam_role
        - aws_iam_role_policy_attachment
        - aws_ecs_task_definition
    - for service
        - aws_security_group
        - aws_ecs_service
8. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/ecs/main.tf) for reference.
9. The *main.tf* file for ECS has been defined.
10. Now we will define *variables.tf* file.
12. Create *variables.tf* file & declare the following variables:
    - ecs-properties
    - ecs-container-definition
    - vpc-id
    - vpc-public-subnets
    - load-balancer-sg-id
    - load-balancer-tg-arn
13. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/ecs/variables.tf) for reference.
14. We have completed defining the **ECS Module**.

---

## EKS Module
Let's start with the EKS Module
1. Create *eks* folder in the above-created *aws-modules* directory.
2. Inside *eks* folder create *data.tf* file.
3. In *data.tf* file, define the following data:
    - aws_iam_policy_document
4. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/eks/data.tf) for reference.
5. Definition of *data.tf* file is completed.
6. Now we will define *main.tf* file.
7. Inside *eks* folder create *main.tf* file & define the following resources:
    - for cluster
        - aws_iam_role
        - aws_iam_role_policy_attachment
        - aws_eks_cluster
    - for node
        - aws_iam_role
        - aws_iam_role_policy_attachment
        - aws_iam_role_policy_attachment
        - aws_iam_role_policy_attachment
        - aws_eks_node_group    
8. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/eks/main.tf) for reference.
9. The *main.tf* file for EKS has been defined.
10. Now we will define variables.tf file.
12. Create *variables.tf* file inside *eks* folder & declare the following variables:
    - eks-properties
    - vpc-public-subnets
13. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/aws/eks/variables.tf) for reference.
14. We have completed defining the **EKS Module**.

---