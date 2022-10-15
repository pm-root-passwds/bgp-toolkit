#!/usr/bin/python3
import os
import json
import xmltodict
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

api_key = os.environ.get('ARIN_API_KEY')


class BgpToolkit:
    def __init__(self):
        self.url="https://reg.arin.net"
        # self.

    def by_as_set(self, as_set):
        """

        :param asn
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """
        get = requests.get(f"{self.url}/rest/irr/as-set/{as_set}?apikey={api_key}",
                                headers=headers,
                                )

        doc = xmltodict.parse(get.text)


        return get.status_code, json.dumps(doc)
        # return get.status_code, resp

test = BgpToolkit()
print(test.by_as_set("AS-IONSWITCH"))