# ECS CI/CD Workflow Using GitHub Actions

## Prerequisites
1. GitHub Account

---

Click [GitHub](https://github.com/inflection-sahil/reancare/blob/master/.github/workflows/ecs-ci-cd.yml) for ECS CI/CD Workflow.

## Steps:
1. Create a GitHub repository.
2. Add your project files and folders to the repository.
2. Create *.github* folder in project directory.
3. Inside it, create a */workflows* folder.
4. Create *ecs-ci-cd.yml* file and store it in above-created *.github/workflows* directory.
5. Define the **`name`** and following map of **`env`** variables:
    - AWS_REGION
    - ROLE_TO_ASSUME
    - ECR_REGISTRY_URI
    - ECR_REPOSITORY_NAME
    - ECR_IMAGE_TAG
    - ECS_CLUSTER_NAME
    - ECS_SERVICE_NAME
    - ECS_TASK_DEFINITION_FAMILY_NAME
    - ECS_TASK_DEFINITION
    - ECS_CONTAINER_NAME
6. Define the **`on`** to set which events can cause the workflow to run.
7. Define the following **`actions`** to build & push i.e **Continuous Integration (CI)**:
    - Checkout the repo
        - actions/checkout@v4
    - Configure the AWS credentials
        - aws-actions/configure-aws-credentials@v4
    - Login to Amazon ECR
        - aws-actions/amazon-ecr-login@v2
    - Build and push the image
        - docker/build-push-action@v5
8. Define the following **`actions`** to deploy the container i.e **Continuous Deployment (CD)**:
    - Run the following to download the task definition
        - aws ecs describe-task-definition --task-definition ${{ env.ECS_TASK_DEFINITION_FAMILY }} \
        --query taskDefinition > task-definition.json
    - Fill in the new image ID in the Amazon ECS task definition
        - aws-actions/amazon-ecs-render-task-definition@v1
    - Deploy Amazon ECS task definition
        - aws-actions/amazon-ecs-deploy-task-definition@v2

---