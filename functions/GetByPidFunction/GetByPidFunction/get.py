import os
import json
import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')
from .decimalencoder import DecimalEncoder


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    data = json.loads(event['body'])
    pid = data.get('pid')
    def_key = data.get('defKey')

    result = table.query(
        KeyConditionExpression= Key('def_key').eq(def_key) & Key('pid').eq(pid)
    )
    print(result)
    if len(result['Items']) > 0:
        item = result['Items'][0]
    else:
        item = {"item":"not found"}

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item,
                           cls=DecimalEncoder)
    }

    return response

def get_by_pid(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    data = json.loads(event['body'])
    pid = data.get('pid')

    index_name = os.environ['FIRST_GLOBAL_INDEX_NAME']
    print(index_name)
    result = table.query(
        IndexName=index_name,
        KeyConditionExpression=Key('pid').eq(pid)
    )

    print(result)
    if len(result['Items']) > 0:
        item = result['Items'][0]
    else:
        item = {"item":"not found"}

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item,
                           cls=DecimalEncoder)
    }

    return response
