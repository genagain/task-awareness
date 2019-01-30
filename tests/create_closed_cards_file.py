import requests
import json

def archived(card):
    if card['type'] == 'updateCard':
        return card['data']['card']['closed'] and not card['data']['old']['closed']
    else:
        return False

# TODO make this absolute path ideally relative to project root
key = open('../.api_key', 'r').read().strip('\n')
token = open('../.api_token', 'r').read().strip('\n')

## Staging board id
board_id = '5c4ef5558ac287209796dace'
output_file = 'archived_card_action.json'

url = f'https://api.trello.com/1/boards/{board_id}/actions'

querystring = {"limit":"300","key":key,"token":token}

response = requests.request("GET", url, params=querystring)

with open(output_file, 'w') as f:
    f.write(response.text)

