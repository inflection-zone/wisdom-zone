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
