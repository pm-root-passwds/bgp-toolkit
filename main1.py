import os
import json
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape
from . import templates
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

template_path = templates.__path__[0]
env = Environment(loader=FileSystemLoader(self.template_path),
                        autoescape=select_autoescape(['html', 'xml']))
headers = json.loads(self.env.get_template('headers.json').render())

api_key = "API-324C-1669-469F-9148"
url = f"https://reg.arin.net"


def test(self, as_set):
    """

    :param asn
    :return: Tuple. Index 0 is http status code and index 1 is response dict.
    """
    post = requests.get(f"{url}/rest/irr/as-set/{as_set}?apikey={api_key}",
                            headers=self.headers,
                            )

    resp = post.json()

    return post.status_code, resp

