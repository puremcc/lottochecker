import os

import boto3
import requests
from boto3.dynamodb.conditions import Key

URL_TEMPLATE = 'https://www.txlottery.org/export/sites/lottery/Games/{}/Winning_Numbers/{}.csv'
TABLE_NAME = os.environ['TABLE_NAME']


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

    winning_numbers = []
    for row in resp.text.split("\r\n")[-2:0:-1]:
        cols = row.split(",")
        y, m, d = int(cols[3]), int(cols[1]), int(cols[2])
        this_row = {
            'DrawingDate': '{}-{:02d}-{:02d}'.format(y, m, d),  # YYYY-MM-DD
            'GameId': cols[0].replace(' ', '').lower(),
            'WinningNumbers': [int(n) for n in cols[4:]]
        }
        winning_numbers.append(this_row)

    print(
        f'Extracted {len(winning_numbers)} records from source for {game_id}.')

    return winning_numbers


def load_winning_numbers(winning_numbers: list):
    game_id = str(winning_numbers[0]['GameId'])
    table = boto3.resource('dynamodb').Table(TABLE_NAME)

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

    print(f'Loaded {len(results_to_load):,} results for {game_id}.')

    return len(results_to_load)
