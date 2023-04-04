# Github Packages
* GitHub Packages is a software package hosting service that allows you to host your software packages privately or publicly and use packages as dependencies in your projects. 
* GitHub Packages combines your source code and packages in one place to provide integrated permissions management and billing, so you can centralize your software development on GitHub. 
* You can integrate GitHub Packages with GitHub APIs, GitHub Actions, and webhooks to create an end-to-end DevOps workflow that includes your code, CI, and deployment solutions.
* GitHub Packages offers different package registries for commonly used package managers, such as npm, RubyGems, Apache Maven, Gradle, Docker, and NuGet. 

# Authenticate Github Packages
* To authenticate to a GitHub Packages registry within a GitHub Actions workflow, you can use:
    - GITHUB_TOKEN to publish packages associated with the workflow repository.
    - a personal access token (classic) with at least read:packages scope to install packages associated with other private repositories (which GITHUB_TOKEN can't access). 
* For more information about GITHUB_TOKEN used in GitHub Actions workflows, see https://docs.github.com/en/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token 

# Introduction to NuGET
* For any modern development platform, a mechanism through which developers can create, share, and consume useful code is an essential tool. Such code is bundled into "packages" that contain compiled code (as DLLs) along with other content needed in the projects that consume these packages. 
* For .NET (including .NET Core), the Microsoft-supported mechanism for sharing code is **NuGet**, which defines how packages for .NET are created, hosted, and consumed, and provides the tools for each of those roles. 
* A NuGet package is a ZIP file with the ".nupkg" extension that contains compiled code (DLLs), other files related to that code, and a descriptive manifest that includes information like the package's version number. 
* One can refer this series of video tutorials which is designed for absolute beginners: https://www.youtube.com/watch?v=WW3bO1lNDmo&list=PLdo4fOcmZ0oVLvfkFk8O9h6v2Dcdh2bh_ 

# Objective 
* In this tutorial, we are going to create a github-action workflow to build and push such NuGET packages to Github Packages Registry. 
* Here, we are going to use GITHUB_TOKEN instead of Personal Access Token to authenticate our packages within the workflow. 

# Steps
1. Create a github repository. You may create a public or private repository as per your application scope.
2. Add your project files and folders in the repository. 
3. We need to change some action permissions so that we will not get any authentication error. For that follow the steps:
    1. Go to settings tab.
    2. Click on Actions. Then select general. Here you can see "Actions Permissions". 
    3. Scroll down for "workflow permissions". Here select "Read and write permission". And save the settings.

4.  