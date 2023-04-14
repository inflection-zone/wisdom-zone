# Deploy Nuget Packages
## Github Packages
* GitHub Packages is a software package hosting service that allows you to host your software packages privately or publicly and use packages as dependencies in your projects. 
* GitHub Packages combines your source code and packages in one place to provide integrated permissions management and billing, so you can centralize your software development on GitHub. 
* You can integrate GitHub Packages with GitHub APIs, GitHub Actions, and webhooks to create an end-to-end DevOps workflow that includes your code, CI, and deployment solutions.
* GitHub Packages offers different package registries for commonly used package managers, such as npm, RubyGems, Apache Maven, Gradle, Docker, and NuGet. 

## Authenticate Github Packages
* To authenticate to a GitHub Packages registry within a GitHub Actions workflow, you can use:
    - GITHUB_TOKEN to publish packages associated with the workflow repository.
    - a personal access token (classic) with at least read:packages scope to install packages associated with other private repositories (which GITHUB_TOKEN can't access). 
* For more information about GITHUB_TOKEN used in GitHub Actions workflows, see https://docs.github.com/en/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token 

## Introduction to NuGET
* For any modern development platform, a mechanism through which developers can create, share, and consume useful code is an essential tool. Such code is bundled into "packages" that contain compiled code (as DLLs) along with other content needed in the projects that consume these packages. 
* For .NET (including .NET Core), the Microsoft-supported mechanism for sharing code is **NuGet**, which defines how packages for .NET are created, hosted, and consumed, and provides the tools for each of those roles. 
* A NuGet package is a ZIP file with the ".nupkg" extension that contains compiled code (DLLs), other files related to that code, and a descriptive manifest that includes information like the package's version number. 
* One can refer this series of video tutorials which is designed for absolute beginners: https://www.youtube.com/watch?v=WW3bO1lNDmo&list=PLdo4fOcmZ0oVLvfkFk8O9h6v2Dcdh2bh_ 

## Objective 
* In this tutorial, we are going to create a github-action workflow to build and push such NuGET packages to Github Packages Registry. 
* Here, we are going to use GITHUB_TOKEN instead of Personal Access Token to authenticate our packages within the workflow. 

## Steps
1. Create a github repository.
2. Add your project files and folders in the repository. 
3. We need to change some permissions so that we will not get any authentication error. For that follow the steps:
    1. Go to `settings` tab.
    2. Click on `Actions`. Then select `general`. Here you can see `Actions Permissions`. 
    3. Scroll down for `workflow permissions`. Here select `Read and write permission`. And save the settings.

4. Go to `Actions` tab. Click on `setup a workflow yourself`.
5. Then in `main.yml` file, add following code.

    ```
        name: "Build and Deploy NuGet Package"

        on:
          push:
            branches: [master]

        env:
          PROJECT_PATH: "<path of your .csproj file>"
          PACKAGE_OUTPUT_DIRECTORY: "${{ github.workspace }}/output"

        jobs:
          deploy:
            name: "Deploy"
            runs-on: "ubuntu-latest"
            steps:
              - name: "Checkout"
                uses: actions/checkout@v2

              - name: "Install dotnet"
                uses: actions/setup-dotnet@v3
                with:
                  dotnet-version: "6.0.x"

              - name: "Restore packages"
                run: dotnet restore ${{ env.PROJECT_PATH }}

              - name: "Build project"
                run: dotnet build ${{ env.PROJECT_PATH }} --no-restore --configuration Release

              - name: "Pack project"
                run: dotnet pack ${{ env.PROJECT_PATH }} --no-restore --no-build --configuration Release --include-symbols --output ${{ env.PACKAGE_OUTPUT_DIRECTORY }}

              - name: "Auth package"
                run: dotnet nuget add source --username Priyanka-Inflectionzone --password ${{ secrets.GITHUB_TOKEN }} --store-password-in-clear-text --name github "https://nuget.pkg.github.com/Priyanka-Inflectionzone/index.json"

              - name: "Push package"
                run: dotnet nuget push "${{ env.PACKAGE_OUTPUT_DIRECTORY }}/*.nupkg" --source "github" --skip-duplicate
    ``` 

6. Now if you push any changes in project to the `master` branch of repository, the worklow will run. It will build the project, pack the project as Nuget package and push that package to Github Nuget packages registry. You may see that all the steps get check marks as shown in following image:

    <img src="./Images/workflow.png" width="600"/> 

7. Now go to your Github Profile. Under `Packages`, you may see your Nuget package. 

    <img src="./Images/package.png" width="600"/> 
