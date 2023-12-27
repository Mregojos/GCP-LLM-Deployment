# use `nano Makefile` to edit this file
# run `make`

target: print

print:
	echo "It's working"

infra_setup:
	sh infra*sh

dev_setup:
	sh app-dev*sh

cleanup:
	sh cleanup*sh

run_test:
	sh test.sh
