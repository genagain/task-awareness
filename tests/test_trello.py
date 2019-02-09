from datetime import datetime
import json

from freezegun import freeze_time
import psycopg2
import pytest

from taskawareness import trello

# TODO make a fixture that sets up different kinds of cards as different variables
# TODO consider parameterizing tests or using scenarios when appropriate

@pytest.fixture
def recreate_tables():
    conn, cur = trello.connect_db()
    # TODO make this relative project root
    cur.execute(open('../schema.sql', 'r').read())
    conn.commit()

def test_archived_closed_card():
    action = {
        'id': '5c50f4e70a13222ac4421104',
        'idMemberCreator': '54adf4eebc4b592a63005ea9',
        'data': {
            'list': {
                'name': 'Do (Urgent and Important)',
                'id': '5c4ef56ff04981732a524b3e'
            },
            'board': {
                'shortLink': 'oKvCzrFR',
                'name': 'I get to testing',
                'id': '5c4ef5558ac287209796dace'
            },
            'card': {
                'shortLink': 'lBvEcUwJ',
                'idShort': 1,
                'name': 'Testing',
                'id': '5c50f4ddb89030449f74f47b',
                'closed': True
            },
            'old': {
                'closed': False
            }
        },
        'type': 'updateCard',
        'date': '2019-01-30T00:50:47.411Z',
        'limits': {},
        'memberCreator': {
            'id': '54adf4eebc4b592a63005ea9',
            'avatarHash': None,
            'avatarUrl': None,
            'fullName': 'Gen Ohta',
            'idMemberReferrer': None,
            'initials': 'GO',
            'username': 'genohta'
        }
    }
    assert trello.archived(action)

def test_archived_update_card():
    action = {
        'id': '5c5628658c0eab75ed6b4b71',
        'idMemberCreator': '54adf4eebc4b592a63005ea9',
        'data': {
            'list': {
                'name': 'Do (Urgent and Important)',
                'id': '5c4ef56ff04981732a524b3e'
            },
            'board': {
                'shortLink': 'oKvCzrFR',
                'name': 'I get to testing',
                'id': '5c4ef5558ac287209796dace'
            },
            'card': {
                'shortLink': 'DXZywyWw',
                'idShort': 2,
                'id': '5c56285ef443aa6100cb520d',
                'name': 'Test Update No Archive'
            },
            'old': {
                'name': 'Update'
            }
        },
        'type': 'updateCard',
        'date': '2019-02-02T23:31:49.661Z',
        'limits': {},
        'memberCreator': {
            'id': '54adf4eebc4b592a63005ea9',
            'avatarHash': None,
            'avatarUrl': None,
            'fullName': 'Gen Ohta',
            'idMemberReferrer': None,
            'initials': 'GO',
            'username': 'genohta'
            }
        }
    assert not trello.archived(action)

def test_archived_create_card():
    action = {
        'id': '5c56285ef443aa6100cb520e',
        'idMemberCreator': '54adf4eebc4b592a63005ea9',
        'data': {
            'board': {
                'shortLink': 'oKvCzrFR',
                'name': 'I get to testing',
                'id': '5c4ef5558ac287209796dace'
            },
            'list': {
                'name': 'Do (Urgent and Important)',
                'id': '5c4ef56ff04981732a524b3e'
            },
            'card': {
                'shortLink': 'DXZywyWw',
                'idShort': 2,
                'name': 'Update',
                'id': '5c56285ef443aa6100cb520d'
            }
        },
        'type': 'createCard',
        'date': '2019-02-02T23:31:42.332Z',
        'limits': {},
        'memberCreator': {
            'id': '54adf4eebc4b592a63005ea9',
            'avatarHash': None,
            'avatarUrl': None,
            'fullName': 'Gen Ohta',
            'idMemberReferrer': None,
            'initials': 'GO',
            'username': 'genohta'
        }
    }
    assert not trello.archived(action)

def test_parse_datetime_utc():
    expected_datetime = datetime(2019, 1, 30, 0, 50, 47, 411000)
    actual_datetime = trello.parse_datetime('2019-01-30T00:50:47.411Z')

    assert actual_datetime == expected_datetime
    assert actual_datetime.strftime('%Y-%m-%d %H:%M:%S') == '2019-01-30 00:50:47'

