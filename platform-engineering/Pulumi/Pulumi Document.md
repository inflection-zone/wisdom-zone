# What is Pulumi 
* Pulumi is an open source infrastructure as code tool for creating, deploying, and managing cloud infrastructure. 
* Pulumi works with traditional infrastructures like VMs, networks, and databases, in addition to modern architectures, including containers, Kubernetes clusters, and serverless functions. 
* Pulumi supports 70+ public, private, and hybrid cloud service providers. 
* Pulumi utilizes the most popular programming languages to simplify provisioning and managing cloud resources. 
* Founded in 2017, Pulumi has fundamentally changed the way DevOps teams approach the concept of infrastructure-as-code. Instead of relying on domain-specific languages, Pulumi enables organizations to use real programming languages to provision and decommission cloud-native infrastructure. 
* Unlike Terraform, which has its proprietary language and syntax for defining infrastructure as code, Pulumi uses real languages. You can write configuration files in Python, JavaScript, or TypeScript. In other words, you are not forced to learn a new programming language only to manage infrastructure. 
* As a cloud-native platform, Pulumi allows you to deploy any type of cloud infrastructure — virtual servers, containers, applications, or serverless functions. You can also deploy and manage resources across multiple cloud providers such as AWS, Microsoft Azure, or PNAP Bare Metal Cloud. 
* Pulumi’s unique approach to IaC enables DevOps teams to manage their infrastructure as an application written in their chosen language. Using Pulumi, you can take advantage of functions, loops, and conditionals to create dynamic cloud environments. Pulumi helps developers create reusable components, eliminating the hassle of copying and pasting thousands of code lines. 
* Pulumi supports the following programming languages:
    - Python
    - JavaScript
    - Go
    - TypeScript
    - .NET languages (C#, F#, and VB) 

# Pulumi Overview
* Following diagram illustrates the structure and major components of Pulumi: 
<img src="pulumi-model.png" width="600" />

* Pulumi programs, written in general-purpose programming languages, describe how your cloud infrastructure should be composed. 
* To declare new infrastructure in your program, you allocate resource objects whose properties correspond to the desired state of your infrastructure. 
* Programs reside in a project, which is a directory that contains source code for the program and metadata on how to run the program. 
* After writing your program, you run the Pulumi CLI command `pulumi up` from within your project directory. This command creates an isolated and configurable instance of your program, known as a stack. 
* Stacks are similar to different deployment environments that you use when testing and rolling out application updates. 

# How Pulumi Works 
* The following diagram illustrates the interaction between parts of the system: 
<img src="engine-block-diagram.png" width="600" /> 

* A Pulumi program is executed by a language host to compute a desired state for a stack’s infrastructure. 
* The deployment engine compares this desired state with the stack’s current state and determines what resources need to be created, updated or deleted. 
* The engine uses a set of resource providers (such as AWS, Azure, Kubernetes, and so on) in order to manage the individual resources. 
* Description Of Pulumi components: 
  1. Language Hosts: The language host is responsible for running a Pulumi program and setting up an environment where it can register resources with the deployment engine. The language host is made up of two different pieces:
        - Language executor
        - Language runtime

  2. Deployment Engine: 
  - The deployment engine is responsible for computing the set of operations needed to drive the current state of your infrastructure into the desired state expressed by your program.
  - When a resource registration is received from the language host, the engine consults the existing state to determine if that resource has been created before. If it has not, the engine uses a resource provider in order to create it.
  - The deployment engine is embedded in the pulumi CLI itself.

  3. Resource Providers: A resource provider is made up of two different pieces:
        - A resource plugin, which is the binary used by the deployment engine to manage a resource. 
        - An SDK which provides bindings for each type of resource the provider can manage.

# Project:
  * Prerequisites:
  To get started with pulumi demo project, we need to have:
   1. An AWS account, AWS CLI installed & configured.
   2. Install language runtime. (Node.js for javascript & typescript) 
   3. Install Pulumi with following link according to your OS:
        https://www.pulumi.com/docs/get-started/install/
   
 * After installating Pulumi, verify everything is in working order by running the pulumi CLI. 
```
    > pulumi version
    v3.51.1`
``` 
* Now that we have set up our environment by installing Pulumi, installing our preferred language runtime (i.e. node.js as we are creating project using typescript), and configuring your AWS credentials, let’s create our first Pulumi program with following steps:
 1. Open command prompt & create new directory using `$ mkdir pulumidemo`. Next go into that directory `$ cd pulumidemo`.
 2. Create new Pulumi project using command `$ pulumi new aws-typescript`.
    **Note**: If this is your first time running pulumi new or other pulumi commands, you may be prompted to log in to the Pulumi Service. Hitting Enter at the prompt opens a browser for you to sign in or sign up.
 3. After logging in, the CLI will proceed with walking you through creating a new project. 
    - First, you will be asked for a project name and project description. Hit ENTER to accept the default values or specify new values. 
    - Next, you will be asked for a stack name. Hit ENTER to accept the default value of dev.
    - Finally, you will be prompted for some configuration values for the stack. For AWS projects, you will be prompted for the AWS region. You can accept the default value or choose another value like ap-south-1
    - After some dependency installations from `npm`, the project and stack will be ready.
  4. You may review the generated files :
   - Pulumi.yaml: This file defines the project
   - Pulumi.dev.yaml: This file contains configuration values for the stack you just initialized.
   - index.ts: It is the Pulumi program that defines your stack resources. It looks like:
   ```
    import * as pulumi from "@pulumi/pulumi";
    import * as aws from "@pulumi/aws";
    import * as awsx from "@pulumi/awsx";

    // Create an AWS resource (S3 Bucket)
    const bucket = new aws.s3.Bucket("my-bucket");

    // Export the name of the bucket
    export const bucketName = bucket.id;

  ```
  This Pulumi program creates a new S3 bucket and exports the name of the bucket.
  5. Deploy the stack: Let’s go ahead and deploy your stack using 
  `pulumi up`
  This command evaluates your program and determines the resource updates to make. First, a preview is shown that outlines the changes that will be made when you run the update:
  ```
  Previewing update (dev):

     Type                 Name            Plan
 +   pulumi:pulumi:Stack  pulumidemo-dev  create
 +   └─ aws:s3:Bucket     my-bucket       create

Resources:
    + 2 to create

Do you want to perform this update?
> yes
  no
  details

 ```

 Once the preview has finished, you are given three options to choose from. Choosing 'details' will show you a details of the changes to be made. Choosing 'yes' will create your new S3 bucket in AWS. Choosing 'no' will return you to the user prompt without performing the update operation.

```
 Do you want to perform this update? yes
Updating (dev):

     Type                 Name            Status
 +   pulumi:pulumi:Stack  pulumidemo-dev  created
 +   └─ aws:s3:Bucket     my-bucket       created

Outputs:
    bucketName: "my-bucket-68e33ec"

Resources:
    + 2 created

Duration: 14s

```

  6. If you want to make changes in your program you can do & then you have to again use command `pulumi up` to deploy those changes.
  7. Destroy the stack: Now that you’ve seen how to deploy changes to our program, let’s clean up the resources that are part of your stack.
  To destroy resources, run the following:
  `pulumi destroy`
  You’ll be prompted to make sure you really want to delete these resources. This can take a minute or two; Pulumi waits until all resources are shut down and deleted before it considers the destroy operation to be complete. 

  

    