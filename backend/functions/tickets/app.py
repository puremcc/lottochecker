import json
import os
import time

import boto3
from boto3.dynamodb.conditions import Key

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
        response['body'] = list(map(mapItemToTicket, resp['Items']))

    if 'GET /tickets/active' == event['routeKey']:
        resp = table.query(KeyConditionExpression=Key(
            'UserId').eq(USERNAME), FilterExpression=Attr)
        if not 200 <= resp['ResponseMetadata']['HTTPStatusCode'] < 300:
            raise Exception(str(resp))
        response['body'] = list(map(mapItemToTicket, resp['Items']))

    elif 'PUT /tickets' == event['routeKey']:
        req_body = json.loads(event['body'])
        item = mapTicketToItem(req_body)
        resp = table.put_item(
            Item=item,
            ConditionExpression='UserId <> :u AND DateRange <> :d',
            ExpressionAttributeValues={
                ':u': {'S': USERNAME},
                ':d': {'S': item['DateRange']}
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


def mapItemToTicket(item: dict):
    return {
        'startDate': item['DateRange'][:10],
        'endDate': item['DateRange'][11:21],
        'picks': [
            # Cast each number to an int.
            {'numbers': [int(n) for n in p['numbers']]}
            for p in item['Picks']
        ]
    }

def mapTicketToItem(ticket: dict):
    return {
        'UserId': USERNAME,
        'DateRange': '{}#{}'.format(ticket['startDate'], ticket['endDate']),
        'StartDate': ticket['startDate'],
        'EndDate': ticket['endDate']
        'Picks': [
            {'numbers': [int(n) for n in p['numbers']]}
            for p in ticket['picks']
        ]
    }

class Controller():

    def handle(request: dict):