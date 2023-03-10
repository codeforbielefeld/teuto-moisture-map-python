build: dist/lambda_package.zip

dist/lambda_package.zip: pyproject.toml poetry.lock $(shell find tmm_api)

	poetry build

	poetry run pip install -t dist/lambda_package dist/*.whl 

	cd dist/lambda_package && \
	zip -r ../lambda_package.zip . -x '*.pyc'	


plan: terraform/tfplan

terraform/tfplan: dist/lambda_package.zip terraform/*.tf
	cp -a dist/lambda_package.zip terraform
	
	cd terraform && \
	terraform plan -out tfplan


deploy: terraform/tfplan
	cd terraform && \
	terraform apply tfplan


clean:
	rm -rf dist terraform/tfplan terraform/lambda_package.zip