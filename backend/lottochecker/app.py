import json
import os
from typing import final
import boto3


TICKETS_TABLE = os.environ['TICKETS_TABLE']


def lambda_handler(event, context):
    username = event['requestContext']['authorizer']['jwt']['claims']['username']
    body = None
    status_code = 200
    headers = {
        'Content-Type': 'application/json'
    }
    dynamo = boto3.client('dynamodb')
    try:
        if 'GET /lottochecker/tickets' == event['routeKey']:
            body = dynamo.query(
                TableName=TICKETS_TABLE,
                KeyConditionExpression='UserId = :u',
                ExpressionAttributeValues={':u': {'S': username}}
            )['Items']
        else:
            body = 'Unsupported route: "{}"'.format(event['routeKey'])
            raise Exception(body)
    except Exception as e:
        status_code = 400
        body = str(e)
    finally:
        return {
            'status_code': status_code,
            'body': json.dumps(body),
            'headers': headers
        }
