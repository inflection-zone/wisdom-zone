# EKS CI/CD Workflow Using GitHub Actions

## Prerequisites
1. GitHub Account

---

Click [GitHub](https://github.com/inflection-sahil/reancare/blob/master/.github/workflows/eks-ci-cd.yml) for EKS CI/CD Workflow.

## Steps:
1. Create a GitHub repository.
2. Add your project files and folders to the repository.
2. Create *.github* folder in project directory.
3. Inside it, create a */workflows* folder.
4. Create *eks-ci-cd.yml* file and store it in above-created *.github/workflows* directory.
5. Define the **`name`** and following map of **`env`** variables:
    - AWS_REGION
    - ROLE_TO_ASSUME
    - ECR_REGISTRY_URI
    - ECR_REPOSITORY_NAME
    - ECR_IMAGE_TAG
    - EKS_CLUSTER_NAME
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
8. Run the following to deploy the pod i.e **Continuous Deployment (CD)**:
    - Update the kube config
        - aws eks update-kubeconfig --name ${{ env.EKS_CLUSTER_NAME }} --region ${{ env.AWS_REGION }}
    - Deploy to EKS
        - sed -i.bak "s|DOCKER_IMAGE|${{ env.ECR_REGISTRY_URI }}/${{ env.ECR_REPOSITORY_NAME }}: ${{ env.ECR_IMAGE_TAG }}|g" ./kubernetes/app/deployment.yml && \
        kubectl apply -f ./kubernetes/app/deployment.yml

---