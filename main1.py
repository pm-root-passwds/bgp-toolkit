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


