import json

from freezegun import freeze_time

from taskawareness import trello

@freeze_time("Jan 29, 2019")
def test_get_archived_cards(monkeypatch):
    def mock_fetch_actions():
        # TODO make this relative project root
        with open('archived_card_action.json', 'r') as f:
            data = json.loads(f.read())

        return data

    monkeypatch.setattr(trello, 'fetch_actions', mock_fetch_actions)

    archived_cards = [
        {
            'datetime': '2019-01-30T00:50:47',
            'board_id': '5c4ef5558ac287209796dace',
            'card_id': '5c50f4ddb89030449f74f47b',
            'card_name': 'Testing'
        }
    ]
    assert trello.get_archived_cards('2019-01-29') == archived_cards


