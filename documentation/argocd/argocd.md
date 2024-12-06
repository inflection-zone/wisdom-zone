# ArgoCD
- Argo CD is implemented as a Kubernetes controller which continuously monitors running applications and compares the current, live state against the desired target state (as specified in the Git repo).
- It automates the deployment of the desired application states in the specified target environments.
- Any modifications made to the desired target state in the Git repo can be automatically applied and reflected in the specified target environments.
- A deployed application whose live state deviates from the target state is considered OutOfSync. 
- Argo CD reports & visualizes the differences, while providing facilities to automatically or manually sync the live state back to the desired target state.

---

## Features of ArgoCD
- ArgoCD works on **Pulling** mechanism.
- No need to give cluster access to every team member as manifests files are applied by ArgoCD thus enhancing security.
- Even if team member applies any changes manually, ArgoCD will override it to match **GitHub state as a desired state** thus keeping **GitHub as a single source of truth**.
- Also has functionality to rollback to previous commits if necessary.

---

## Installation and Steps to login
Follow this [*link*](https://argo-cd.readthedocs.io/en/stable/getting_started/) to install argo cd in the cluster.

---

## Application file
- Click on [*application.yml*](https://github.com/sahilphule/templates/kubernetesmodules/argocd/application.yml) for ArgoCD template.
- If the Git repository is private, create a secret containing GitHub Username and GitHub Password. Click [*secret.yml*](https://github.com/sahilphule/templates/kubernetesmodules/argocd/secret.yml) for reference.

---