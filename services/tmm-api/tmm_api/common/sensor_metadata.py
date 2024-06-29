import boto3
import os

from fastapi import HTTPException
from decimal import Decimal

sensors_table_name = os.environ.get("TMM_SENSORS_TABLE_NAME")


def get_sensors_metadata():
    dynamodb = boto3.resource("dynamodb")
    if sensors_table_name is None:
        print("Error: TMM_SENSORS_TABLE_NAME not set")
        raise HTTPException(status_code=500, detail="Error: TMM_SENSORS_TABLE_NAME not set")
    table = dynamodb.Table(sensors_table_name)

    try:
        response = table.scan()
        return {
            item["sensor_id"]: delete_private_keys(convert_dyno_to_plain(item))
            for item in response["Items"]
            if item.get("sensor_id") is not None
        }
    except Exception as e:
        print(f"Error retrieving sensor metadata: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving sensor metadata")


def convert_dyno_to_plain(dynamo_item):
    return {k: float(v) if isinstance(v, Decimal) else v for k, v in dynamo_item.items()}


def delete_private_keys(item):
    private_keys = {"contact", "ttn_account"}
    return {k: v for k, v in item.items() if k not in private_keys}


def write_sensor_metadata(sensor):
    dynamodb = boto3.resource("dynamodb")
    if sensors_table_name is None:
        print("Error: TMM_SENSORS_TABLE_NAME not set")
        raise HTTPException(status_code=500, detail="Error: TMM_SENSORS_TABLE_NAME not set")
    table = dynamodb.Table(sensors_table_name)

    try:
        response = table.put_item(Item=sensor)
        return response
    except Exception as e:
        print(f"Error saving sensor metadata: {e}")
        raise HTTPException(status_code=500, detail="Error saving sensor metadata")
