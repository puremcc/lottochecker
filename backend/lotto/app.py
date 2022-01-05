import sys
import datetime
import json
import requests
import os

url_base = "www.txlottery.org"
url_path = "http://www.txlottery.org/export/sites/lottery/Games/Lotto_Texas/Winning_Numbers/lottotexas.csv"


def get_winning_numbers() -> str:
    response = requests.get(url_path)

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

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '{},{}'.format(os.environ['APP_HOST_URL'], 'http://localhost:8080'),
            "Access-Control-Allow-Methods": "OPTIONS,GET"
        },
        "body": json.dumps(winning_numbers)
    }


def lambda_handler(event, context):
    try:
        return get_winning_numbers()
    except:
        # logging.exception(sys.exc_info()[0])
        raise Exception('Unable to retrieve winning numbers.\n {} \n {}'.format(
            str(sys.exc_info()[0]), str(sys.exc_info()[1])))
