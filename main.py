#!/usr/bin/python3
import os
import json
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape
import templates
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

template_path = templates.__path__[0]

template_path = templates.__path__[0]
env = Environment(loader=FileSystemLoader(template_path),
                        autoescape=select_autoescape(['html', 'xml']))
headers = json.loads(env.get_template('headers.json').render())

api_key = "API-324C-1669-469F-9148"
url = f"https://reg.arin.net"


def test(as_set):
    """

    :param asn
    :return: Tuple. Index 0 is http status code and index 1 is response dict.
    """
    post = requests.get(f"{url}/rest/irr/as-set/{as_set}?apikey={api_key}",
                            headers=headers,
                            )

    resp = post.json()

    return post.status_code, resp

test("AS-IONSWITCH")