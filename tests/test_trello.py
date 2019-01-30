# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import json

from freezegun import freeze_time

from taskawareness import trello

@freeze_time("Jan 29, 2019")
def test_get_archived_cards(monkeypatch):
    def mock_fetch_actions():
        with open('archived_card_action.json', 'r') as f:
            data = json.loads(f.read())

        return data

    monkeypatch.setattr(trello, 'fetch_actions', mock_fetch_actions)

    archived_cards = [
        {
            'date': '2019-01-30T00:50:47.411Z',
            'card_id': '5c50f4ddb89030449f74f47b',
            'board_id': '5c4ef5558ac287209796dace',
            'name': 'Testing'
        }
    ]
    assert trello.get_archived_cards('2019-01-29') == archived_cards


