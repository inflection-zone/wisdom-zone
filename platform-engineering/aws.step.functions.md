# Automating EC2 Instance Management with AWS Step Functions, EventBridge, and PM2

## Table of Contents

1. [Introduction](#introduction)
2. [Step Functions Setup](#step-functions-setup)
   - [Creating a State Machine](#creating-a-state-machine)
   - [Defining the Workflow](#defining-the-workflow)
   - [Triggering with EventBridge](#triggering-with-eventbridge)
3. [PM2 Configuration](#pm2-configuration)
   - [Saving the PM2 Process List](#saving-the-pm2-process-list)
   - [Setting Up PM2 to Start on Boot](#setting-up-pm2-to-start-on-boot)
   - [Verifying PM2 Setup](#verifying-pm2-setup)
4. [Handling Dynamic IPs with Route 53 Using Elastic IPs](#handling-dynamic-ips-with-route-53-using-elastic-ips)
5. [Summary](#summary)

---

## Introduction

This document provides detailed steps to automate the management of your EC2 instances using AWS services like Step Functions and EventBridge, along with configuring PM2 to manage your services. It also covers how to handle dynamic IP addresses in Route 53.

## Step Functions Setup

### Creating a State Machine

1. **Open AWS Step Functions Console:**
   - Navigate to the AWS Management Console and select "Step Functions."

2. **Create a New State Machine:**
   - Click on "Create state machine."
   - Choose either "Design your workflow visually" or "Write your workflow in code (JSON)."
   - Select the "Standard" type.

3. **Create an IAM Role:**
   - During the state machine creation process, AWS will prompt you to create a new IAM role or use an existing one.
   - If you create a new role, note the role name.

4. **Add Required Permissions to the IAM Role:**
   - Go to the [IAM Console](https://console.aws.amazon.com/iam/).
   - In the navigation pane, choose "Roles."
   - Search for the IAM role created by Step Functions.
   - Select the role and click on "Add permissions."
   - Choose "Attach policies" and search for the following policies:
     - `AmazonEC2FullAccess` (or you can use a custom policy with specific permissions):
       ```json
       {
         "Version": "2012-10-17",
         "Statement": [
           {
             "Effect": "Allow",
             "Action": [
               "ec2:StartInstances",
               "ec2:StopInstances"
             ],
             "Resource": "*"
           }
         ]
       }
       ```
   - Attach the selected policy to the role.

### Defining the Workflow

The following is a sample workflow to stop and start EC2 instances:

```json
{
  "StartAt": "StopInstances",
  "States": {
    "StopInstances": {
      "Type": "Task",
      "Resource": "arn:aws:states:::aws-sdk:ec2:stopInstances",
      "Parameters": {
        "InstanceIds": ["i-1234567890abcdef0", "i-0987654321fedcba9"]
      },
      "Next": "WaitUntilMorning"
    },
    "WaitUntilMorning": {
      "Type": "Wait",
      "Seconds": 43200,
      "Next": "StartInstances"
    },
    "StartInstances": {
      "Type": "Task",
      "Resource": "arn:aws:states:::aws-sdk:ec2:startInstances",
      "Parameters": {
        "InstanceIds": ["i-1234567890abcdef0", "i-0987654321fedcba9"]
      },
      "End": true
    }
  }
}
```

### Triggering with EventBridge

1. **Open EventBridge Console:**
   - Go to the AWS EventBridge console.

2. **Create a New Rule:**
   - Set the event source to "Schedule."
   - Use a cron expression (e.g., `cron(0 23 * * ? *)` for 11 PM daily).

3. **Set the Target:**
   - Choose "Step Functions state machine" as the target.
   - Select the state machine you created earlier.

4. **Save the Rule:**
   - Review and save the rule.

## PM2 Configuration

### Saving the PM2 Process List

1. **Save the Process List:**
   - Run the following command to save the current PM2 processes:
   ```bash
   pm2 save
   ```

### Setting Up PM2 to Start on Boot

1. **Generate the Startup Script:**
   - Run:
   ```bash
   pm2 startup
   ```
   - Execute the output command to set up PM2 to start on boot.

2. **Save the Process List Again:**
   - Ensure the saved process list is loaded on startup:
   ```bash
   pm2 save
   ```

### Verifying PM2 Setup

1. **Reboot the Instance:**
   ```bash
   sudo reboot
   ```

2. **Check PM2 Status After Reboot:**
   ```bash
   pm2 status
   ```

## Handling Dynamic IPs with Route 53 Using Elastic IPs

1. **Allocate an Elastic IP:**
   - Go to the EC2 Console and allocate a new Elastic IP.

2. **Associate the Elastic IP:**
   - Associate the Elastic IP with your EC2 instance.

3. **Update Route 53:**
   - Point your Route 53 records to the Elastic IP.

## Summary

This guide provides a complete walkthrough for automating the management of EC2 instances, ensuring PM2 services start correctly, and managing dynamic IPs in Route 53. By following these steps, you can minimize manual intervention and ensure a smooth operation of your services.