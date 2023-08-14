def get_aws_secret(secret_id):
    import boto3

    secrets_client = boto3.client("secretsmanager")
    secret_response = secrets_client.get_secret_value(SecretId=secret_id)
    secret = secret_response["SecretString"]
    return secret
