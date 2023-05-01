# Install Lens Desktop

## System requirements
Before you proceed with Lens Desktop installation, verify that your system meets the system requirements.

### Hardware requirements
Minimum hardware requirements:

- 2 GHz or faster processor
- 1 GB of RAM
- 1 GB of disk space

### Platforms
Lens has been tested on the following platforms:

- macOS
- Windows
- Linux

### Install Lens Desktop on Windows
1. Download the [Lens Desktop installer](https://k8slens.dev/) for Windows.
2. Now run the `Lens-Setup-{version}.exe installer` to install Lens Desktop.
3. Open Lens Desktop. Here you need to activate Lens. Choose Lens ID if you already have a Lens ID or need to create one. Alternatively, you can select Activation Code to proceed with an air-gapped installation, if you have already set up an activation code.
    <img src="./Images/Lens-Id.png" width="600" height="250"/>
     &nbsp;<br>
4. Here are steps for new account creation on Lens:
    1. If you select Lens ID in previous step, on the next page, either log in or select **Create your Lens ID**. 
    <img src="./Images/Lens-Id-2.png" width="600" height="250"/>
    You will need to enter a username, password, and email. Alternatively, you can authenticate with a GitHub or Google account.
    <img src="./Images/Lens-Id-3.png" width="600" height="250"/>
     &nbsp;<br>

    2. Next, you need to verify your email, then select **Add Lens Subscription**. 
    <img src="./Images/verify-email-subscribe.png" width="600" height="250"/> 
     &nbsp;<br>

    3. Choose a Lens Personal or Lens Pro subscription. (A 30-day free trial of Lens Pro is available.)
    <img src="./Images/choose-sub.png" width="600" height="250"/> 
     &nbsp;<br> 

    4. Now you are ready to get started with Lens. Select **Open Lens Desktop** to open Lens. The application will check for updates, and then you’ll be ready to get started. 
    <img src="./Images/ready.png" width="600" height="250"/> 
     &nbsp;<br> 


### Add a Cluster
* Select the catalog icon in the upper right-hand corner. You may brows clusters here.
* Lens will search common directories for kubeconfig files. 
* you may already find some clusters listed,for example- local development clusters like minikube or docker-desktop.
* You can simply click on these clusters to connect to them with Lens.

    <img src="./Images/lens-clusters.png" width="600" height="280"/> 
     &nbsp;<br>

* To add a new cluster to the catalog, hover over the blue plus icon in the lower right-hand corner of the screen. You will have the option to add a kubeconfig directly or by syncing with a file.
<img src="./Images/lens-cluster-1.png" width="600" height="280"/> 
     &nbsp;<br>

     <img src="./Images/add-from-kubeconfig.png" width="600" height="280"/> 
     &nbsp;<br>


### Deploy Workloads

* In this tutorial, let's use `minikube` cluster. So select minikube from cluster's list. You may see the following screen.
<img src="./Images/add-minikube.png" width="600" height="280"/> 
     &nbsp;<br> 

* Here you may all information about cluster like its nodes, workloads, configs etc. Terminal is also provided in lens. Let's deploy some workloads. We have already created [manifests](./manifests/). 
* To deploy these manifests, open terminal of lens and move to folder containing manifests. 
<img src="./Images/manifests.png" width="600" height="280"/> 
     &nbsp;<br> 

* Now to deploy these workloads on our minikube cluster, please run command ` kubectl apply -f . ` You may see the output that all workloads are created.

    <img src="./Images/kubectl-apply.png" width="600" height="280"/> 
     &nbsp;<br> 

* Now click on `Workloads` tab. You may see the list of workloads and overview. If you select `Overview`, you may see the total numbe of pods, deployments etc. 
<img src="./Images/overview.png" width="600" height="280"/> 
     &nbsp;<br> 

* You may check status and logs of these workloads one by one. Click on `Pods`. You will see the list of Pods deployed in cluster. If you want to check details of Pod, just click on it and lens will display all the details of that Pod. 
<img src="./Images/Pods.png" width="600" height="280"/> 
     &nbsp;<br>

* In the right corner of details plane, you may see some icons like, pod shell, logs, edit, delete etc. Lens make it easy for us to check logs of pods, execute inside pod or edit pods manifest using these option in UI. Let's check logs of `nodeapp` pod. Click on `Pod Logs` icon. It will display logs of that paricular pod. 
<img src="./Images/nodeapp-logs.png" width="600" height="280"/> 
     &nbsp;<br> 

* In this way, you may check details and status of any workload you deployed. 

* In, `Network` section, you may see services and other network components listed. Click on `Services`. You may see the list of services running and their details.
* Let's check `nginx` service. Select it, you will see the details of service. 
<img src="./Images/services.png" width="600" height="280"/> 
     &nbsp;<br> 

* Now if you want to `port forward` for this service, you may see the blue coloured tab `Forward` under `ports` section in details plane. Slect it and you will see a small pop-up screen, in which you have to mention port number to which you want to expose this service. Then click on start. It will redirect you to browser and you may see your service's index page in browser.
<img src="./Images/port-forward.png" width="600" height="280"/> 
     &nbsp;<br> 
<img src="./Images/output.png" width="600" height="280"/> 
    &nbsp;<br>

