# Multi-Modal Model (MMM) Deployment

## Objective
* To test the new multi-modal model
* To deploy the new multi-modal model using GCP services

## Instructions
```sh
source mmm-env*
sh mmm-infra*
sh app-mmm-dev.sh

# Cleanup
source mmm-env*
sh mmm-cleanup.sh