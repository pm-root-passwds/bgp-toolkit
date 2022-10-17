#!/usr/bin/python3
import json
import requests
import xmltodict
from arin import Arin


class POC(Arin):
    def __init__(self):
        super().__init__()
        self.template = self.env.get_template("poc_payload.xml")

    def get_poc_info(self, poc_handle):
        """
        https://www.arin.net/resources/manage/regrws/methods/#get-poc-information

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        get = requests.get(
            f"{self.url}/poc/{poc_handle}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(get.text)

        return get.status_code, json.dumps(doc)

    def create_poc(self, makelink=False, **kwargs):
        """
        https://www.arin.net/resources/manage/regrws/methods/#create-poc

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """
        if makelink:
            makelink = "true"
        else:
            makelink = "false"

        payload = self.template.render(**kwargs)
        print(f"Payload: {payload}")
        post = requests.post(
            f"{self.url}/poc;makeLink={makelink}?apikey={self.api_key}",
            headers=self.headers,
            data=payload,
        )

        doc = xmltodict.parse(post.text)
        print(f"Response: {doc}")
        return post.status_code, json.dumps(doc)

    def modify_poc(self, poc_handle, **kwargs):
        """
        https://www.arin.net/resources/manage/regrws/methods/#modify-poc

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """
        _, get_poc = self.get_poc_info(poc_handle)
        get_poc = json.loads(get_poc)
        payload = self.poc_payload.render(
            handle=poc_handle,
            registration_date=get_poc["poc"]["registrationDate"],
            **kwargs,
        )

        put = requests.put(
            f"{self.url}/poc/{poc_handle}?apikey={self.api_key}",
            headers=self.headers,
            data=payload,
        )
        doc = xmltodict.parse(put.text)

        return put.status_code, json.dumps(doc)

    def delete_poc(self, poc_handle, **kwargs):
        """
        https://www.arin.net/resources/manage/regrws/methods/#delete-poc

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """
        delete = requests.delete(
            f"{self.url}/poc/{poc_handle}?apikey={self.api_key}",
            headers=self.headers,
        )
        doc = xmltodict.parse(delete.text)

        return delete.status_code, json.dumps(doc)
