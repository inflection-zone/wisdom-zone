# What is Cloud Computing

- Cloud computing is on demand delivery of IT resources (compute, storage, application) through cloud services platform (AWS, Azure, GCP etc) via internet with pay as you go pricing.
- Cloud computing provides a simple way to access servers, storage, databases & set of application services over the internet.

# Why Cloud Computing

- Before cloud, companies were having their own onpremises physical datacenters.
- For those datacenters, companies needed space, physical servers, networking hardwares, resources like network engineer, OS engineer, datacenter admin, database engineer, etc. And companies have to manage all these resources on their own. In short companies needed to invest lot of money & energy to establish physical datacenters.
- With cloud, instead of buying, owning, and maintaining physical data centers and servers, we can access technology services, such as computing power, storage, and databases, on an as-needed basis from a cloud provider like Amazon Web Services (AWS).
- Here are some reasons for which companies nowadays turning to cloud computing services.
  1. **Cost**: Cloud computing eliminates capital expense of buying hardware, setting up & running on-premises datacenters.
  2. **Speed**: Most cloud computing services provides self-service & on-demand. So even large number of comuting resources are provisioned in minutes, with just some mouse clicks.
  3. **Scalability**: The benefits of cloud computing services include the ability to scale elastically. In cloud speak, that means delivering the right amount of IT resources.
  4. **Productivity**: On-premises datacenters require a lot of "racking & stacking"- hardware set-up, software patching & many other time consuming IT management chores. Cloud computing removes the need for many of these tasks. So IT teams can spend time on achieving more important business goals.
  5. **Performance**: The cloud computing services run on a worldwide network of secure datcenters, which are regularly upgraded to the latest generation of fast & efficient computing hardware. This gives several benefits over a single corporate datacenter, including reduced network latency.
  6. **Reliablity**: Cloud computing makes data backup, disaster recovery & business continuity easier & less expensive, because data can be mirrored at multiple sites on the cloud provider's network.

# Types of Cloud Computing

- Cloud computing provides developers and IT departments with the ability to focus on what matters most and avoid undifferentiated work such as procurement, maintenance, and capacity planning.
- Each type of cloud service and deployment method provides you with different levels of control, flexibility, and management.
- **Cloud Computing Models**: 1. **Infrastructure as a Service (IaaS)**: Infrastructure as a Service (IaaS) contains the basic building blocks for cloud IT and typically provides access to networking features, computers (virtual or on dedicated hardware), and data storage space. IaaS provides you with the highest level of flexibility and management control over your IT resources and is most similar to existing IT resources that many IT departments and developers are familiar with today. 2. **Platform as a Service (PaaS)**: Platform as a Service (PaaS) removes the need for your organization to manage the underlying infrastructure (usually hardware and operating systems) and allows you to focus on the deployment and management of your applications. This helps you be more efficient as you don’t need to worry about resource procurement, capacity planning, software maintenance, patching, or any of the other undifferentiated heavy lifting involved in running your application. 3. **Software as a Service (SaaS)**: Software as a Service (SaaS) provides you with a completed product that is run and managed by the service provider. In most cases, people referring to Software as a Service are referring to end-user applications. With a SaaS offering you do not have to think about how the service is maintained or how the underlying infrastructure is managed; you only need to think about how you will use that particular piece of software.
  &nbsp;<br>
  <img src="service model.png" width="900" height="400"/>

&nbsp;<br>

- **Cloud Computing Deploying Models**:
  1. **Cloud** : A cloud-based application is fully deployed in the cloud and all parts of the application run in the cloud. Applications in the cloud have either been created in the cloud or have been migrated from an existing infrastructure to take advantage of the benefits of cloud computing.
  2. **Hybrid** : A hybrid deployment is a way to connect infrastructure and applications between cloud-based resources and existing resources that are not located in the cloud. The most common method of hybrid deployment is between the cloud and existing on-premises infrastructure to extend, and grow, an organization's infrastructure into the cloud while connecting cloud resources to the internal system.
  3. **On-premises** : The deployment of resources on-premises, using virtualization and resource management tools, is sometimes called the “private cloud”. On-premises deployment doesn’t provide many of the benefits of cloud computing but is sometimes sought for its ability to provide dedicated resources.

