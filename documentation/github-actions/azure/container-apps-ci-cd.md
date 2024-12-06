# Container Apps CI/CD Workflow Using GitHub Actions

## Prerequisites
1. GitHub Account

---

Click [GitHub](https://github.com/inflection-sahil/reancare/blob/master/.github/workflows/container-apps-ci-cd.yml) for Container Apps CI/CD Workflow.

## Steps:
1. Create a GitHub repository.
2. Add your project files and folders to the repository.
2. Create *.github* folder in project directory.
3. Inside it, create a */workflows* folder.
4. Create *container-apps-ci-cd.yml* file and store it in above-created *.github/workflows* directory.
5. Define the **`name`** and following map of **`env`** variables:
    - ACR_LOGIN_SERVER
    - ACR_NAMESPACE
    - ACR_REPOSITORY_NAME
    - ACR_IMAGE_TAG
    - RESOURCE_GROUP_NAME
    - CONTAINER_APP_ENVIRONMENT_NAME
    - CONTAINER_APP_NAME
6. Define the **`on`** to set which events can cause the workflow to run.
7. Define the following **`actions`** to build & push i.e **Continuous Integration (CI)**:
    - Checkout the repo
        - actions/checkout@v4
    - Login to ACR
        - azure/docker-login@v2
    - Build and push the image
        - docker/build-push-action@v5
8. Define the following **`actions`** to deploy the container i.e **Continuous Deployment (CD)**:
    - Azure login
        - azure/login@v2
    - Deploy Container Apps
        - azure/container-apps-deploy-action@v1

---