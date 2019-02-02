from datetime import datetime, timedelta
import json

import psycopg2
import psycopg2.extras
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

def execute_sql(query):
    # TODO make this a test DB
    conn = psycopg2.connect("dbname=taskawareness_dev user=postgres")

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)

    # TODO consider breaking up connection and reading records

    all_records = []
    for raw_record in cur.fetchall():
        record = [(key,value.strftime('%Y-%m-%d %H:%M:%S'))
                  if type(value).__name__ == 'datetime'
                  else
                  (key,value)
                  for key, value
                  in raw_record.items()]

        all_records.append(dict(record))

    return all_records

# INSERT INTO cards (datetime, board_id, card_id, card_name)
# VALUES ('2019-01-30 00:50:47-00', '5c4ef5558ac287209796dace', '5c50f4ddb89030449f74f47b', 'Testing');
def bulk_insert(records):
    attributes = ', '.join(records[0].keys())

    insert_query = "INSERT INTO cards (datetime, board_id, card_id, card_name) VALUES (%s, %s, %s, %s)"

    conn = psycopg2.connect("dbname=taskawareness_dev user=postgres")
    cur = conn.cursor()

    for record in records:
        data = tuple(record.values())
        # import pdb; pdb.set_trace()
        cur.execute(insert_query, data)
        conn.commit()

    # TODO consider using bulk insert
    # cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
    #     ...      (100, "abc'def"))
    # psycopg2.extras.execute_values(cur, "INSERT INTO cards (datetime, board_id, card_id, card_name) VALUES %s", data)


def store_archived_cards(actions, date):
    date_actions = [action for action in actions if filter_date(action, date)]
    archived_actions = [action for action in date_actions if archived(action)]
    archived_cards = []
    for action in archived_actions:
        datetime = parse_date(action['date'])
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
    # TODO bulk insert here
    import pdb; pdb.set_trace()
    bulk_insert(archived_cards)

    return True

def store_completed_items(actions, date):
    return True

# TODO make this a DB read operation
def get_archived_cards(date):
    # TODO parsing archived cards a DB write operation
    actions = fetch_actions()
    date_actions = [action for action in actions if filter_date(action, date)]
    archived_actions = [action for action in date_actions if archived(action)]
    archived_cards = []
    for action in archived_actions:
        datetime = parse_date(action['date']).strftime('%Y-%m-%d %H:%M:%S')
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
    # TODO bulk insert here
    return archived_cards
