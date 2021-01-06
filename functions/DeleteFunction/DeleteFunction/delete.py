import os
import json
import boto3
dynamodb = boto3.resource('dynamodb')

from .decimalencoder import DecimalEncoder

def delete(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    data = json.loads(event['body'])
    pid = data.get('pid')
    def_key = data.get('defKey')

    item = table.delete_item(
        Key={
            'def_key': def_key,
            'pid': pid
        },
        ReturnValues='ALL_OLD'
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item,
                           cls=DecimalEncoder)
    }

    return response
