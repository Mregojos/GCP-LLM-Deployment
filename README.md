# GCP Multi-Modal Large Language Model Deployment

---

## Objective 
* To deploy Multi-Modal Large Language Model on GCP

---
### Prerequisite
* GCP Account
* GCP Project Owner Role

```sh
# Export Variables
source environment-variables.sh
# Build infrastructure and deploy the app
sh infrastructure-automation.sh

# Cleanup
# Export Variables
source environment-variables.sh
sh cleanup.sh
```

---
Resources:
* Git Repository https://github.com/mregojos/GCP-LLM-Deployment
* Model Deployment Repository https://github.com/mregojos/model-deployment