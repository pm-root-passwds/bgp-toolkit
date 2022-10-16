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
        print(org_handle)
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


temp = Org()

r = temp.get_org_information("IL-446")
print(r)
