# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:3.0-python3.6-appservice
FROM mcr.microsoft.com/azure-functions/python:3.0-python3.6

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

# Install fbClient
RUN apt-get update && \
    apt-get install -y libfbclient2

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot