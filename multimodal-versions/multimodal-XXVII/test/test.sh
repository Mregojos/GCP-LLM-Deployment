echo "Run some tests... \n"

# Check if the database is reachable
# psycopg2
echo "pip install psycopg2-binary -q"
pip install psycopg2-binary -q
echo "Finished: psycopg2-binary \n"

# Check if the Cloud Run Endpoint is ready

# Check if the API is working