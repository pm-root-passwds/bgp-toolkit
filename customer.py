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
from arin import Arin


class Customer(Arin):
    def __init__(self):
        super().__init__()

    def create_recipient_customer(
            self,
            parent_net_handle: str,
            customer_payload: dict,
    ):
        """
        https://www.arin.net/resources/manage/regrws/methods/#create-recipient-customer

        :param parent_net_handle:
        :param customer_payload:
        :return:
        """
        url = f"{self.url}/net/{parent_net_handle}/customer?apikey={self.api_key}"
        template = self.env.get_template('customer_payload.jinja2')
        rendered_payload = template.render(**customer_payload)
        print(url)
        print(rendered_payload)
        r = requests.post(
            url=url,
            headers=self.headers,
            data=rendered_payload
        )
        doc = xmltodict.parse(r.text)
        print(doc)
        return r.status_code, json.dumps(doc)