def test_parse_datetime_est():
    expected_datetime = datetime(2019, 1, 29, 19, 50, 47, 411000)
    actual_datetime = trello.parse_datetime('2019-01-30T00:50:47.411Z', convert_est=True)

    assert actual_datetime == expected_datetime
    assert actual_datetime.strftime('%Y-%m-%d %H:%M:%S') == '2019-01-29 19:50:47'

def test_filter_date_true():
    action = {
        'id': '5c50f4e70a13222ac4421104',
        'idMemberCreator': '54adf4eebc4b592a63005ea9',
        'data': {
            'list': {
                'name': 'Do (Urgent and Important)',
                'id': '5c4ef56ff04981732a524b3e'
            },
            'board': {
                'shortLink': 'oKvCzrFR',
                'name': 'I get to testing',
                'id': '5c4ef5558ac287209796dace'
            },
            'card': {
                'shortLink': 'lBvEcUwJ',
                'idShort': 1,
                'name': 'Testing',
                'id': '5c50f4ddb89030449f74f47b',
                'closed': True
            },
            'old': {
                'closed': False
            }
        },
        'type': 'updateCard',
        'date': '2019-01-30T00:50:47.411Z',
        'limits': {},
        'memberCreator': {
            'id': '54adf4eebc4b592a63005ea9',
            'avatarHash': None,
            'avatarUrl': None,
            'fullName': 'Gen Ohta',
            'idMemberReferrer': None,
            'initials': 'GO',
            'username': 'genohta'
        }
    }
    assert trello.filter_date(action, '2019-01-29')

def test_filter_date_false():
    action = {
        'id': '5c50f4e70a13222ac4421104',
        'idMemberCreator': '54adf4eebc4b592a63005ea9',
        'data': {
            'list': {
                'name': 'Do (Urgent and Important)',
                'id': '5c4ef56ff04981732a524b3e'
            },
            'board': {
                'shortLink': 'oKvCzrFR',
                'name': 'I get to testing',
                'id': '5c4ef5558ac287209796dace'
            },
            'card': {
                'shortLink': 'lBvEcUwJ',
                'idShort': 1,
                'name': 'Testing',
                'id': '5c50f4ddb89030449f74f47b',
                'closed': True
            },
            'old': {
                'closed': False
            }
        },
        'type': 'updateCard',
        'date': '2019-01-30T00:50:47.411Z',
        'limits': {},
        'memberCreator': {
            'id': '54adf4eebc4b592a63005ea9',
            'avatarHash': None,
            'avatarUrl': None,
            'fullName': 'Gen Ohta',
            'idMemberReferrer': None,
            'initials': 'GO',
            'username': 'genohta'
        }
    }
    assert not trello.filter_date(action, '2019-01-30')

def test_connect_db_cursor():
    conn, cur = trello.connect_db()

    # TODO change this to taskawareness_test once I make the db connection environment aware
    assert conn.dsn == 'dbname=taskawareness_dev user=postgres'
    assert type(conn).__name__ == 'connection'
    assert type(cur).__name__ == 'cursor'

def test_connect_db_dict_cursor():
    conn, cur = trello.connect_db(dict_cursor=True)

    # TODO change this to taskawareness_test once I make the db connection environment aware
    assert conn.dsn == 'dbname=taskawareness_dev user=postgres'
    assert type(conn).__name__ == 'connection'
    assert type(cur).__name__ == 'DictCursor'

def test_sequential_insert_one_row(recreate_tables):
    records = [
        {
            'datetime': '2019-01-30 00:50:47',
            'board_id': '5c4ef5558ac287209796dace',
            'card_id': '5c50f4ddb89030449f74f47b',
            'card_name': 'Testing'
        }
    ]

    recreate_tables

    trello.sequential_insert(records)

    query = 'SELECT datetime, board_id, card_id, card_name FROM cards;'
    query_results = trello.execute_select(query)

    assert len(query_results) == 1

