#!/usr/bin/python3
import json
import os
import re
import requests
import templates
import urllib3
import xmltodict
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sys import prefix


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Arin:
    def __init__(self):
        self.url = "https://reg.arin.net/rest"
        self.template_path = templates.__path__[0]
        self.env = Environment(
            loader=FileSystemLoader(self.template_path),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self.headers = json.loads(self.env.get_template("headers.json").render())
        self.headers_rpsl = json.loads(self.env.get_template("headers_rpsl.json").render())
        self.api_key = os.environ.get("ARIN_API_KEY")
