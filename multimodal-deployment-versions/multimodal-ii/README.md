# Multimodal Model (MMM) Deployment

## Objective
* To test the new multimodal model
* To deploy the new multimodal model using GCP services

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