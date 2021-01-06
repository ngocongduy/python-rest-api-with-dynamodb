import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')

from .decimalencoder import DecimalEncoder

import base64
from datetime import datetime
import time


def save_file_to_s3(file_key, encoded_file):
    s3 = boto3.client("s3", region_name='ap-southeast-1')
    stamp = datetime.now()

    key = "{}_{}.png".format(stamp, file_key)
    decodedFile = base64.b64decode(encoded_file)
    rs = s3.put_object(
        Bucket='my-static-html',
        Key=key,
        Body=decodedFile
    )
    print(rs)
    return key


def handle(event, context):
    # print(event)
    id = event['pathParameters']['id']
    body = event.get('body')
    print(type(body))
    isBase64Encoded = event.get('isBase64Encoded')
    key = None
    print(id)
    if isBase64Encoded:
        key = save_file_to_s3(id, body)
        act_hi_var = {'url': key}
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
        timestamp = str(time.time())
        item = {
            'def_key': 'file',
            'pid': int(id),
            'act_hi_var': act_hi_var,
            'checked': False,
            'createdAt': timestamp,
            'updatedAt': timestamp,

        }
        print(item)
        table.put_item(Item=item,
                       ConditionExpression='attribute_not_exists(def_key) AND attribute_not_exists(pid)'
                       )
    body = {"results": str(key)}
    print(body)
    response = {
        "statusCode": 200,
        "body": json.dumps(body, cls=DecimalEncoder)
    }
    return response
