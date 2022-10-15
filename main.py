#!/usr/bin/python3
import os
import json
import xmltodict
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape
import templates
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PyArin:
    def __init__(self):
        self.url="https://reg.arin.net"
        self.template_path = templates.__path__[0]
        self.env = Environment(loader=FileSystemLoader(self.template_path),
                          autoescape=select_autoescape(['html', 'xml']))
        self.headers = json.loads(self.env.get_template('headers.json').render())

        self.api_key = os.environ.get('ARIN_API_KEY')
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

test = PyArin()
print(test.by_as_set("AS-IONSWITCH"))