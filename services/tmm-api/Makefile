build: dist/lambda_package.zip

dist/lambda_package.zip: tmm_api/* pyproject.toml poetry.lock

	poetry build

	poetry run pip install -t dist/lambda_package dist/*.whl 

	cd dist/lambda_package && \
	zip -r ../lambda_package.zip . -x '*.pyc'	

plan: build
	cp dist/lambda_package.zip terraform
	
	cd terraform && \
	terraform plan