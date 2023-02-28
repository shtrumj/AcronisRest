import requests
import json
import pprint
import time
import datetime
from base64 import b64encode

current_timestamp = time.time()

current_datetime = datetime.datetime.fromtimestamp(current_timestamp)

week_ago_datetime = current_datetime - datetime.timedelta(days=1)
week_ago_str = week_ago_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

print(week_ago_str)
client_id = '5e99e385-8df4-44cd-935a-c7cb9181e382'
datacenter_url = 'https://eu-cloud.acronis.com'
endpoint = f'{datacenter_url}/api/2/{client_id}'
client_secret = 'bkgvqpkjellf34ost6ib5du2cqhbc2gu7enpvwvpljeipe5c5ehi'
base_url = f'{datacenter_url}/api/2'

encoded_client_creds = b64encode(f'{client_id}:{client_secret}'.encode('ascii'))
basic_auth = {
    'Authorization': 'Basic ' + encoded_client_creds.decode('ascii')
}
# print(basic_auth)

response = requests.post(
     f'{base_url}/idp/token',
     headers={'Content-Type': 'application/x-www-form-urlencoded', **basic_auth},
     data={'grant_type': 'client_credentials'},
 )
token_info = response.json()
auth = {'Authorization': 'Bearer ' + token_info['access_token']}
filters = {
    'startedAt': f'gt({week_ago_str})'
}
task_base = 'https://eu-cloud.acronis.com/api/task_manager/v2'
response = requests.get(f'{task_base}/tasks', headers=auth, params=filters)
response = response.json()
# print(response['items'])
# pprint.pprint(response['items'][0]['result'])
# pprint.pprint(response['items'][1]['policy']['type'])
GoodBackups = 0
BadBackups = 0
for items in response['items']:
    try:
        if items['policy']['type'] == 'backup':
            pprint.pprint(items['result']['code'])
            if items['result']['code'] == 'ok':
                GoodBackups = GoodBackups + 1

    except :
        pass
print(GoodBackups)