# Multi-Modal Model (MMM) Deployment

## Objective
* To test the new multi-modal model
* To deploy the new multi-modal model using GCP services

## Instructions
```sh
# Infra
source env*
sh infra*
# Dev
source env*
sh app-dev-mmm.sh

# Cleanup
source env*
sh cleanup-mmm.sh
```