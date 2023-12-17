# Multimodal Deployment

# Build the Infra
source env*.sh
sh infra*
# Development
source env*.sh
sh app-dev*.sh

# Cleanup
source env*.sh
sh cleanup.sh

