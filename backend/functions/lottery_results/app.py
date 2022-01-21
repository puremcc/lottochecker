import json
import os
# from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import List

import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ['TABLE_NAME']


def lambda_handler(event, context):
    game_id = 'lottotexas'  # event['pathParameters']['game']
    num_results = 50  # event['queryParams']['limit']
    # today = datetime.today().date()
    table = boto3.resource('dynamodb').Table(TABLE_NAME)
    resp = table.query(
        KeyConditionExpression=Key('GameId').eq(game_id),
        ScanIndexForward=False,
        Limit=num_results)

    items = []
    for item in resp['Items']:
        item['WinningNumbers'] = [int(n) for n in item['WinningNumbers']]
        items.append(item)

    return {
        "statusCode": 200,
        "body": json.dumps(resp['Items'])
    }
