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

# Test
source env*
make run_test

# Cleanup
source env*
sh cleanup-mmm.sh

---
# Using Makefile
# Infra
source env*
make infra_setup

# Dev
source env*
make dev_setup

# Test
source env*
make run_test

# Cleanup
source env*
make cleanup
```


---
## Resources
* Git Repository: https://github.com/mregojos/GCP-LLM-Deployment
* Model Deployment Repository: https://github.com/mregojos/model-deployment