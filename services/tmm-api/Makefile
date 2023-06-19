build: dist/lambda_package.zip

dist/lambda_package.zip: pyproject.toml poetry.lock $(shell find tmm_api)

	poetry build

	poetry run pip install -t dist/lambda_package dist/*.whl 

	cd dist/lambda_package && \
	zip -r ../lambda_package.zip . -x '*.pyc'	

plan-lambda: terraform/tfplan-lambda

terraform/tfplan-lambda: dist/lambda_package.zip terraform/*.tf
	cp -a dist/lambda_package.zip terraform
	
	cd terraform && \
	terraform plan --target aws_lambda_function.api_lambda_function -out tfplan-lambda

deploy-lambda: terraform/tfplan-lambda
	cd terraform && \
	terraform apply tfplan-lambda

plan-all: terraform/tfplan

terraform/tfplan: dist/lambda_package.zip terraform/*.tf
	cp -a dist/lambda_package.zip terraform
	
	cd terraform && \
	terraform plan -out tfplan


deploy-all: terraform/tfplan
	cd terraform && \
	terraform apply tfplan

init:
	cd terraform && \
	terraform init

clean:
	rm -rf dist terraform/tfplan terraform/lambda_package.zip