def test_sequential_insert_three_rows(recreate_tables):
    records = [
        {
            'datetime': '2019-01-30 00:50:47',
            'board_id': '5c4ef5558ac287209796dace',
            'card_id': '5c50f4ddb89030449f74f47b',
            'card_name': 'Testing 1'
        },
        {
            'datetime': '2019-01-30 00:50:47',
            'board_id': '5c4ef5558ac287209796dace',
            'card_id': '5c50f4ddb89030449f74f5fc',
            'card_name': 'Testing 2'
        },
        {
            'datetime': '2019-01-30 00:50:47',
            'board_id': '5c4ef5558ac287209796dace',
            'card_id': '5c50f4ddb89030449f74f8df',
            'card_name': 'Testing 3'
        }
    ]

    recreate_tables

    trello.sequential_insert(records)

    query = 'SELECT datetime, board_id, card_id, card_name FROM cards;'
    query_results = trello.execute_select(query)

    assert len(query_results) == 3

def test_sequential_insert_no_rows(recreate_tables):
    records = []

    recreate_tables

    trello.sequential_insert(records)

    query = 'SELECT datetime, board_id, card_id, card_name FROM cards;'
    query_results = trello.execute_select(query)

    assert len(query_results) == 0

def test_execute_select_all_attributes(recreate_tables):
    records = [
        {
            'datetime': '2019-01-30 00:50:47',
            'board_id': '5c4ef5558ac287209796dace',
            'card_id': '5c50f4ddb89030449f74f47b',
            'card_name': 'Testing 1'
        },
        {
            'datetime': '2019-01-30 00:50:47',
            'board_id': '5c4ef5558ac287209796dbcf',
            'card_id': '5c50f4ddb89030449f74f5fc',
            'card_name': 'Testing 2'
        },
        {
            'datetime': '2019-01-30 00:50:47',
            'board_id': '5c4ef5558ac287209796deac',
            'card_id': '5c50f4ddb89030449f74f8df',
            'card_name': 'Testing 3'
        }
    ]

    recreate_tables

    trello.sequential_insert(records)

    query = 'SELECT id, datetime, board_id, card_id, card_name FROM cards;'
    query_results = trello.execute_select(query)

    assert all([set(result.keys()) == set(['id', 'datetime', 'board_id', 'card_id', 'card_name']) for result in query_results])


def test_execute_select_no_date(recreate_tables):
    records = [
        {
            'datetime': '2019-01-30 00:50:47',
            'board_id': '5c4ef5558ac287209796dace',
            'card_id': '5c50f4ddb89030449f74f47b',
            'card_name': 'Testing 1'
        },
        {
            'datetime': '2019-01-30 00:50:47',
            'board_id': '5c4ef5558ac287209796dbcf',
            'card_id': '5c50f4ddb89030449f74f5fc',
            'card_name': 'Testing 2'
        },
        {
            'datetime': '2019-01-30 00:50:47',
            'board_id': '5c4ef5558ac287209796deac',
            'card_id': '5c50f4ddb89030449f74f8df',
            'card_name': 'Testing 3'
        }
    ]

    recreate_tables

    trello.sequential_insert(records)

    query = 'SELECT id, board_id, card_id, card_name FROM cards;'
    query_results = trello.execute_select(query)

    assert all([set(result.keys()) == set(['id', 'board_id', 'card_id', 'card_name']) for result in query_results])

def test_execute_select_no_ids(recreate_tables):
    records = [
        {
            'datetime': '2019-01-30 00:50:47',
            'board_id': '5c4ef5558ac287209796dace',
            'card_id': '5c50f4ddb89030449f74f47b',
            'card_name': 'Testing 1'
        },
        {
            'datetime': '2019-01-30 00:50:47',
            'board_id': '5c4ef5558ac287209796dbcf',
            'card_id': '5c50f4ddb89030449f74f5fc',
            'card_name': 'Testing 2'
        },
        {
            'datetime': '2019-01-30 00:50:47',
            'board_id': '5c4ef5558ac287209796deac',
            'card_id': '5c50f4ddb89030449f74f8df',
            'card_name': 'Testing 3'
        }
    ]

    recreate_tables

    trello.sequential_insert(records)

    query = 'SELECT datetime, card_name FROM cards;'
    query_results = trello.execute_select(query)

    assert all([set(result.keys()) == set(['datetime', 'card_name']) for result in query_results])

