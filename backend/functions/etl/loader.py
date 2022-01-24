import csv
import os
from io import StringIO

import boto3
import requests
from boto3.dynamodb.conditions import Key

URL_TEMPLATE = 'https://www.txlottery.org/export/sites/lottery/Games/{}/Winning_Numbers/{}.csv'
LOTTERY_RESULTS_TABLE = os.environ['TABLE_NAME']


class Games:
    LOTTO_TEXAS = 'Lotto Texas'
    MEGAMILLIONS = 'Mega Millions'
    POWERBALL = 'Powerball'


def run_etl(game_id: str) -> dict:
    source_data = extract_winning_numbers(game_id)
    loaded = load_winning_numbers(source_data)
    return {
        game_id: {
            'extracted': len(source_data),
            'loaded': loaded
        }
    }


def extract_winning_numbers(game_id: str) -> list:
    url = URL_TEMPLATE.format(
        game_id.replace(' ', '_'),
        game_id.replace(' ', '').lower()
    )
    resp = requests.get(url)
    reader = csv.DictReader(StringIO(resp.text),
                            fieldnames=['GameName', 'Month', 'Day', 'Year'],
                            restkey='Numbers')
    winning_numbers = []
    for row in reader:
        winning_numbers.append({
            'DrawingDate': '{}-{:02d}-{:02d}'.format(int(row['Year']), int(row['Month']), int(row['Day'])),
            'GameId': row['GameName'].replace(' ', '').lower(),
            'WinningNumbers': [int(n) for n in row['Numbers']]
        })

    return winning_numbers


def load_winning_numbers(winning_numbers: list):
    game_id = str(winning_numbers[0]['GameId'])
    table = boto3.resource('dynamodb').Table(LOTTERY_RESULTS_TABLE)

    # Get latest loaded record from target table.
    resp = table.query(
        KeyConditionExpression=Key('GameId').eq(game_id),
        ScanIndexForward=False,
        Limit=1)
    results_to_load = []
    if len(resp['Items']) == 0:
        # No data has been loaded, so load everything.
        results_to_load = winning_numbers
    else:
        latest_loaded_date = resp['Items'][0]['DrawingDate']
        for result in reversed(winning_numbers):
            result_date = result['DrawingDate']
            if result_date <= latest_loaded_date:
                break
            results_to_load.append(result)

    # Load only records after latest loaded date.
    with table.batch_writer() as batch:
        for result in results_to_load:
            batch.put_item(Item=result)

    return len(results_to_load)
