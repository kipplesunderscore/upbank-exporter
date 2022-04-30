import requests
from datetime import datetime, timezone
import calendar
from pprint import pprint
import csv
import argparse

class Upbank:

    base_url = 'https://api.up.com.au/api/v1'

    page_size = 80
    
    def __init__(self, access_token):
        self._headers = {'Authorization': 'Bearer ' + access_token}

    def calculate_transaction_type(self, transaction):
        if transaction['relationships']['transferAccount']['data']:
           transaction['transaction_type'] = "Transfer"
           id = transaction['relationships']['transferAccount']['data']['id']
           response = self.request(self.base_url + f'/accounts/{id}')
           transaction['relationships']['transferAccount']['data']['display_name'] = response['data']['attributes']['displayName']
        else:
            if transaction['attributes']['amount']['valueInBaseUnits'] < 0:
                transaction['transaction_type'] = "Purchase"
            else:
                transaction['transaction_type'] = "Payment Received"

        return transaction
        

    def transactions(self, year, month):
        month_begin = datetime(year, month, 1).astimezone().isoformat()
        month_end = datetime(year, month, calendar.monthrange(year, month)[-1], 23, 59, 59).astimezone().isoformat()
        params = {'filter[since]': str(month_begin), 
                'filter[until]': str(month_end),
                'page[size]': str(self.page_size), }

        response = self.request(self.base_url + '/transactions', params)

        response['data'] = map(self.calculate_transaction_type, response['data'])

        yield(response['data'])

        while(response['links']['next']):
            response = self.request(response['links']['next'], params)
            response['data'] = map(self.calculate_transaction_type, response['data'])
            yield(response['data'])

    def request(self, endpoint, params = {}):
        response = requests.get(endpoint, params = params, headers = self._headers)

        return response.json()


def output_csv_for_month(year, month, access_token_file):
    with open(access_token_file, 'r') as file:
        with open(f'./{year}-{month:02}.csv', 'w') as csvfile:
            fieldnames = ['id', 'transaction_type', 'description', 'raw_text', 'message', 'amount', 'roundup', 'created', 'settled']
            access_token = file.read().rstrip()
            
            upbank = Upbank(access_token)
            
            transactions = []
            for page in upbank.transactions(year, month):
                for transaction in page:
                    transactions.append(
                        {
                            'id': transaction['id'],
                            'transaction_type': transaction['transaction_type'],
                            'description': transaction['attributes']['description'],
                            'raw_text': transaction['attributes']['rawText'],
                            'amount': transaction['attributes']['amount']['value'],
                            'roundup': transaction['attributes']['roundUp']['amount']['value'] if transaction['attributes']['roundUp'] else '0',
                            'created': datetime.fromisoformat(transaction['attributes']['createdAt']).strftime("%Y/%m/%d"),
                            'settled': datetime.fromisoformat(transaction['attributes']['settledAt']).strftime("%Y/%m/%d"),
                        }
                    )
                    
                    csv_writer = csv.DictWriter(csvfile, fieldnames)
                    csv_writer.writeheader()   
                    csv_writer.writerows(transactions)

def main():
    parser = argparse.ArgumentParser(description="Up Bank CSV Exporter.")
    parser.add_argument('-year', metavar='year', type=int, nargs='?', default=datetime.now().year)
    parser.add_argument('-month', metavar='month', type=int, nargs='?', default=datetime.now().month)
    parser.add_argument('-token-file', metavar='file', type=str, nargs='?', default='./access_token')

    args = parser.parse_args()

    output_csv_for_month(args.year, args.month, args.token_file)
