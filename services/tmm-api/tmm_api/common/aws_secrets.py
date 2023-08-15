def get_aws_ssm_parameter(parameter):
    import boto3

    client = boto3.client("ssm")
    resp = client.get_parameter(Name=parameter, WithDecryption=True)
    return resp["Parameter"]["Value"]
