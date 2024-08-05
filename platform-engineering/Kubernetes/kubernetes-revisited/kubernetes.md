# Kubernetes Overview

## Table of Contents
1. [Introduction to Kubernetes](#introduction-to-kubernetes)
2. [Kubernetes Architecture](#kubernetes-architecture)
   - [Master Components](#master-components)
   - [Node Components](#node-components)
3. [Kubernetes Objects](#kubernetes-objects)
   - [Pods](#pods)
   - [ReplicaSets](#replicasets)
   - [Deployments](#deployments)
   - [Services](#services)

---

## Introduction to Kubernetes

Kubernetes (often abbreviated as K8s) is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications. Originally developed by Google, Kubernetes is now maintained by the Cloud Native Computing Foundation (CNCF).

Key features of Kubernetes:
- **Self-healing**
- **Horizontal scaling**
- **Service discovery and load balancing**
- **Automated rollouts and rollbacks**
- **Secret and configuration management**

## Kubernetes Architecture

Kubernetes follows a master-worker architecture.

### Master Components

1. **API Server**:
   - Serves as the frontend for the Kubernetes control plane.
   - Exposes the Kubernetes API, which is the primary entry point for the system.

2. **etcd**:
   - A consistent and highly-available key-value store used as Kubernetes' backing store for all cluster data.

3. **Controller Manager**:
   - Manages various controllers, including the Node Controller, Replication Controller, and others.
   - Controllers are the components of Kubernetes which ensure thet the actusl state of cluster is same as the desired state.

4. **Scheduler**:
   - Assigns workloads (Pods) to nodes in the cluster based on resource availability and other constraints.

### Node Components

1. **Kubelet**:
   - An agent running on each node that ensures containers are running in a Pod as defined in the PodSpec.

2. **Kube-Proxy**:
   - A network proxy that runs on each node and manages network rules for communication to Pods from inside or outside the cluster.

3. **Container Runtime**:
   - The underlying software responsible for running containers, e.g., Docker, containerd.

## Kubernetes Objects

### Pods
- The smallest deployable unit in Kubernetes.
- A Pod can contain one or more containers.
- All containers in a Pod share the same network namespace.

#### Example: Pod YAML

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
    - name: nginx
      image: nginx:1.21.6
      ports:
        - containerPort: 80
```

### ReplicaSets
- Ensures that a specified number of pod replicas are running at any given time.
- Automatically creates or deletes Pods to reach the desired state.

#### Example: ReplicaSet YAML

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-replicaset
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.21.6
          ports:
            - containerPort: 80
```

### Deployments
- A higher-level abstraction that manages ReplicaSets and provides declarative updates to applications.

#### Example: Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.21.6
          ports:
            - containerPort: 80
```

### Services
- An abstraction that defines a logical set of Pods and a policy by which to access them.
- Types: ClusterIP, NodePort, LoadBalancer.

#### Example: Service YAML (NodePort)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
      nodePort: 30001
  type: NodePort
```
