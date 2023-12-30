# For Dev Firewall Rule
if gcloud compute firewall-rules list --filter="name=$FIREWALL_RULES_NAME-dev" --format="table(name)" | grep -q $FIREWALL_RULES_NAME-dev; then
    gcloud compute firewall-rules delete $FIREWALL_RULES_NAME-dev --quiet
# else
    # echo "$FIREWALL_RULES_NAME-dev Firewall Rule doesn't exist." 
fi