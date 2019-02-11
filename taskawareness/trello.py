from datetime import datetime, timedelta
import json

import psycopg2
import psycopg2.extras
import requests

# TODO add docstrings to every method

def fetch_actions():
    key = open('./.api_key', 'r').read().strip('\n')
    token = open('./.api_token', 'r').read().strip('\n')

    board_id = '56e6030fc8a3bbee27545990'
    url = f'https://api.trello.com/1/boards/{board_id}/actions'

    querystring = {"limit":"300","key":key,"token":token}
    response = requests.request("GET", url, params=querystring)
    json_response = json.loads(response.text)

    return json_response

def archived(action):
    if action['type'] == 'updateCard':
        return action['data']['card'].get('closed', False) and not action['data']['old'].get('closed', False)
    else:
        return False

def parse_datetime(date, convert_est=False):
    datetime_utc = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    if convert_est:
        return datetime_utc - timedelta(hours=5)
    else:
        return datetime_utc

def filter_date(action, date):
    datetime_est = parse_datetime(action['date'], convert_est=True)
    return date == datetime_est.strftime('%Y-%m-%d')

def connect_db(dict_cursor=False):
    # TODO make this environment aware with some environment variable or somethin
    conn = psycopg2.connect("dbname=taskawareness_dev user=postgres")
    if dict_cursor:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    else:
        cur = conn.cursor()

    return conn, cur

def execute_select(query):
    all_records = []
    _, cur = connect_db(dict_cursor=True)

    cur.execute(query)

    raw_records = cur.fetchall()

    if len(raw_records) == 0:
        return []

    for raw_record in raw_records:
        record = [(key,value.strftime('%Y-%m-%d %H:%M:%S'))
                  if type(value).__name__ == 'datetime'
                  else
                  (key,value)
                  for key, value
                  in raw_record.items()]

        all_records.append(dict(record))

    return sorted(all_records, key=lambda d: d['datetime']) \
           if 'datetime' in  raw_records[0].keys() \
           else all_records

def sequential_insert(records):
    if len(records) == 0:
        return

    attributes = records[0].keys()
    formatted_attributes = ', '.join(attributes)
    placeholders = ', '.join(['%s' for i in range(len(attributes))])

    insert_query = f"INSERT INTO cards ({formatted_attributes}) VALUES ({placeholders})"
    conn, cur = connect_db()

    for record in records:
        data = tuple(record.values())
        cur.execute(insert_query, data)
        conn.commit()

def store_archived_cards(actions, date):
    date_actions = [action for action in actions if filter_date(action, date)]
    archived_actions = [action for action in date_actions if archived(action)]
    archived_cards = []
    for action in archived_actions:
        datetime = parse_datetime(action['date'])
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
    sequential_insert(archived_cards)
