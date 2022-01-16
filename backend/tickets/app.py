import json
import os
import time

import boto3
from boto3.dynamodb.conditions import Attr, Key
from dynamodb_json import json_util as dynamo_json

TICKETS_TABLE = os.environ['TICKETS_TABLE']


def lambda_handler(event, context):
    username = event['requestContext']['authorizer']['jwt']['claims']['username']
    response = { 
        'statusCode': 200
    }
    dynamo = boto3.client('dynamodb')
    table = boto3.resource('dynamodb').Table(TICKETS_TABLE)
    try:
        if 'GET /tickets' == event['routeKey']:
            resp = dynamo.query(
                TableName=TICKETS_TABLE,
                KeyConditionExpression='UserId = :u',
                ExpressionAttributeValues={':u': {'S': username}}
            )
            tickets = dynamo_json.loads(resp['Items'])
            response['body'] = list(map(lambda _: {
                'startDate': _['DateRange'][:10],
                'endDate': _['DateRange'][11:21],
                'picks': _['Picks']
            }, tickets))
        elif 'PUT /tickets' == event['routeKey']:
            req_body = json.loads(event['body'])
            ticket = {
                'UserId': username,
                'DateRange': '{}#{}#{}'.format(req_body['startDate'], req_body['endDate'], time.time()),
                'Picks': req_body['picks']
            }
            resp = table.put_item(
                Item=ticket,
                ConditionExpression='UserId <> :u AND DateRange <> :d',
                ExpressionAttributeValues={
                    ':u': {'S': username},
                    ':d': {'S': ticket['DateRange']}
                })
            print(resp)
            if resp['ResponseMetadata']['HTTPStatusCode'] >= 200 and resp['ResponseMetadata']['HTTPStatusCode'] < 300:
                response['statusCode'] = 201
            else:
                raise Exception(str(resp))
        else:
            msg = 'Unsupported route: {}'.format(event['routeKey'])
            response['body'] = msg
            raise Exception(msg)
    except Exception as e:
        response['statusCode'] = 400
        response['body'] = str(e)
    finally:
        if 'body' in response: 
            response['body'] = json.dumps(response['body'])
        return response
