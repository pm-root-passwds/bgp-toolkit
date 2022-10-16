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


class Report(Arin):
    def __init__(self):
        super().__init__()

    def whowas_asn(self, asn):  # TODO: Getting a 401?
        """
        https://www.arin.net/resources/manage/regrws/methods/#request-whowas-asn-report

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        get = requests.get(
            f"{self.url}/report/whoWas/asn/{asn}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(get.text)

        return get.status_code, json.dumps(doc)

    def whowas_ip(self, ip):  # TODO: probably getting a 401 just like above
        """
        https://www.arin.net/resources/manage/regrws/methods/#request-whowas-net-report

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        get = requests.get(
            f"{self.url}/report/whoWas/net/{ip}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(get.text)

        return get.status_code, json.dumps(doc)

    def req_associations_report(self):
        """
        https://www.arin.net/resources/manage/regrws/methods/#request-associations-report

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        get = requests.get(
            f"{self.url}/report/associations?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(get.text)

        return get.status_code, json.dumps(doc)

