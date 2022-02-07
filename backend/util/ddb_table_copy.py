#!/usr/local/bin/python3

'''usage: ddb_table_copy.py [-h] [--dest-table DEST_TABLE] [--dest-file DEST_FILE] source_table

Copy all DynamoDB items from SOURCE_TABLE to either DEST_TABLE or DEST_FILE. Useful for migrating data during a stack teardown/re-creation.

positional arguments:
  source_table          Name of source table in DynamoDB.

optional arguments:
  -h, --help            show this help message and exit
  --dest-table DEST_TABLE
                        Name of destination table in DynamoDB.
  --dest-file DEST_FILE
                        2) a valid file path string to save the items to, e.g. 'items.json'.
'''

import decimal
import json
from argparse import ArgumentParser
from typing import List

import boto3


def main(source_table: str, dest_table: str = None, dest_file: str = None):
    print('Getting records from source table...')
    tickets = get_items(source_table).map(add_date_columns) 
    if dest_table:
        print(
            f'Loading {len(tickets)} records into dest table {dest_table}...')
        load_items(tickets, dest_table)
    if dest_file:
        print(f'Saving {len(tickets)} records to file {dest_file}...')
        save_items_to_file(tickets, dest_file)


def get_items(table: str) -> List[dict]:
    table = boto3.resource('dynamodb').Table(table)
    resp = table.scan()
    tickets = resp['Items']
    while 'LastEvaluatedKey' in resp:
        resp = table.scan(ExclusiveStartKey=resp['LastEvaluatedKey'])
        tickets.append(resp['Items'])
    return tickets


def save_items_to_file(items: List[str], file_path: str):
    with open(file_path, 'w') as file:
        file.write(json.dumps(items, cls=DynamoItemEncoder))


def load_items(items: List[dict], table: str):
    table = boto3.resource('dynamodb').Table(table)
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(item)


def add_date_columns(item):
    item['StartDate'], item['EndDate'] = item['DateRage'].split('#')[:2]
    return item

class DynamoItemEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        if isinstance(obj, set):
            return list(obj)
        return super(DynamoItemEncoder, self).default(obj)


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Copy all DynamoDB items from SOURCE_TABLE to either DEST_TABLE or DEST_FILE. Useful for migrating data during a stack teardown/re-creation.')
    parser.add_argument(
        'source_table', help='Name of source table in DynamoDB.')
    parser.add_argument(
        '--dest-table', help='Name of destination table in DynamoDB.')
    parser.add_argument(
        '--dest-file', help='A valid file path string to save the items to, e.g. \'items.json\'.')
    args = parser.parse_args()
    main(args.source_table, args.dest_table, args.dest_file)
