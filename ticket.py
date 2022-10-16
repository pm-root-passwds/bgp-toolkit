from arin import *


class Ticket(Arin):
    def _init__(self):
        super().__init__()

    def get_ticket_details(self, ticket_number=None):
        """
        https://www.arin.net/resources/manage/regrws/methods/#get-ticket-details

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        if not ticket_number:
            return  # Something useful

        get = requests.get(
            f"{self.url}/ticket/{ticket_number}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(get.text)

        return get.status_code, json.dumps(doc)

    def get_ticket_summary(self, ticket_number=None):
        """
        https://www.arin.net/resources/manage/regrws/methods/#get-ticket-summary
        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        if not ticket_number:
            return  # Something useful

        get = requests.get(
            f"{self.url}/ticket/{ticket_number}/summary?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(get.text)

        return get.status_code, json.dumps(doc)

    def get_ticket_summaries(self, ticket_type=None, ticket_status=None):
        """
        https://www.arin.net/resources/manage/regrws/methods/#get-ticket-summaries

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        if not ticket_type or not ticket_status:
            return  # Something useful

        get = requests.get(
            f"{self.url}/ticket/summary;{'ticketType=' + ticket_type if ticket_type else ''}{';' if ticket_type and ticket_status else ''}{'ticketStatus=' + ticket_status if ticket_status else ''}=ASN_REQUEST?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(get.text)

        return get.status_code, json.dumps(doc)
