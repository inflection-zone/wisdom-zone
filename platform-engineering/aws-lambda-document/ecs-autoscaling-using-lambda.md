# Scaling an ECS Services Using a Scheduled AWS Lambda Function in DuploCloud

This document outlines the process of creating a Python script that automatically scales an ECS services in DuploCloud. It covers deploying the script as an AWS Lambda function and scheduling it using AWS EventBridge.

---

## **1. Prerequisites**
Ensure you have the following:
- A **DuploCloud API token** for authentication. If you don't have one, you can follow stps mentioned [here](./generate-duplo-api-token.md)
- Your **Tenant ID** in DuploCloud.
- The **ECS service name** you want to scale.
- AWS CLI configured with necessary permissions.
- Python 3.x installed.

---

## **2. Store Secrets in AWS Secrets Manager**
Store credentials securely in **AWS Secrets Manager**.

### **Step 1: Create a Secret**
Run the following command to create a secret with your **DuploCloud API token** and **Tenant ID**:

```sh
aws secretsmanager create-secret --name DuploCloudSecrets \
    --secret-string '{"DUPLO_TOKEN":"your_duplocloud_token","DUPLO_ID":"your_tenant_id"}'
```
Or you may also use AWS Console to store secrets in secret manager.

---

## **3. Install Required Dependencies**
- Add required dependencies such as `boto3`, `duplocloud-client` in `requirements.txt` file.
- Install them:
```sh
pip install -r requirements.txt -t .
```

---

## **4. Create the Python Script**
Create a Python script (`app.py`) that:
- **Fetches credentials** from **AWS Secrets Manager**.
- **Retrieves the current replica count** of the ECS service.
- **Updates the replica count and ECS service**

```python
import os
import boto3
import json
from duplocloud.client import DuploClient

secrets_client = boto3.client('secretsmanager')

def get_secret(secret_name):
    print("Inside get_secret function...")
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        raise

def toggle_replicas(duplo_token, duplo_id, service_names):

    print("Inside toggle_replicas function...")

    duplo_host = "https://abc.duplocloud.net"

    client = DuploClient(duplo_host, duplo_token, tenant_id=duplo_id)

    try:
        all_services = client.load("ecs")
        print("All Services: ", all_services)

        for service_name in service_names:

            ecs_service = all_services.find(service_name)
            print("ECS Service: ", ecs_service)

            replicas = ecs_service['Replicas']
            print("Replica Count: ", replicas)

            if replicas > 0:
                ecs_service['Replicas'] = 0
            else:
                ecs_service['Replicas'] = 1

            all_services.update(ecs_service)

            print("ECS Service: ", ecs_service)

    except Exception as e:
        print(f"Error toggling replicas: {e}")
        raise

def lambda_handler(event, context):

    secret_name = "DuploCloudLambdaSecrets"
    service_names = ["service-1", "service-2", "service-3", "service-4", "service-5"]

    try:
        secrets = get_secret(secret_name)
        duplo_token = secrets.get("DUPLO_TOKEN")
        duplo_id = secrets.get("DUPLO_ID")

        if not duplo_token or not duplo_id:
            raise ValueError("Missing DUPLO_TOKEN or TENANT_URL in secrets.")

        toggle_replicas(duplo_token, duplo_id, service_names)

    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error toggling ECS service replicas.", "error": str(e)})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Successfully toggled ECS service replicas."})
    }
```

---

## **5. Package the Lambda Function**
Before deploying, zip the function using `winzip` tool.

---

## **6. Upload to S3**
Upload the zipped Lambda function to AWS S3 bucket.

## **7. Deploy as an AWS Lambda Function**
- Go to DuploCloud Console.
- Navigate to `Cloud Services` > `Serverless` > `Lambda`.
- Click `Add` to create new function.
- Provide:
    - Name: LambdaTest
    - Description: LambdaTest
    - Package Type: zip
    - Runtime: Python 3.12
    - Memory: 128 MB
    - Ephemeral Storage: 512 MB
    - Timeout: 120 seconds
    - Function Handler: app.lambda_handler
    - Environment Variables: Provide if any
    - S3 Bucket: Bucket name
    - Function Package: lambda.zip
- Click `Submit`.

---

## **8. Assign IAM Permissions**
### **Step 1: Attach AWS Secrets Manager Permission to Lambda**
Ensure the Lambda function's IAM role has **Secrets Manager read access** (`secretsmanager:GetSecretValue`).

Attach the following **IAM policy** to your **Lambda role**:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "secretsmanager:GetSecretValue",
            "Resource": "arn:aws:secretsmanager:YOUR_AWS_REGION:YOUR_ACCOUNT_ID:secret:DuploCloudSecrets"
        }
    ]
}
```

---

## **9. Schedule the Function Using AWS EventBridge**
### **Step 1: Open AWS EventBridge**
1. Sign in to the **AWS Console**.
2. Navigate to **Amazon EventBridge** → **Schedules**.
3. Click **Create schedule**.

### **Step 2: Define the Schedule**
1. Enter a **Schedule name**: `LambdaTestSchedule`.
2. Choose **Cron Expression**:
   - **Schedule:** `cron(0 23,8 * * ? *)`

### **Step 3: Add Target**
1. Under **Select Targets**, choose **AWS Lambda Function**.
2. Select the **Lambda function**: `LambdaTest`.
3. Click **Create Schedule**.

---

## **10. Testing the Setup**

### **1. Open AWS Lambda Console**
1. Sign in to **AWS Management Console**.
2. Navigate to **AWS Lambda**.
3. Click on your function **`LambdaTest`**.

### **2. Create a Test Event**
1. In the **Test** tab, click **"Test"**.
2. Click **"Create new test event"**.
3. **Event Name:** `test-scaling`
4. Leave the **event JSON** as:
   ```json
   {}
   ```
5. Click **Create**.

### **3. Execute the Test**
1. Click **"Test"**.
2. AWS Lambda **executes the function** and displays the output.

---

## **Conclusion**
✅ **Lambda function dynamically scales ECS services as scheduled via AWS EventBridge to run at 11 PM & 8 AM Local Time Zone**


