import json
import os
import time

import boto3
from boto3.dynamodb.conditions import Attr, Key
from dynamodb_json import json_util as dynamo_json

TICKETS_TABLE = os.environ['TICKETS_TABLE']


def lambda_handler(event, context):
    USERNAME = event['requestContext']['authorizer']['jwt']['claims']['username']
    response = {
        'statusCode': 200
    }
    table = boto3.resource('dynamodb').Table(TICKETS_TABLE)
    if 'GET /tickets' == event['routeKey']:
        resp = table.query(KeyConditionExpression=Key('UserId').eq(USERNAME))
        if not 200 <= resp['ResponseMetadata']['HTTPStatusCode'] < 300:
            raise Exception(str(resp))
        response['body'] = [
            {
                'startDate': item['DateRange'][:10],
                'endDate': item['DateRange'][11:21],
                'picks': [
                    # Cast each number to an int.
                    {'numbers': [int(n) for n in p['numbers']]}
                    for p in item['Picks']
                ]
            } for item in resp['Items']
        ]
    elif 'PUT /tickets' == event['routeKey']:
        req_body = json.loads(event['body'])
        ticket = {
            'UserId': USERNAME,
            'DateRange': '{}#{}#{}'.format(req_body['startDate'], req_body['endDate'], time.time()),
            'Picks': [
                {'numbers': set([int(n) for n in p['numbers']])}
                for p in req_body['picks']
            ]
        }
        resp = table.put_item(
            Item=ticket,
            ConditionExpression='UserId <> :u AND DateRange <> :d',
            ExpressionAttributeValues={
                ':u': {'S': USERNAME},
                ':d': {'S': ticket['DateRange']}
            })
        print(resp)
        if 200 <= resp['ResponseMetadata']['HTTPStatusCode'] < 300:
            response['statusCode'] = 201
        else:
            raise Exception(str(resp))
    else:
        msg = 'Unsupported route: {}'.format(event['routeKey'])
        response['body'] = msg
        raise Exception(msg)

    if 'body' in response:
        response['body'] = json.dumps(response['body'])
    return response
