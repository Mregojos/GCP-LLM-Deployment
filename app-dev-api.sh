# Enable APIs
# gcloud services list --available | grep <service name>
gcloud services enable compute.googleapis.com iam.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com run.googleapis.com aiplatform.googleapis.com cloudresourcemanager.googleapis.com
# Generative Language API
gcloud services enable generativelanguage.googleapis.com

echo "\n #----------Services have been successfully enabled.----------# \n"

# 