# Define the shell to use
SHELL := /bin/bash

# Set the commands as phony that aren't returning a file and should be run on every execution attempt
.PHONY: init plan apply autoapply destroy test checkvars lint

init:
	# Check if virtual environment already exists. If not, create it.
	[ ! -d "./priceChecker" ] && python3 -m venv priceChecker || true

	. priceChecker/bin/activate && \ # Activate the virtual environment
	pip3 install -r requirements.txt && \ # Install dependencies
	pip3 install ruff pylint bandit && \ # Install shift-left scanners

	terraform init # Initialise Terraform

	# Clean out old build & setup new lambda package build
	[ -d ./lambda_package ] && rm -rf ./lambda_package || true
	[ -d ./lambda_function.zip ] && rm -rf ./lambda_function.zip || true
	mkdir ./lambda_package
	pip3 install -r requirements.txt -t ./lambda_package
	cp priceChecker.py ./lambda_package # Need to update once rewrite is complete

plan: checkvars init lint test
	terraform plan
	[ -d ./lambda_function.zip ] && rm -rf ./lambda_function.zip || true

apply: checkvars init lint test
	terraform apply
	[ -d ./lambda_function.zip ] && rm -rf ./lambda_function.zip || true

autoapply: checkvars init lint test
	terraform apply -auto-approve
	[ -d ./lambda_function.zip ] && rm -rf ./lambda_function.zip || true

destroy: checkvars 
	terraform destroy # Blow it all away.  Requires user input.
	[ -d ./lambda_package ] && rm -rf ./lambda_package || true # If the directory exists, remove it
	[ -d ./lambda_function.zip ] && rm -rf ./lambda_function.zip || true # If the archive exists, remove it
	[ -d ./priceChecker ] && rm -rf ./priceChecker || true # Removes the virtual environment

checkvars:
	# Check that the AWS_PROFILE variable has been set
	@[ "${AWS_PROFILE}" ] || (echo "AWS_PROFILE is not set"; exit 1)

lint:
	# Run the linters over the scripts directory
	. priceChecker/bin/activate && \
	pylint ./lambdaScripts/* || exit 1 && \ # https://pypi.org/project/pylint/
	bandit -r ./lambdaScripts/ || exit 1 && \ # https://bandit.readthedocs.io
	ruff ./lambdaScripts/* || exit 1 # https://github.com/astral-sh/ruff

	test:
	# Implement testing using the virtual environment.
	. priceChecker/bin/activate && python3 ./lambdaScripts/items.py