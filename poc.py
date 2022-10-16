from arin import *


class POC(Arin):
    def _init__(self):
        super().__init__()

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
