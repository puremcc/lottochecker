#!/usr/local/bin/python3

'''usage: load_tickets_api.py [-h] --file-path FILE_PATH --api-url API_URL --access-token ACCESS_TOKEN

Load a JSON export of Tickets into TIckets table via the tickets API. The tickets will be stored as the cognito user (token) whose runs this.

optional arguments:
  -h, --help            show this help message and exit
  --file-path FILE_PATH
                        File path to json export of Ticket items.
  --api-url API_URL
  --access-token ACCESS_TOKEN
  '''

import json
from argparse import ArgumentParser

import requests


def main(file_path: str, api_url: str, access_token: str):
    api_url += '/tickets'
    tickets = json.load(open(file_path))
    for ticket in tickets:
        ticket['startDate'], ticket['endDate'] = ticket['DateRange'].split('#')[:2]
        ticket['picks'] = ticket['Picks']

    all_tickets = list_tickets(api_url, access_token)
    print(f'Total tickets in DB: {len(all_tickets)}')

    for ticket in tickets:
        resp = put_ticket(ticket, api_url, access_token)
        resp.raise_for_status()
        print(resp)

    all_tickets = list_tickets(api_url, access_token)
    print(f'Total tickets in DB: {len(all_tickets)}')


def put_ticket(ticket: dict, api_url, access_token) -> requests.Response:

    resp = requests.put(
        api_url,
        headers={'Authorization': f'Bearer {access_token}'},
        json=ticket
    )
    return resp


def list_tickets(api_url, access_token):
    resp = requests.get(
        api_url,
        headers={'Authorization': f'Bearer {access_token}'})
    resp.raise_for_status()
    return resp.json()


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Load a JSON export of Tickets into TIckets table via the tickets API. The tickets will be stored as the cognito user (token) whose runs this.')
    parser.add_argument('--file-path', required=True,
                        help="File path to json export of Ticket items.")
    parser.add_argument('--api-url', required=True)
    parser.add_argument('--access-token', required=True)
    args = parser.parse_args()
    main(args.file_path, args.api_url, args.access_token)
