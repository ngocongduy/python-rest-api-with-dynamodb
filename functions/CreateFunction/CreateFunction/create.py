import json
import logging
import os
import time

import boto3
dynamodb = boto3.resource('dynamodb')

from .decimalencoder import DecimalEncoder

def create(event, context):
    data = json.loads(event['body'])
    pid = data.get('pid')
    def_key = data.get('defKey')
    act_hi_var = data.get('actHiVar')
    # if 'text' not in data:
    #     logging.error("Validation Failed")
    #     raise Exception("Couldn't create the todo item.")
    if None in (pid,def_key,act_hi_var) or type(act_hi_var) is not dict:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")
    
    timestamp = str(time.time())

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'def_key': def_key,
        'pid': int(pid),
        'act_hi_var': act_hi_var,
        'checked': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,

    }

    # write the todo to the database
    try:
        table.put_item(Item=item,
                       ConditionExpression='attribute_not_exists(def_key) AND attribute_not_exists(pid)'
                       )
    except Exception as e:
        print(e)

        # ExpressionAttributeNames={
        #     '#todo_text': 'text',
        # },

        value = table.update_item(
            Key={
                'def_key': def_key,
                'pid': int(pid),
            },
            UpdateExpression="set act_hi_var = :r, updatedAt = :u",
            ExpressionAttributeValues={
                ':r': act_hi_var,
                ':u': timestamp
            },
            ReturnValues='ALL_NEW'
        )
        print(value)
        item = value
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item, cls=DecimalEncoder)
    }

    return response
