import sys
import datetime
import json
import requests
import os

LOTTO_URL = "http://www.txlottery.org/export/sites/lottery/Games/Lotto_Texas/Winning_Numbers/lottotexas.csv"


def lambda_handler(event, context):
    try:
        winning_numbers = get_winning_numbers()
        return {
            "statusCode": 200,
            "headers": {
                # "Access-Control-Allow-Origin": os.environ['APP_HOST_URL'],
                "Access-Control-Allow-Origin": '*',
                "Access-Control-Allow-Methods": "OPTIONS,GET"
            },
            "body": json.dumps(winning_numbers)
        }
    except:
        # logging.exception(sys.exc_info()[0])
        raise Exception('Unable to retrieve winning numbers.\n {} \n {}'.format(
            str(sys.exc_info()[0]), str(sys.exc_info()[1])))


def get_winning_numbers() -> str:
    response = requests.get(LOTTO_URL)

    winning_numbers = []
    for row in response.text.split("\r\n")[-2:0:-1]:
        cols = row.split(",")
        # Only process last 3 years.
        if int(cols[3]) >= datetime.date.today().year - 3:
            drawing_date = "/".join(cols[1:4])
            this_row = {
                "drawingDate": drawing_date,
                "lottoType": cols[0],
                "numbers": cols[4:]
            }
            winning_numbers.append(this_row)
        else:
            break

    return winning_numbers
