# Pulumi Modules

## VPC Module
1. Create *vpc* folder.
2. Inside *vpc* folder, create *__init__.py* file.
3. Import the following in the file:
    - from .main import vpc
4. Now, inside *vpc* folder create *main.py* file.
5. Import the following:
    - pulumi_aws as aws
6. Define a class named *vpc*.
3. Inside *vpc* class, define the *__init__* constructor & inside it call the following functions:
    - aws.ec2.Vpc()
    - aws.get_availability_zones()
    - for public
        - aws.ec2.InternetGateway()
        - aws.ec2.RouteTable()
        - aws.ec2.Subnet()
        - aws.ec2.RouteTableAssociation()
    - for private
        - aws.ec2.RouteTable()
        - aws.ec2.Subnet()
        - aws.ec2.RouteTableAssociation()
4. Click [code](https://github.com/sahilphule/pulumi/blob/master/src/inflection_zone_pulumi/modules/aws/vpc/main.py) for reference.
5. Now we have completed defining the **VPC Module**.

---

## S3 Module
1. Create *s3* folder.
2. Inside *s3* folder, create *__init__.py* file.
3. Import the following in the file:
    - from .main import s3
4. Now, inside *s3* folder create *main.py* file.
5. Import the following:
    - pulumi_aws as aws
6. Define a class named *s3*.
7. Inside *s3* class, define the *__init__* constructor & inside it call the following functions:
    - aws.s3.BucketV2()
    - aws.s3.BucketVersioningV2()
8. Click [code](https://github.com/sahilphule/pulumi/blob/master/src/inflection_zone_pulumi/modules/aws/s3/main.py) for reference.
9. Now we have completed defining the **S3 Module**.

---

## RDS Module
1. Create *rds* folder.
2. Inside *rds* folder, create *__init__.py* file.
3. Import the following in the file:
    - from .main import rds
4. Now, inside *rds* folder, create *data.py* file and import the following:
    - import pulumi_aws as aws
5. Call the following function:
    - aws.ec2.get_ami()
6. Click [code](https://github.com/sahilphule/pulumi/blob/master/src/inflection_zone_pulumi/modules/aws/rds/data.py) for reference.
6. Now, inside *rds* folder create *main.py* file.
7. Import the following:
    - pulumi
    - pulumi_aws as aws
    - from . import data
8. Define a class named *rds*.
9. Inside *rds* class, define the *__init__* constructor & inside it call the following functions:
    - for database
        - aws.rds.SubnetGroup()
        - aws.ec2.SecurityGroup()
        - aws.ec2.SecurityGroupIngressArgs()
        - aws.ec2.SecurityGroupEgressArgs()
        - aws.rds.Instance()
    - for bastion-host
        - aws.ec2.SecurityGroup()
        - aws.ec2.SecurityGroupIngressArgs()
        - aws.ec2.SecurityGroupEgressArgs()
        - aws.ec2.KeyPair()
        - aws.ec2.Instance()
10. Export the following outputs:
    - DB_HOST
    - bastion-host-ip
11. Click [code](https://github.com/sahilphule/pulumi/blob/master/src/inflection_zone_pulumi/modules/aws/rds/main.py) for reference.
12. Now we have completed defining the **RDS Module**.

---

## Load Balancer Module
1. Create *load_balancer* folder.
2. Inside *load_balancer* folder, create *__init__.py* file.
3. Import the following in the file:
    - from .main import load_balancer
4. Now, inside *load_balancer* folder create *main.py* file.
5. Import the following:
    - pulumi
    - pulumi_aws as aws
6. Define a class named *load_balancer*.
7. Inside *load_balancer* class, define the *__init__* constructor & inside it call the following functions:
    - aws.ec2.SecurityGroup()
    - aws.lb.LoadBalancer()
    - aws.lb.TargetGroup()
    - aws.lb.Listener()
8. Export the following output:
    - url
9. Click [code](https://github.com/sahilphule/pulumi/blob/master/src/inflection_zone_pulumi/modules/aws/load_balancer/main.py) for reference.
10. Now we have completed defining the **Load Balancer Module**.

---

## ECS Module
1. Create *ecs* folder.
2. Inside *ecs* folder, create *__init__.py* file.
3. Import the following in the file:
    - from .main import ecs
4. Now, inside *ecs* folder, create *data.py* file and import the following:
    - import pulumi_aws as aws
5. Define the following:
    - ecs_task_role_policy_document
6. Click [code](https://github.com/sahilphule/pulumi/blob/master/src/inflection_zone_pulumi/modules/aws/ecs/data.py) for reference.
6. Now, inside *ecs* folder create *main.py* file.
7. Import the following:
    - pulumi
    - pulumi_aws as aws
    - from . import data
    - import json
8. Define a class named *ecs*.
9. Inside *ecs* class, define the *__init__* constructor & inside it call the following functions:
    - aws.ecs.Cluster()
    - aws.iam.Role()
    - aws.iam.RolePolicyAttachment()
    - aws.ecs.TaskDefinition()
    - aws.ecs.Service()
10. Click [code](https://github.com/sahilphule/pulumi/blob/master/src/inflection_zone_pulumi/modules/aws/ecs/main.py) for reference.
11. Now we have completed defining the **ECS Module**.

---

## EKS Module
1. Create *eks* folder.
2. Inside *eks* folder, create *__init__.py* file.
3. Import the following in the file:
    - from .main import eks
4. Now, inside *eks* folder, create *data.py* file and import the following:
    - import pulumi_aws as aws
5. Define the following:
    - eks_cluster_role_policy_document
    - eks_node_group_role_policy_document
6. Click [code](https://github.com/sahilphule/pulumi/blob/master/src/inflection_zone_pulumi/modules/aws/eks/data.py) for reference.
6. Now, inside *eks* folder create *main.py* file.
7. Import the following:
    - pulumi_aws as aws
    - from . import data
    - import json
8. Define a class named *eks*.
9. Inside *eks* class, define the *__init__* constructor & inside it call the following functions:
    - for eks-cluster
        - aws.iam.Role
        - aws.iam.RolePolicyAttachment()
        - aws.ec2.SecurityGroup()
        - aws.ec2.SecurityGroupIngressArgs()
        - aws.eks.Cluster()
        - aws.eks.ClusterVpcConfigArgs()
    - for eks-node-groups
        - aws.iam.Role()
        - aws.iam.RolePolicyAttachment()
        - aws.iam.RolePolicyAttachment()
        - aws.iam.RolePolicyAttachment()
        - aws.eks.NodeGroup()
        - aws.eks.NodeGroupScalingConfigArgs()
10. Click [code](https://github.com/sahilphule/pulumi/blob/master/src/inflection_zone_pulumi/modules/aws/eks/main.py) for reference.
11. Now we have completed defining the **EKS Module**.

---