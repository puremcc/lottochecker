import json
import os
from typing import final

import boto3
from boto3.dynamodb.conditions import Attr, Key
from dynamodb_json import json_util as dynamo_json

TICKETS_TABLE = os.environ['TICKETS_TABLE']


def lambda_handler(event, context):
    username = event['requestContext']['authorizer']['jwt']['claims']['username']
    body = None
    status_code = 200
    headers = {
        'Content-Type': 'application/json'
    }
    dynamo = boto3.client('dynamodb')
    table = boto3.resource('dynamodb').Table(TICKETS_TABLE)
    try:
        if 'GET /lottochecker/tickets' == event['routeKey']:
            resp = dynamo.query(
                TableName=TICKETS_TABLE,
                KeyConditionExpression='UserId = :u',
                ExpressionAttributeValues={':u': {'S': username}}
            )
            body = dynamo_json.loads(resp['Items'])
        elif 'PUT /lottochecker/ticket' == event['routeKey']:
            req_body = json.loads(event['body'])
            ticket = {
                'UserId': username,
                'DateRange': '{}#{}'.format(req_body['startDate'], req_body['endDate']),
                'Picks': req_body['picks']
            }
            resp = table.put_item(Item=ticket)
            print(resp)
            if resp['ResponseMetadata']['HTTPStatusCode'] >= 200 and resp['ResponseMetadata']['HTTPStatusCode'] < 300:
                body = 'Ticket successfully created.'
        else:
            body = 'Unsupported route: {}'.format(event['routeKey'])
            raise Exception(body)
    except Exception as e:
        status_code = 400
        body = str(e)
    finally:
        return json.dumps(body)
        # return {
        #     # 'status_code': status_code,
        #     'body': json.dumps(body)  # ,
        #     # 'headers': headers
        # }


