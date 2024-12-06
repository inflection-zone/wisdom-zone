# Problem Statement
### Control the EC2 instance state using AWS Step Functions, Lambda Functions, and EventBridge Scheduler.

---

## EC2 Instances
### Steps to create EC2 instance
- Click on launch instance.
- Select the desired machine image and keep everything default and launch it.
- Add a new tag to the instance to control the state via the Lambda Function.

## Lambda Function
### Steps to Create Lambda Function
- Click on the Create Lambda function.
- Specify Python as a runtime and IAM role with basic lambda permissions.
- Open the created role in IAM and manually attach the EC2FullAccess policy.
- Edit timeout in configuration settings of lambda functions to 5 mins.
- Write the lambda function to control the EC2 instance state.
- Click on *[code](https://github.com/sahilphule/quizstar-portal/blob/prod/aws/lambda.py)* for reference.
- Deploy the code and create the test event.
- Test the code and check whether the EC2 instance state changed.

## Step Functions
### Steps to Create State Machine
- Click on Create State Machine
- Use AWS Lambda Invoke action as an intermediate action.
- Set the Lambda Invoke action function name parameter to the Lambda function created above and save it.

## EventBridge Schedule
### Steps to Create EventBridge Schedule
- Click on Create Schedule.
- Select recurring schedule.
- Select a cron-based schedule.
- Specify the cron expression **`(0 7,23 ? * * *)`** to trigger job at 7:00 am and 23:00 pm every day.
- Choose the `Off` option for **Flexible Time Window**.
- Select the Step Functions as the target API and select the above-created state machine.
- Select **Action After Schedule** to `None`.
- Create a new IAM role for EventBridge Scheduler.

---

> ### The Event will be triggered at 7:00 am and 23:00 pm daily to start and stop the EC2 instance at a specific time.