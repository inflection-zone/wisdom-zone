# WSL Installation Steps 
* **Step 1**: Check whether virtualization is enabled in your system. To check this open "Task Manager". Navigate to "Performances" tab. At bottom look for virtualization. If it is enabled then fine, you may proceed to WSL installation. But if it is disabled, you need to enable it in BIOS settings. To do so you may follow this article : https://www.simplilearn.com/enable-virtualization-windows-10-article.
   <img src="task.png" width="600" /> 
      &nbsp;<br>
* **Step 2**: If virtaualization is enabled, then go to search and search for "Turn windows features on or off". It will open a window. In that enable options "Virtual machine platform", "Windows Hyperviser platform" and "windows subsystem for linux". 
    <img src="wsl1.png" width="600" /> 
      &nbsp;<br> 

* **Step 3**: Check for windows version and build. You must be running windows 10 or later & version & build requirements are : Version 2004 or later, with Build 19041 or later. To check press "windows key + R" and type "winver" there and press enter. 
* **Step 4**: If your windows fullfills above requirement, open windows powershell as "administrator" and run command `wsl --install`.
* **Step 5**: Next we need to install linux distribution. To see all available linux distributions, run command `wsl --list --online` or `wsl -l -o`. Then install your favourite distribution using command `wsl --install -d <distribution name>`. During installation, you need to configure your linux distribution by providing username & password. To check running distributions & their versions use command `wsl --list --verbose`. You can also install linux distribution directly from microsoft store.  
