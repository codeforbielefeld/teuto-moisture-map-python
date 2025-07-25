ENV ?= dev
LAMBDA_NAME ?= tmm_api_$(ENV)_lambda
LAMBDA_SOURCE_BUCKET ?= tmm-api-$(ENV)-lambda-src

.PHONY: build clean deploy-lambda


build: dist/lambda_package.zip

dist/lambda_package.zip: pyproject.toml uv.lock $(shell find tmm_api)

	rm -rf dist

	uv build --wheel

	uvx -p 3.11.13 pip install -t dist/lambda_package dist/*.whl 
#	uv pip install -t dist/lambda_package dist/*.whl 

	cd dist/lambda_package && \
	zip -q -r ../lambda_package.zip . -x '*.pyc'	

deploy-lambda: dist/lambda_package.zip

	aws s3 cp dist/lambda_package.zip s3://${LAMBDA_SOURCE_BUCKET}

	aws lambda update-function-code --function-name $(LAMBDA_NAME) --s3-bucket $(LAMBDA_SOURCE_BUCKET) --s3-key lambda_package.zip > /dev/null

clean:
	rm -rf dist