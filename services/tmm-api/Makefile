ENV ?= dev
LAMBDA_NAME ?= tmm_api_$(ENV)_lambda
LAMBDA_SOURCE_BUCKET ?= tmm-api-$(ENV)-lambda-source

build: dist/lambda_package.zip

dist/lambda_package.zip: pyproject.toml poetry.lock $(shell find tmm_api)

	rm -rf dist

	poetry build

	poetry run pip install -t dist/lambda_package dist/*.whl 

	cd dist/lambda_package && \
	zip -q -r ../lambda_package.zip . -x '*.pyc'	

deploy-lambda: dist/lambda_package.zip

	aws s3 cp dist/lambda_package.zip s3://${LAMBDA_SOURCE_BUCKET}

	aws lambda update-function-code --function-name $(LAMBDA_NAME) --s3-bucket $(LAMBDA_SOURCE_BUCKET) --s3-key lambda_package.zip > /dev/null

plan: terraform/tfplan

terraform/tfplan: terraform/*.tf terraform/*.tfvars terraform/.terraform.lock.hcl
	cd terraform && \
	terraform plan -out tfplan

deploy-infrastructure: terraform/tfplan
	cd terraform && \
	terraform apply tfplan

init:
	cd terraform && \
	terraform init

clean:
	rm -rf dist terraform/tfplan