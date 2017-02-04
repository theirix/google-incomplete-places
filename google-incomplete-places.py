#!/usr/bin/env python3
# pylint: disable=C0103
# pylint: disable=missing-docstring
import json
import os
import sys
import time
import googlemaps

def search(gmaps, search_query, search_type, pages, language):
    page_token = None
    page_index = 0
    place_ids = []
    if pages > 3:
        pages = 3
    while True:
        if page_token:
            time.sleep(5)
            response = gmaps.places('', page_token=page_token)
        else:
            response = gmaps.places(search_query, language=language,
                                    location=(55.749780, 37.633992),
                                    radius=15000, type=search_type)
        print(repr(response))
        place_ids.extend(list(result.get('place_id') for result in response.get('results', [])
                              if not result.get('permanently_closed', False)))
        page_token = response.get('next_page_token', None)
        if (page_token is None) or (page_index >= pages):
            break
        print("Using next page token", page_token)
        page_index += 1
    print(place_ids)
    return place_ids

def check_incomplete(gmaps, place_id, language):
    try:
        response = gmaps.place(place_id, language=language)
        url = response.get('result').get('url')
        website = response.get('result').get('website', None)
        opening_hours = response.get('result').get('opening_hours')
        if opening_hours:
            opening_periods = opening_hours.get('periods', None)
        else:
            opening_periods = None
        is_website_ok = not website is None
        is_periods_ok = not (opening_periods is None or len(opening_periods) == 0)

        if not is_website_ok or not is_periods_ok:
            print("\nPlace id {}, url {}".format(place_id, url+'&hl='+language))
            print("Name: ", response.get('result').get('name', None))
            print("Address: ", response.get('result').get('formatted_address', None))
            if not is_website_ok:
                print("No website given")
            if not is_periods_ok:
                print("No periods given")
            print("Should be fixed")
    except Exception: # pylint: disable=broad-except
        print("Got an error for place {}: {}".format(place_id, repr(sys.exc_info())))
        print(repr(response))

def main():
    # logging.basicConfig(level=logging.DEBUG)

    config_dir = os.path.join(os.path.expanduser('~'), '.config', 'google-incomplete-places')
    cache_file = os.path.join(config_dir, 'cache.json')
    cred_file = os.path.join(config_dir, 'key.json')
    with open(cred_file) as file:
        server_key = json.load(file)['server_key']

    pages = 1
    language = 'ru'
    # see https://developers.google.com/places/supported_types
    search_query = 'вело'
    search_type = 'bicycle_store'

    gmaps = googlemaps.Client(key=server_key, queries_per_second=1)

    place_ids = search(gmaps, search_query, search_type, pages, language)
    with open(cache_file, 'w') as file:
        json.dump(place_ids, file)
    print("Saved {} entries to cache".format(len(place_ids)))

    mode = input("Continue (y/n)?")
    if mode == 'y' or mode == 'Y':
        # with open(cache_file) as file:
            # place_ids = json.load(file)
        # print("Loaded {} entries from cache".format(len(place_ids)))
        for place_id in place_ids:
            check_incomplete(gmaps, place_id, language)
            time.sleep(1)

    print("Done")

if __name__ == '__main__':
    main()
