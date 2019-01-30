import requests
import json

def fetch_actions():
    key = open('./.api_key', 'r').read().strip('\n')
    token = open('./.api_token', 'r').read().strip('\n')

    # TODO implement this
    return []


def get_archived_cards(date):
    return fetch_actions()
