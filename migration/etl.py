import json
from uuid import uuid4

import boto3


def ticket_json_to_dynamodb_json(ticket: dict):
    item = {
        "Id": {
            "S": str(uuid4())
        },
        "UserId": {
            "S": user_id
        },
        "StartDate": {
            "S": ticket['startDate']
        },
        "EndDate": {
            "S": ticket['endDate']
        },
        "Picks": {
            "L": [
                {
                    "M": {
                        "Numbers": {
                            "NS": [str(num) for num in ticket['picks'][0]['numbers']]
                        }
                    }
                }
            ]
        }
    }
    return item


if __name__ == '__main__':
    tickets = json.load(open('firebase_export.json'))
    ticket = tickets[0]

    user_id = 'mike@puremcc.com'
    table_name = 'LottoChecker-Tickets'
    dynamodb = boto3.Session(profile_name='mike').client('dynamodb')

    items = []
    for ticket in tickets:
        items.append(
            {
                'PutRequest': {
                    'Item': ticket_json_to_dynamodb_json(ticket)
                }
            })

    # response = dynamodb.put_item(Item=item, TableName=table_name)
    # response = dynamodb.put_item(Item=item, TableName=table_name)
    response = dynamodb.batch_write_item(RequestItems={table_name: items})
    print(response)
