# use `nano makefile` to edit this file
# run `make`
# run `make [target name]` e.g., make run_test

target: print

print:
	echo "Makefile's working."

# Deployment

run_infra:
	# source env*
	sh infra*sh
	sh app-dev*sh

run_cleanup:
	sh cleanup*sh

run_test:
	sh test/test.sh
	python test/test.py

# For Development

run_dev:
	sh app-dev.sh

run_dev_cleanup:
	sh app-dev-cleanup.sh


# For Development (API)

run_dev_api:
	# source app-dev-api-env.sh
	app-dev-api.sh

run_dev_api_cleanup:
	# source app-dev-api-env.sh
	app-dev-api-cleanup.sh

