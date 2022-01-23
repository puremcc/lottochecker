import json
import os
from datetime import date, datetime, timedelta
from typing import List

import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ['TABLE_NAME']


def lambda_handler(event, context):
    today = datetime.today().date()
    from_date = (today - timedelta(days=365)).isoformat()
    to_date = today.isoformat()
    if 'queryStringParameters' in event:
        from_date = event['queryStringParameters'].get('fromDate') or from_date
        to_date = event['queryStringParameters'].get('toDate') or to_date
    game_id = 'lottotexas'  # event['pathParameters']['game']
    # num_results = 50  # event['queryParams']['limit']
    table = boto3.resource('dynamodb').Table(TABLE_NAME)
    resp = table.query(
        KeyConditionExpression=Key('GameId').eq(game_id)
        & Key('DrawingDate').between(from_date, to_date),
        ScanIndexForward=False)  # Sort descending.

    tickets = []
    for item in resp['Items']:
        tickets.append({
            'drawingDate': item['DrawingDate'],
            'gameId': item['GameId'],
            'numbers': [int(n) for n in item['WinningNumbers']]
        })

    return {
        "statusCode": 200,
        "body": json.dumps(tickets)
    }
