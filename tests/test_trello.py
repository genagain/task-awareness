import json

from freezegun import freeze_time

from taskawareness import trello


# TODO make a fixture that sets up and tears down tables

@freeze_time("Jan 29, 2019")
def test_store_archived_cards(monkeypatch):
    def mock_fetch_actions():
        # TODO make this relative project root
        # TODO use this mock for testing DB storage functions
        with open('archived_card_action.json', 'r') as f:
            data = json.loads(f.read())

        return data

    monkeypatch.setattr(trello, 'fetch_actions', mock_fetch_actions)

    actions = trello.fetch_actions()

    # TODO make sure this passes with an empty table
    trello.store_archived_cards(actions, '2019-01-29')

    expected_archived_cards = [
        {
            'datetime': '2019-01-29 19:50:47',
            'board_id': '5c4ef5558ac287209796dace',
            'card_id': '5c50f4ddb89030449f74f47b',
            'card_name': 'Testing'
        }
    ]

    query = 'SELECT datetime, board_id, card_id, card_name FROM cards;'
    actual_archived_cards = trello.execute_sql(query)

    assert actual_archived_cards == expected_archived_cards
