# Multimodal Model Deployment

---
## Objective
* To test the new multimodal model capabilities
* To deploy the new multimodal model using GCP services

---
## Prerequisite
* Google Cloud Account
* Google Cloud Owner Role

---
## Setup

### For Multimodal Agent / Chatbot (One-Turn / Multi-Turn)
```sh
# Environment Variables
source env*

# Deployment (Google Cloud Services)
sh infrastructure-automation-multimodal.sh

# Dev
sh app-dev.sh

# Test
make run_test

# Cleanup
sh cleanup-multimodal.sh
sh app-dev-cleanup.sh

---
# Using makefile
# Environment Variables
source env*

# Deployment (Google Cloud Services)
make infra_setup

# Dev
make run_dev

# Test
make run_test

# Cleanup
make cleanup
make run_dev_cleanup

```

### For Multimodal App Collection and CLI
```sh
# Multimodal App Collection
sh app-collection.sh 
# Cleanup
sh app-collection-cleanup.sh

# Using Multimodal with CLI
cd app-cli
# README.md
# Cleanup
sh app-cli-cleanup.sh
```

---
## Screenshot

![Screenshot](image/Screenshot.png)


---
## Resources
* Multimodal Model Deployment Repository: https://github.com/mregojos/GCP-LLM-Deployment
* Deployed Web App: https://mattcloudtech.com/Agent
* Site Model Deployment Repository: https://github.com/mregojos/model-deployment