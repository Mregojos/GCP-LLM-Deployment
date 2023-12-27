# Multimodal Model Deployment

---
## Objective
* To test the new multimodal model capabilities
* To deploy the new multimodal model using GCP services

## Prerequisite
* Google Cloud Account
* Google Cloud Owner Role

## Setup
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

---
## Resources
* Git Repository: https://github.com/mregojos/GCP-LLM-Deployment
* Model Deployment Repository: https://github.com/mregojos/model-deployment