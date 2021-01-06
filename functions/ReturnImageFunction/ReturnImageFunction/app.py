import os
import json
import boto3
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')
from .decimalencoder import DecimalEncoder

import base64
def get_file_from_s3(file_key):
    s3 = boto3.client('s3')
    bucket_name="my-static-html"
    response = s3.get_object(
        Bucket=bucket_name,
        Key=file_key,
    )
    print(response)
    if response['ContentType'] == 'text/html':
        html = response['Body'].read()
        # print(html)
        # print(type(html))
        # print(html.decode())
        # print(type(html.decode()))
        return {
            'headers': { "Content-Type": "text/html" },
            'statusCode': 200,
            'body': html.decode()
        }

    image = response['Body'].read()
    return {
        'headers': { "Content-Type": "image/png" },
        'statusCode': 200,
        'body': base64.b64encode(image).decode('utf-8'),
        'isBase64Encoded': True
    }

def handle(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # data = json.loads(event['body'])
    # pid = data.get('pid')
    # print(event)
    # print(event['pathParameters'])
    pid = event['pathParameters']['id']
    print(pid)
    print(type(pid))
    index_name = os.environ['FIRST_GLOBAL_INDEX_NAME']
    print(index_name)
    result = table.query(
        IndexName=index_name,
        KeyConditionExpression=Key('pid').eq(int(pid))
    )
    print(result)

    if len(result['Items']) > 0:
        item = result['Items'][0]
        act_hi_var = item.get('act_hi_var')
        url = act_hi_var.get('url')
        if type(url) is str:
            try:
                return get_file_from_s3(url)
            except:
                return {
                    'headers': { "Content-type": "text/html" },
                    'statusCode': 200,
                    'body': "<h1>Fail to load get image!</h1>",
                }
        body = {"results":"Something wrong when getting file from s3"}
    else:
        body = {"results":"not found"}
    print(body)
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(body, cls=DecimalEncoder)
    }
    return response


