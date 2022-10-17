import json
import requests
import xmltodict
from arin import Arin


class Org(Arin):
    def __init__(self):
        super().__init__()

    def get_org_information(self, org_handle):
        """
        https://www.arin.net/resources/manage/regrws/methods/#get-org-information

        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        get = requests.get(
            f"{self.url}/org/{org_handle}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(get.text)

        return get.status_code, json.dumps(doc)

    def add_poc_to_org(self, org_handle, poc_handle, poc_function):
        """
        https://www.arin.net/resources/manage/regrws/methods/#add-poc

        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        put = requests.put(
            f"{self.url}/org/{org_handle}/poc/{poc_handle};pocFunction={poc_function}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(put.text)

        return put.status_code, json.dumps(doc)

    def remove_poc_from_org(self, org_handle, poc_handle, poc_function):
        """
        https://www.arin.net/resources/manage/regrws/methods/#remove-poc

        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        delete = requests.delete(
            f"{self.url}/org/{org_handle}/poc/{poc_handle};pocFunction={poc_function}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(delete.text)

        return delete.status_code, json.dumps(doc)
