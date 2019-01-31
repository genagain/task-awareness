from datetime import datetime, timedelta
import json

import requests

def fetch_actions():
    key = open('./.api_key', 'r').read().strip('\n')
    token = open('./.api_token', 'r').read().strip('\n')

    # TODO implement this with actual boardid
    return []


def archived(card):
    if card['type'] == 'updateCard':
        return card['data']['card']['closed'] and not card['data']['old']['closed']
    else:
        return False

def parse_date(date, convert_est=False):
    datetime_utc = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    if convert_est:
        return datetime_utc - timedelta(hours=5)
    else:
        return datetime_utc

def filter_date(action, date):
    datetime_est = parse_date(action['date'], convert_est=True)
    return date == datetime_est.strftime('%Y-%m-%d')

def get_archived_cards(date):
    actions = fetch_actions()
    date_actions = [action for action in actions if filter_date(action, date)]
    archived_actions = [action for action in date_actions if archived(action)]
    archived_cards = []
    for action in archived_actions:
        datetime = parse_date(action['date']).strftime('%Y-%m-%dT%H:%M:%S')
        board_id = action['data']['board']['id']
        card_id = action['data']['card']['id']
        card_name = action['data']['card']['name']
        archived_card = {
            'datetime': datetime,
            'board_id': board_id,
            'card_id': card_id,
            'card_name': card_name
        }
        archived_cards.append(archived_card)
    return archived_cards
