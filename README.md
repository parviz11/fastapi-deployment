# Deploy API Endpoint for ML app with fastapi

Deploy ML app with API Endpoint that can handle single and batch requests. In this specific case, ML model is saved as `.pkl` file. The API endpoint is built using fastapi and is deployed on MS Azure platform.


### Source
https://learn.microsoft.com/en-us/azure/developer/python/tutorial-containerize-simple-web-app-for-app-service?tabs=web-app-fastapi#build-and-run-the-image-locally

# Create a resource group and Azure Container Registry

## Create a group with the az group create command.
az group create --name web-app-simple-rg --location northeurope

## Create an Azure Container Registry with the az acr create command.

az acr create --resource-group web-app-simple-rg --name scoringapp123 --sku Basic --admin-enabled true

ACR_PASSWORD=$(az acr credential show --resource-group web-app-simple-rg --name scoringapp123 --query "passwords[?name == 'password'].value" --output tsv)

# Build the image in Azure Container Registry
az acr build --resource-group web-app-simple-rg --registry scoringapp123 --image scoringapp:latest .


# Deploy to web app to azure

## Create App Service plan
az appservice plan create --name webplan --resource-group web-app-simple-rg --sku B1 --is-linux

## Create the web app
az webapp create --resource-group web-app-simple-rg --plan webplan --name scoringapp123 --docker-registry-server-password $ACR_PASSWORD --docker-registry-server-user scoringapp123 --role acrpull --deployment-container-image-name scoringapp123.azurecr.io/scoringapp:latest

## Log deployment
az webapp log tail --resource-group web-app-simple-rg --name scoringapp123
