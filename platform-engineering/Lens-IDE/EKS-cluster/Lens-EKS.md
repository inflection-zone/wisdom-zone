# Deploy Workloads on EKS Cluster using Lens
## Objective
* In this tutorial, we will deploy workloads on Amazon EKS cluster using Lens IDE. 
* We will use RDS as database for this service.

## Prerequisites
* An AWS account
* Lens Desktop installed on your system. If you don't have Lens, please follow steps to install it documented [here](../minikube/Lens-minikube.md) 

## Create an EKS Cluster 

1. Login to your AWS Account (either as a `root` user or as an `IAM User` with sufficient permissions).
2. In `services`, search for `Elastic Kubernetes Service`. 
3. On EKS dashboard, Click on `Add Cluster` --> `Create`.
4. On `Configure cluster` page, specify name of cluster, select desired version of kubernetes and cluster service role. Here we need to create a new IAM role to associate with cluster. To do so: 
    i. Go to `IAM` console.
    ii. Click on `Roles` --> `Create role`.
    iii. On the next page, do following:

        a. Select AWS service under Trusted entity type section. 
        b. In `Use case` section, browse for `EKS`and select `Eks Cluster`. 
        c. Click on `Next`.

    <img src="./Images/eks-role-1.png" width="600" height="250"/> 
     &nbsp;<br> 
    iv. Here you may see that `AmazonEKSClusterPolicy` is already added to the role. Click on `Next`. 
    v. Enter a name for this role. Review and create role.
    vi. We need to add one more policy to this role i.e. RDS access policy. For that do following steps:

        a. Choose created role. 
        b. Under `Permissions` tab, click on `Add Permissions` --> `Attach Policies`. 
        c. On next page, select `AmazonRDSFullAccess` policy and attach it to the role.

5. Go to EKS dashboard, assign created role to our EKS cluster. Click on `Next`.
6. Specify networking here. Select your VPC and subnets and security group for cluster. Here we have to create a security group for cluster. For that: 
    i. Open EC2 dashboard. Click on `Security groups` under `Network and security` section. 
    ii. Click on `Create security group`.
    iii. On the next page, specify name and description of security group. 
    iv. Under `Inbound rules` section, click on `Add rule`. 
    v. Allow all traffic fron anywhere. Select `All traffic` type and destination `Anywhere IPV4`. And `Create security group`.

7. Assign this created security group to the cluster. 
8. Choose cluster IP family `IPV4`. make Cluster Endpoint access `Public`. Click `Next`. On the next page, don't configure any logging. Just click on `Next`.
9. On the next page, keep default add-ons and click on `Next`.
10. Review and create cluster. It will require few minutes for cluster to be ready.

## Create a Nodegroup
1. Once cluster gets ready, click on cluster, go to `Compute` tab, select `Add node group`.
2. On the next page i.e. noge group configuration, give a name to nodegroup, then we need to create an IAM role for nodes. To do so:
    i. Open the `IAM console`. 
    ii. In the left navigation pane, choose `Roles`.
    iii. On the Roles page, choose `Create role`. 
    iv. On the Select trusted entity page, do the following:

        a. In the Trusted entity type section, choose `AWS service`.
        b. Under Use case, choose `EC2`.
        c. Choose `Next`.

    v. On the Add permissions page, add following policies and choose `Next`:

        a. AmazonEKSWorkerNodePolicy.
        b. AmazonEC2ContainerRegistryReadOnly.
        c. AmazonEKS_CNI_Policy 

    vi. On the Name, review, and create page, do the following:
    
        a. For Role name, enter a unique name for your role, such as eks-nodegroup-role.
        b. For Description, replace the current text with descriptive text such as Amazon EKS - Node role.
        c. Under Add tags (Optional), add metadata to the role by attaching tags as key–value pairs. For more information about using tags in IAM, see Tagging IAM Entities in the IAM User Guide.
        d. Choose Create role. 

3. Assign this IAM role to node group and choose `Next`.
4. On Set compute and scaling configuration page, do following: 

    i. Select `Amazon Linux 2` in AMI type section.
    ii. Cpacity type: `On Demand`
    iii. Instance type: `t3.medium` (Choose according to your requirement)
    iv. Disk Size: `20 GB` (Decide according to your application requirement)
    v. In node group scaling configuration, all values i.e. desired, max and min are set to `2`.
    vi. In Node group update configuration, select `Number` and value `1`.
    vii. Choose `Next`.

5. Select all subnets on `Specify Networking` page and enable `Configure remote access to nodes`. In this section, do following:
    i. Specify a`key-pair` for accessing nodes remotely.
    ii. Allow remote access from: `All` (You may select `Slected security groups` and specify security groups to allow access)
    iii. Choose `Next`
6.  Review and create node group. It will take few minutes to setup the worker nodes.

## Create a SQL Server DB instance (RDS)
1. Open `RDS` console.
2. In the upper-right corner of the Amazon RDS console, choose the AWS Region in which you want to create the DB instance. 
3. In the navigation pane, choose Databases.
4. Choose Create database and make sure that `Standard create` is chosen. 
5. In Configuration, choose `Microsoft SQL Server`.
6. For Edition, choose `SQL Server community Edition`. For DB instance size, choose `Free tier`.
7. For DB instance identifier, enter `database-1`.
8. For Master username, enter a name for the master user, or keep the default name.
9. Choose `Don't connect to an EC2 compute resource`.
10. To use an automatically generated master password for the DB instance, select the Auto generate a password box. To enter your master password, clear the Auto generate a password box, and then enter the same password in Master password and Confirm password. 
11. In `Additional configuration`, give initial database name as `db`.
11. Choose Create database. To view the master username and password for the DB instance, choose View credential details. You can use the username and password that appears to connect to the DB instance as the master user. 
<img src="./Images/rds-instance.png" width="600" height="250"/> 
     &nbsp;<br> 

## Configure `kubectl` and Deploy Workloads 
1. To configure `kubectl` for our cluster, run following command in terminal:
    ```
    $ aws eks --region <region-name> update-kubeconfig --name <cluster-name>
    ```
2. Create [manifests](./manifests/). In nodeapp-deployment.yaml, modify env variable `Database_URL` using RDS instance's endpoint and credentials.
3. Open Lens Desktop. 
4. Browse Clusters. Select our eks cluster to connect. 
5. Then open terminal and move to folder containing manifests.
6. Run command:
    ```
    & kubectl apply -f .
    ```
7. You may see the output as: 
<img src="./Images/terminal.png" width="600" height="250"/> 
     &nbsp;<br> 
8. Now you may check all workloads one by one. 
    i. Overview: 
    <img src="./Images/overview.png" width="600" height="250"/> 
     &nbsp;<br>
    
    ii. Pods: 
  <img src="./Images/pods.png" width="600" height="250"/> 
     &nbsp;<br>

    iii. Services: 
    <img src="./Images/services.png" width="600" height="250"/> 
     &nbsp;<br> 

    iv. Pod logs:
    <img src="./Images/pod-logs.png" width="600" height="250"/> 
     &nbsp;<br>

9. You may also check these created resources on aws console.
    <img src="./Images/pods-eks.png" width="600" height="250"/> 
     &nbsp;<br>
10. Now, to test application, take public IP of a node on which our nginx-pod is deployed. And paste it into browser with `nodePort` of nginx-service. You may see the index page of your application as : 
    <img src="./Images/final-output.png" width="600" height="250"/> 
     &nbsp;<br>

    <img src="./Images/final-output-1.png" width="600" height="250"/> 
     &nbsp;<br>
