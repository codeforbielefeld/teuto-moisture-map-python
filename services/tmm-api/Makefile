LAMBDA_NAME ?= tmm_api_lambda

build: dist/lambda_package.zip

dist/lambda_package.zip: pyproject.toml poetry.lock $(shell find tmm_api)

	poetry build

	rm -rf dist

	poetry run pip install -t dist/lambda_package dist/*.whl 

	cd dist/lambda_package && \
	zip -r ../lambda_package.zip . -x '*.pyc'	

deploy-lambda: dist/lambda_package.zip
	aws lambda update-function-code --function-name $(LAMBDA_NAME) \
		--zip-file fileb://dist/lambda_package.zip > /dev/null

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