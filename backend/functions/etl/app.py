import os

import boto3
import requests
from boto3.dynamodb.conditions import Key

URL_TEMPLATE = 'http://www.txlottery.org/export/sites/lottery/Games/Lotto_Texas/Winning_Numbers/{game}.csv'
TABLE_NAME = os.environ['TABLE_NAME']


def lambda_handler(event, context):
    response = {'statusCode': 200}

    winning_numbers = get_winning_numbers(GamesIds.LOTTO_TEXAS)
    load_winning_numbers(winning_numbers)


class GamesIds:
    LOTTO_TEXAS = 'lottotexas'
    MEGAMILLIONS = 'megamillions'
    POWERBALL = 'powerball'


def get_winning_numbers(game: str) -> list:
    url = URL_TEMPLATE.format(game)
    response = requests.get(url)

    winning_numbers = []
    for row in response.text.split("\r\n")[-2:0:-1]:
        cols = row.split(",")
        this_row = {
            "DrawingDate": "-".join(cols[3:0:-1]),  # YYYY-MM-DD
            "GameId": cols[0],
            "WinningNumbers": [int(n) for n in cols[4:]]
        }
        winning_numbers.append(this_row)

    return winning_numbers


def load_winning_numbers(winning_numbers: list):
    game_id = winning_numbers[0]['GameId']
    table = boto3.resource('dynamo').table(TABLE_NAME)

    # Get latest loaded drawing date from target table.
    resp = table.query(
        KeyConditionExpression=Key('GameId').eq(game_id),
        ScanIndexForward=False,
        Limit=1)
    latest_loaded_date = resp['Items'][0]['DrawingDate']

    # Load only records after latest loaded date.
    with table.batch_writer() as batch:
        for result in winning_numbers:
            batch.put_item(Item=result)
