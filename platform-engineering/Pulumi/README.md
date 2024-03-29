# AWS Infrastucture Using Pulumi
This documentation covers overview of Pulumi and some sample codes to create AWS Infra.

## Prerequisites
* An AWS account, AWS CLI installed & configured on your machine.
* Install language runtime. (Node.js for javascript & typescript) 
* Install Pulumi with following link according to your OS:
        https://www.pulumi.com/docs/get-started/install/

## Overview and Sample Examples

*  ### [Infrastructure for School App](./Pulumi%20Document.md) 

    * Overview of Pulumi
    * Sample code to create S3 bucket
    * Code to create AWS infra that includes ECS cluster, RDS Instance and more supporting AWS resources 

* ### [Infrastructure for Dockerized Application On EC2](./Pulumi-for-EC2-with%20script.md) 

    * Pulumi code to create an EC2 instance with Userdata script in custom VPC and other AWS resources. 
    * The code includes Userdata script for EC2 instance, through which we will spin up containers having a full stack node.js app using docker-compose while launching the instance. 

* ### [Infrastructure for dev env](./Pulumi-dev-env.md) 

    * This pulumi code will create many AWS resources like networking related components, EC2 and RDS instances with their supporting components.


