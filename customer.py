#!/usr/bin/python3
import json
import requests
import xmltodict
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

    # UNTESTED
    def get_customer_info(self, customer_handle: str):
        """
        https://www.arin.net/resources/manage/regrws/methods/#get-customer-information

        :param customer_handle:
        :return:
        """
        url = f"{self.url}/customer/{customer_handle}?apikey={self.api_key}"
        r = requests.get(
            url=url,
            headers=self.headers,
        )
        doc = xmltodict.parse(r.text)
        print(doc)
        return r.status_code, json.dumps(doc)

    # UNTESTED
    def delete_customer(self, customer_handle: str):
        """
        https://www.arin.net/resources/manage/regrws/methods/#delete-customer

        :param customer_handle:
        :return:
        """
        url = f"{self.url}/customer/{customer_handle}?apikey={self.api_key}"
        r = requests.delete(
            url=url,
            headers=self.headers,
        )
        doc = xmltodict.parse(r.text)
        print(doc)
        return r.status_code, json.dumps(doc)

    # UNTESTED
    def modify_customer(self, customer_handle: str, customer_payload: dict):
        """
        https://www.arin.net/resources/manage/regrws/methods/#modify-customer

        :param customer_handle:
        :param customer_payload:
        :return:
        """
        url = f"{self.url}/customer/{customer_handle}?apikey={self.api_key}"
        r = requests.post(
            url=url,
            headers=self.headers,
            data=customer_payload
        )
        doc = xmltodict.parse(r.text)
        print(doc)
        return r.status_code, json.dumps(doc)