# Global Infrastructure

- The AWS Cloud infrastructure is built around AWS Regions and Availability Zones.
- An AWS Region is a physical location in the world where we have multiple Availability Zones.
- Availability Zones consist of one or more discrete data centers, each with redundant power, networking, and connectivity, housed in separate facilities.
- These Availability Zones offer you the ability to operate production applications and databases that are more highly available, fault tolerant, and scalable than would be possible from a single data center.
- The AWS Cloud spans 96 Availability Zones within 30 geographic regions around the world.

# Amazon EC2

- Amazon Elastic Compute Cloud (Amazon EC2) provides scalable computing capacity in the AWS Cloud.
- You can use Amazon EC2 to launch as many or as few virtual servers as you need, configure security and networking, and manage storage.
- Amazon EC2 enables you to scale up or down to handle changes in requirements or spikes in popularity, reducing your need to forecast traffic.
- Amazon EC2 provides the following features:
  - Virtual computing environments, known as instances
  - Preconfigured templates for your instances, known as Amazon Machine Images (AMIs).
  - Various configurations of CPU, memory, storage, and networking capacity for your instances, known as instance types.
  - Secure login information for your instances using key pairs
  - Temporary storage volumes
  - Persistent storage volumes for your data using Amazon Elastic Block Store (Amazon EBS), known as Amazon EBS volumes
  - Multiple physical locations for your resources, known as Regions and Availability Zones
  - A firewall that enables you to specify the protocols, ports, and source IP ranges that can reach your instances using security groups
  - Static IPv4 addresses for dynamic cloud computing, known as Elastic IP addresses
  - Metadata, known as tags, that you can create and assign to your Amazon EC2 resources
  - Virtual networks you can create that are logically isolated from the rest of the AWS Cloud, and that you can optionally connect to your own network, known as virtual private clouds(VPC).
- Steps to create Amazon EC2 instance:

  1. Login to AWS management console as a root user.
  2. We can see following screen. Select desired region. Then click on "Services" tab to browse AWS services.
     <img src="EC2-1.png" width="900" height="300"/>
     &nbsp;<br>
  3. Select EC2 service. On the next screen, select instances. Then following screen appears. Click on "Launch Instances"
     <img src="EC2-2.png" width="900" height="300"/>
     &nbsp;<br>
  4. On the next screen, we have to give desired specifications for our instance. Give any name you want, then select AMI (Amazon machine image - OS for our instance). Note- If you are using free tier account, select free tier eligible AMI.
     <img src="EC2-3.png" width="900" height="300"/>
     &nbsp;<br>
  5. Then select right instance type. It is nothing but the CPU & RAM configurations. Then for key-pair (required for login into instance), click on "Create new key-pair".
     <img src="EC2-4.png" width="900" height="300"/>
     &nbsp;<br>
  6. In network settings, select desired VPC (here, we are using AWS default VPC), then subnet (It is nothing but the availability zone. In Mumbai region, there are 3 subnets, you may select any of them or if you give no prference, AWS decides where to launch your instance), enable auto-assign public IP.
     <img src="EC2-5.png" width="900" height="300"/>
     &nbsp;<br>
  7. Then set firewall (security group). Click on "Create new security group". Give it a name & description. Then add rule. (Here we are creating Linux instance, so we are opening SSH port no.22 because we will remotely access our linux instance through ssh. For windows instance, you need to add RDP rule in this section). We may add more than one rule to this section. In source type there are 3 options- anywhere, custom & my ip. (If you select anywhere, it means anyone from anywhere can access your instance. With custom, we may specify any custom IP to access instance. With 'my ip', instance can only be accessed by your IP address).
     <img src="EC2-6.png" width="900" height="300"/>
     &nbsp;<br>
  8. Add storage. For free tier, it is providing 8Gb storage. If you want more you may increase it or you may add more volumes to it.
  9. Click on "Launch instance".
  10. Instance will get ready in few seconds. Click on "View all instances". You may see your instance running.
      <img src="EC2-7.png" width="900" height="300"/>
      &nbsp;<br>

