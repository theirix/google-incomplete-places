# Google Incomplete Maps Detect

Small script for searching Google Places with a few missing information
fields such as an website or opening hours. Places can be found
by [type](https://developers.google.com/places/supported_types), query, and location.

## Requirements

1. Python3

2. Unofficial [Google Maps API Web Services](https://github.com/googlemaps/google-maps-services-python) python library.
```shell
pip3 install -U googlemaps
``` 
3. Also you need `~/.config/google-incomplete-places/key.json` with the Web Services server key. Format of the file:
```json
{"server_key": "myserverkey"}
```

## Usage

Just launch:
```shell
python3 google-incomplete-places.rb
```
Maximum 61-62 requests are made (3 paginated search requests with 20 results for each page and 1 request per place).
Please take care of your daily API quota (usually 1000 requests per day).

## License

MIT

