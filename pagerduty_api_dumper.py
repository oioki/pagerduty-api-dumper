#!/usr/bin/env python3

# https://developer.pagerduty.com/api-reference/reference/REST/openapiv3.json

import argparse
import json
import os
import requests

from entities import entities_quick, entities_full


BASE_URL = 'https://api.pagerduty.com'


def mkdir(_dir):
    if not os.path.exists(_dir):
        os.mkdir(_dir)


def get_all_data(entity, headers):
    all_data = []

    offset = 0
    limit = 100

    while True:
        url = '{}/{}?offset={}&limit={}'.format(BASE_URL, entity, offset, limit)

        r = requests.get(url, headers=headers)
        # r.status_code:
        # 200 - OK
        # 401 - key is incorrect
        # 403 - key is correct, but access is restricted

        if r.status_code == 404:
            return {'status_code': 404, 'body': r.text}

        json_data = r.json()
        if entity in json_data:
            all_data += json_data[entity]
        else:
            all_data = json_data

        if 'more' in json_data:
            more = json_data['more']
            offset = json_data['offset']
            limit = json_data['limit']
            if more:
                offset = offset + limit
                continue

        return all_data


def entity_to_file(entity, local_headers=None, outfile=''):
    print('...', entity)
    if not outfile:
        outfile = entity.replace('/', '_') + '.json'

    if local_headers:
        headers = {**global_headers, **local_headers}
    else:
        headers = global_headers

    all_data = get_all_data(entity, headers)

    f = open('{}/{}'.format(output_dir, outfile), 'w')
    f.write(json.dumps(all_data, indent=2))
    f.close()

    return all_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dump all available data having PagerDuty API key')
    parser.add_argument('-k', '--key', required=True, help='PagerDuty API key')
    parser.add_argument('-o', '--output', default='output', help='Local directory to dump data')
    parser.add_argument('-f', '--full', action='store_true', default=False, help='Distinct API request for each item')
    args = parser.parse_args()

    global_headers = {
        'Authorization': 'Token token=' + args.key,
    }

    output_dir = args.output
    mkdir(output_dir)

    entities = entities_quick
    if args.full:
        entities = entities_full


    for entity in entities:
        data = entity_to_file(entity)
        if entity == 'users':
            users = data
        if isinstance(entities[entity], list):
            for subentity in entities[entity]:
                for item in data:
                    entity_id = item['id']
                    entity_to_file(subentity.format(entity=entity, id=entity_id))


    # Special case for "Response Plays"
    # You must provide a valid email address in the 'From' header to perform this action.
    if args.full:
        for user in users:
            email = user['email']
            local_headers = {
                'From': email,
            }
            entity_to_file('response_plays', local_headers, 'response_plays_{}.json'.format(email))