def test_execute_select_no_data(recreate_tables):
    recreate_tables

    query = 'SELECT id, board_id, card_id, card_name FROM cards;'
    query_results = trello.execute_select(query)

    assert query_results == []

def test_store_archived_one_card(monkeypatch, recreate_tables):
    def mock_fetch_actions():
        # TODO make this relative project root
        # TODO use this mock for testing DB storage functions
        with open('archived_card_action.json', 'r') as f:
            data = json.loads(f.read())

        return data

    monkeypatch.setattr(trello, 'fetch_actions', mock_fetch_actions)

    recreate_tables

    actions = trello.fetch_actions()

    trello.store_archived_cards(actions, '2019-01-29')

    expected_archived_cards = [
        {
            'datetime': '2019-01-30 00:50:47',
            'board_id': '5c4ef5558ac287209796dace',
            'card_id': '5c50f4ddb89030449f74f47b',
            'card_name': 'Testing'
        }
    ]

    query = 'SELECT datetime, board_id, card_id, card_name FROM cards;'
    actual_archived_cards = trello.execute_select(query)

    assert actual_archived_cards == expected_archived_cards

def test_store_archived_no_cards(monkeypatch, recreate_tables):
    def mock_fetch_actions():
        # TODO make this relative project root
        # TODO use this mock for testing DB storage functions
        with open('archived_card_action.json', 'r') as f:
            data = json.loads(f.read())

        return data

    monkeypatch.setattr(trello, 'fetch_actions', mock_fetch_actions)

    recreate_tables

    actions = trello.fetch_actions()

    trello.store_archived_cards(actions, '2019-01-30')

    expected_archived_cards = []

    query = 'SELECT datetime, board_id, card_id, card_name FROM cards;'
    actual_archived_cards = trello.execute_select(query)

    assert actual_archived_cards == expected_archived_cards

def test_store_archived_deleted_card(monkeypatch, recreate_tables):
    def mock_fetch_actions():
        # TODO make this relative project root
        # TODO use this mock for testing DB storage functions
        with open('archive_delete_card_action.json', 'r') as f:
            data = json.loads(f.read())

        return data

    monkeypatch.setattr(trello, 'fetch_actions', mock_fetch_actions)

    recreate_tables

    actions = trello.fetch_actions()

    trello.store_archived_cards(actions, '2019-02-04')

    expected_archived_cards = []

    query = 'SELECT datetime, board_id, card_id, card_name FROM cards;'
    actual_archived_cards = trello.execute_select(query)

    assert actual_archived_cards == expected_archived_cards


def test_store_archived_three_cards(monkeypatch, recreate_tables):
    def mock_fetch_actions():
        # TODO make this relative project root
        # TODO use this mock for testing DB storage functions
        with open('archived_three_cards_action.json', 'r') as f:
            data = json.loads(f.read())

        return data

    monkeypatch.setattr(trello, 'fetch_actions', mock_fetch_actions)

    recreate_tables

    actions = trello.fetch_actions()

    trello.store_archived_cards(actions, '2019-02-04')

    expected_archived_cards = [
        {
            'datetime': '2019-02-05 01:14:01',
            'board_id': '5c4ef5558ac287209796dace',
            'card_id': '5c58e134bb05383311047074',
            'card_name': 'card 1'
        },
        {
            'datetime': '2019-02-05 01:14:02',
            'board_id': '5c4ef5558ac287209796dace',
            'card_id': '5c58e1352aa99c67e1f86803',
            'card_name': 'card 2'
        },
        {
            'datetime': '2019-02-05 01:14:04',
            'board_id': '5c4ef5558ac287209796dace',
            'card_id': '5c58e13714b9bb51dddcb7c8',
            'card_name': 'card 3'
        }
    ]

    query = 'SELECT datetime, board_id, card_id, card_name FROM cards;'
    actual_archived_cards = trello.execute_select(query)

    assert actual_archived_cards == expected_archived_cards

  # TODO test get archived card first clearing the DB, storing the card and then invoving get archived card and then make assertions
