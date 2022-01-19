import json

import loader
from loader import Games


def lambda_handler(event, context):
    response = {'statusCode': 200}

    job_summary = [
        loader.run_etl(Games.LOTTO_TEXAS),
        loader.run_etl(Games.MEGAMILLIONS)
    ]
    response['body'] = json.dumps(job_summary)

    return response
