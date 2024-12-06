# Azure Terraform Modules

Create the **azure-modules** directory.

The folder structure for the above-created directory is as follows:

```
azure-modules
├───acr
│       main.tf
│       outputs.tf
│       variables.tf
│
├───aks
│       main.tf
│       variables.tf
│
├───container-apps
│       main.tf
│       outputs.tf
│       variables.tf
│
├───mysql-flexible
│       main.tf
│       outputs.tf
│       variables.tf
│
├───resource-group
│       main.tf
│       variables.tf
│
└───virtual-network
        main.tf
        outputs.tf
        variables.tf
```

---

## Resource Group Module
Let's start with the Resource Group Module.
1. Create a *resource-group* folder inside the above-created directory.
2. Inside *resource-group* folder, create *main.tf* file.
3. Define the following resources:
    - azurerm_resource_group
4. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/resource-group/main.tf) for reference.
5. The definition of *main.tf* file has been completed.
6. Now we will create *variables.tf* file for declaring variables.
7. Inside it, declare the following variables:
    - resource-group-properties
8. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/resource-group/variables.tf) for reference.
9. We have completed defining the **Resource Group Module**.

---

## VNet Module
Now, let's create a Virtual Network module.
1. Create a *vnet* folder inside the above-created directory.
2. Inside *vnet* folder, create *main.tf* file.
3. Define the following resources:
    - azurerm_virtual_network
4. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/virtual-network/main.tf) for reference.
5. The definition of *main.tf* file is completed.
6. Now we will create *variables.tf* file for declaring variables.
7. Inside it, declare the following variables:
    - resource-group-properties
    - virtual-network-properties
8. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/virtual-network/variables.tf) for reference.
9. We have completed declaring *variables.tf* file for the *VNet module*.
10. Now we will declare outputs for the *VNet module*.
11. Create *outputs.tf* file and add the following outputs:
    - azurerm_virtual_network.vnet.id
    - azurerm_virtual_network.vnet.name
12. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/virtual-network/outputs.tf) for reference.
13. Now we have completed defining the **VNet Module**.

---

## ACR Module
We will use Azure Container Registry for storing container image.
1. Create *acr* folder inside the above-created *azure-modules* directory.
2. Inside *acr* folder, create *main.tf* file and define the following resources:
    - azurerm_container_registry
3. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/acr/main.tf) for reference.
4. The definition of *main.tf* file is complete.
5. Now we will create *variables.tf* file.
6. Inside it, declare the following variables:
    - resource-group-properties
    - acr-properties
7. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/acr/variables.tf) for reference.
8. Variables have been declared.
9. Now create the *outputs.tf* file and define the following outputs:
    - acr-id
    - acr-name
    - acr-login-server
10. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/acr/outputs.tf) for reference.
11. We have completed defining the **ACR Module**.

## MySQL Flexible Module
For the database, we will use Azure MySQL Flexible.
1. Create *mysql-flexible* folder inside the *azure-modules* directory.
2. Inside *mysql-flexible* folder, create *main.tf* file and define the following resources:
    - azurerm_subnet
    - azurerm_private_dns_zone
    - azurerm_private_dns_zone_virtual_network_link
    - azurerm_mysql_flexible_server
    - azurerm_mysql_flexible_database
3. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/mysql-flexible/main.tf) for reference.
4. The definition of *main.tf* file is complete.
5. Now we will create *variables.tf* file and declare the following variables:
    - resource-group-properties
    - mysql-flexible-properties
    - vnet-id
    - vnet-name
6. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/mysql-flexible/variables.tf) for reference.
7. Variables have been declared.
8. Now create the *outputs.tf* file and define the following outputs:
    - DB_HOST
9. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/mysql-flexible/outputs.tf) for reference.
10. We have completed defining the **MySQL Flexible Module**.

---
## Storage Module
Let's start with the Storage Module
1. Create *storage* folder in the above-created *azure-modules* directory.
2. Inside it, create *main.tf* file and define the following resources:
    - azurerm_storage_account
    - azurerm_storage_container
    - azurerm_storage_blob
3. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/storage/main.tf) for reference.
4. The definition of *main.tf* file for *Storage Module* is complete.
5. Now create *variables.tf* file and declare the following variables:
    - resource-group-properties
    - storage-properties
    - vnet-public-subnet-id
6. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/storage/variables.tf) for reference.
7. Variables have been declared.
8. The definition of **Storage Module** is complete.

---

## Container Apps Module
Let's start with the Container Apps Module.
1. Create *container-apps* folder in the above-created *azure-modules* directory.
2. Inside it, create *main.tf* file and define the following resources:
    - azurerm_container-registry_scope_map
    - azurerm_container_registry_token
    - azurerm_container_registry_token_password
    - azurerm_log_analytics_workspace
    - azurerm_container_app_environment
    - azurerm_container_app
3. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/container-apps/main.tf) for reference.
4. The definition of *main.tf* file for *Container Apps* is complete.
5. Now create *variables.tf* file and declare the following variables:
    - resource-group-properties
    - container-apps-properties
    - vnet-public-subnet-id
    - acr-id
    - acr-name
6. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/container-apps/variables.tf) for reference.
7. Variables have been declared.
8. Now create the *outputs.tf* file and define the following outputs:
    - container-apps-url
9. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/container-apps/outputs.tf) for reference.
10. The definition of **Container Apps Module** is complete.

---

## AKS Module
Let's start with the AKS Module.
1. Create the *aks* folder in the *azure-modules* directory.
2. Inside it, create a *main.tf* file and define the following resources:
    - azurerm_subnet
    - azurerm_kubernetes_cluster
3. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/aks/main.tf) for reference.
4. The *main.tf* file for AKS has been defined.
5. Now we will create *variables.tf* file and declare the following variables:
    - resource-group-properties
    - aks-properties
    - vnet-name
6. Click [code](https://github.com/sahilphule/templates/blob/master/terraform/modules/azure/aks/variables.tf) for reference.
7. We have completed defining the **AKS Module**.

---