- Steps to access EC2 instance with Mobaxterm:

  1.  Download & install Mobaxterm.(https://download.mobatek.net/2222022102210348/MobaXterm_Portable_v22.2.zip)
  2.  Go to AWS EC2. Slect running instance. Click on "Details". We can see here our instance has got two IPs - public IP & private IP.
      <img src="EC2-8.png" width="900" height="300"/>
      &nbsp;<br>
  3.  Copy public IP of the instance. Go to Mobaxterm. Click on "Session" to start new session. Then click on "SSH". Paste copied public IP in "Host" field. Login as "ec2-user". Then click on "Advanced SSH Settings". Use private key you have created. Click on "Ok".
      <img src="EC2-9.png" width="900" height="300"/>
      &nbsp;<br>
  4.  Now you are logged in into your instance. You can now access your instance.
      <img src="EC2-10.png" width="900" height="300"/>
      &nbsp;<br>

- Steps to create & access windows instance:

  1. Go to EC2 service. Click on "Launch instances". Give name to your Instance. Select windows AMI (Free tier eligible).
     <img src="EC2-11.png" width="900" height="300"/>
     &nbsp;<br>

  2. Select instance type (Free tier eligible). Then select previously created key-pair or create new. (Note: You may use single key-pair for maximum 500 instances.)
     <img src="EC2-12.png" width="900" height="300"/>
     &nbsp;<br>
  3. In network settings, as we done with linux instance, select AWS default VPC, select subnet, enable public IP.
  4. To set firewall (i.e. security group), select type RDP, because we access windows instance through rdp client port no. 3389.
     <img src="EC2-13.png" width="900" height="300"/>
     &nbsp;<br>

  5. Configure storage. And then click on "Launch instance".
  6. Select instance & click on "connect".
     <img src="EC2-14.png" width="800" height="250"/>
     &nbsp;<br>
  7. Then select RDP Client. Then "Download remote desktop file". Click on "Get password".
     <img src="EC2-15.png" width="900" height="300"/>
     &nbsp;<br>
  8. It opens following window. Click on "Upload private key file".
     <img src="EC2-16.png" width="900" height="300"/>
     &nbsp;<br>
  9. Upload key-pair we have created. Then click on "Decrypt password". Then we will get password to login into our instance. Copy that password.
     <img src="EC2-17.png" width="900" height="300"/>
     &nbsp;<br>
  10. Open downloaded RDP client & click on "Connect".
      <img src="EC2-18.png" width="800" height="250"/>
      &nbsp;<br>
  11. Then paste the copied password. Click on "OK". Then click on "Yes". You are logged into your windows instance.

- Steps to install webserver on linux instance:

  1. Go to EC2 service. Click on "Launce instances".
  2. Give name to instance. Select amazon linux AMI. Then select right instance type. Select previously created key-pair.
  3. In network settings, select AWS default VPC, subnet, enable auto assign public IP. Then in security group, we have to add "HTTP" rule, as we are deploying webserver & we will see the webpage in web browser.
     <img src="EC2-20.png" width="800" height="250"/>
     &nbsp;<br>
  4. Then configure storage as per your requirement. Go to Advanced details. Scroll down & you will see "User data" section at the bottom. Add following script to it.
     ```
     #!/bin/bash
     sudo su -
     yum install httpd -y
     echo "welcome to pune" >/var/www/html/index.html
     service httpd start
     chkconfig httpd on
     ```
     <img src="EC2-21.png" width="800" height="250"/>
     &nbsp;<br>
  5. Click on "Launch instance". Click on "View all instances". Select instance & copy it's public IP address. Paste it in browser & you will see the message.
     <img src="EC2-22.png" width="800" height="250"/>
     &nbsp;<br>

- **Instance Types**: Amazon EC2 provides a wide selection of instance types optimized to fit different use cases. Instance types comprise varying combinations of CPU, memory, storage, and networking capacity and give you the flexibility to choose the appropriate mix of resources for your applications. Each instance type includes one or more instance sizes, allowing you to scale your resources to the requirements of your target workload.

  1.  **General Purpose**: General purpose instances provide a balance of compute, memory and networking resources and can be used for a variety of workloads. These instances are ideal for applications that use these resources in equal proportions such as web servers and code repositories.
  2.  **Compute Optimized**: Compute Optimized instances are ideal for compute bound applications that benefit from high performance processors. Instances belonging to this family are well suited for batch processing workloads, media transcoding, high performance web servers, high performance computing (HPC), scientific modeling, dedicated gaming servers and other compute intensive applications.
  3.  **Memory Optimized**: Memory optimized instances are designed to deliver fast performance for workloads that process large data sets in memory.
  4.  **Accelerated Computing**: Accelerated computing instances use hardware accelerators, or co-processors, to perform functions, such as floating point number calculations, graphics processing, or data pattern matching, more efficiently than is possible in software running on CPUs.
  5.  **Storage Optimized**: Storage optimized instances are designed for workloads that require high, sequential read and write access to very large data sets on local storage. They are optimized to deliver tens of thousands of low-latency, random I/O operations per second (IOPS) to applications.

- **Instance purchasing options**:
  1.  On-Demand Instances: With On-Demand Instances, you pay for compute capacity by the second with no long-term commitments. You have full control over its lifecycle—you decide when to launch, stop, hibernate, start, reboot, or terminate it. We should use On-Demand Instances for applications with short-term, irregular workloads that cannot be interrupted.
  2.  Reserved Instances: Reserved Instances provide you with significant savings on your Amazon EC2 costs compared to On-Demand Instance pricing. Resrved instances give you dedicated hypervisers. You can purchase a Reserved Instance for a one-year or three-year commitment. The following payment options are available for Reserved Instances:
      - All Upfront: Full payment is made at the start of the term, with no other costs or additional hourly charges incurred for the remainder of the term, regardless of hours used.
      - Partial Upfront: A portion of the cost must be paid upfront and the remaining hours in the term are billed at a discounted hourly rate, regardless of whether the Reserved Instance is being used.
      - No Upfront: You are billed a discounted hourly rate for every hour within the term, regardless of whether the Reserved Instance is being used. No upfront payment is required.
  3.  Spot Instances: A Spot Instance is an instance that uses spare EC2 capacity that is available for less than the On-Demand price. Because Spot Instances enable you to request unused EC2 instances at steep discounts, you can lower your Amazon EC2 costs significantly. The hourly price for a Spot Instance is called a Spot price. Spot Instances are a cost-effective choice if you can be flexible about when your applications run and if your applications can be interrupted. For example, Spot Instances are well-suited for data analysis, batch jobs, background processing, and optional tasks.
  4.  Dedicated Hosts: An Amazon EC2 Dedicated Host is a physical server with EC2 instance capacity fully dedicated to your use. Dedicated Hosts allow you to use your existing per-socket, per-core, or per-VM software licenses, including Windows Server, Microsoft SQL Server, SUSE, and Linux Enterprise Server.

# Amazon EBS (Elastic Block Storage):

- Amazon Elastic Block Store (Amazon EBS) provides block level storage volumes for use with EC2 instances. EBS volumes are raw, unformatted block devices. You can mount these volumes as devices on your instances.
- EBS volumes that are attached to an instance are exposed as storage volumes that persist independently from the life of the instance. You can create a file system on top of these volumes, or use them in any way you would use a block device (such as a hard drive).
- You can dynamically change the configuration of a volume attached to an instance.
- Amazon EBS can be used for data that must be quickly accessible and requires long-term persistence. EBS volumes are particularly well-suited for use as the primary storage for file systems, databases, or for any applications that require fine granular updates and access to raw, unformatted, block-level storage.
- Amazon EBS is well suited to both database-style applications that rely on random reads and writes, and to throughput-intensive applications that perform long, continuous reads and writes.
