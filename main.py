#!/usr/bin/python3
import os
import json
import xmltodict
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape
import templates
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PyArin:
    def __init__(self):
        self.url = "https://reg.arin.net/rest"
        self.template_path = templates.__path__[0]
        self.env = Environment(
            loader=FileSystemLoader(self.template_path),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self.headers = json.loads(self.env.get_template("headers.json").render())

        self.api_key = os.environ.get("ARIN_API_KEY")

    def by_as_set(self, as_set):
        """

        :param as-set
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """
        get = requests.get(
            f"{self.url}/irr/as-set/{as_set}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(get.text)

        return get.status_code, json.dumps(doc)
        # return get.status_code, resp

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
            f"{self.url}/ticket/summary;{'ticketType='+ticket_type if ticket_type else ''}{';' if ticket_type and ticket_status else ''}{'ticketStatus='+ticket_status if ticket_status else ''}=ASN_REQUEST?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(get.text)

        return get.status_code, json.dumps(doc)

    def get_roas(self, orghandle):
        """
        https://www.arin.net/resources/manage/regrws/methods/#get-a-list-of-roas-for-an-org

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        get = requests.get(
            f"{self.url}/roa/{orghandle}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(get.text)

        return get.status_code, json.dumps(doc)

    def submit_roa_req(self, orghandle, resource_class):  # TODO: Test me
        """
        https://www.arin.net/resources/manage/regrws/methods/#submit-a-roa-request

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        post = requests.post(
            f"{self.url}/roa/{orghandle};resourceClass={resource_class}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(post.text)

        return post.status_code, json.dumps(doc)

    def delete_roa(self, roahandle, resource_class):  # TODO: Test me
        """
        https://www.arin.net/resources/manage/regrws/methods/#delete-a-roa

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """

        delete = requests.delete(
            f"{self.url}/roa/spec/{roahandle}?apikey={self.api_key}",
            headers=self.headers,
        )

        doc = xmltodict.parse(delete.text)

        return delete.status_code, json.dumps(doc)

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

    def create_poc(
        self,
        first_name=None,
        middle_name=None,
        last_name=None,
        company_name=None,
        contact_type=None,
        email=None,
        phone_description=None,
        phone_number=None,
        phone_extension=None,
        phone_code=None,
        street_address=[],
        city=None,
        postal_code=None,
        comments=[],
        state_province=None,
        coutry_code_2=None,
        reg_date=None,
    ):
        """
        https://www.arin.net/resources/manage/regrws/methods/#get-poc-information

        :param
        :return: Tuple. Index 0 is http status code and index 1 is response dict.
        """
        payload = self.env.get_template("poc_payload.xml").render(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            company_name=company_name,
            contact_type=contact_type,
            email=email,
            phone_description=phone_description,
            phone_number=phone_number,
            phone_extension=phone_extension,
            phone_code=phone_code,
            street_address=street_address,
            city=city,
            postal_code=postal_code,
            comments=comments,
            state_province=state_province,
            coutry_code_2=coutry_code_2,
            reg_date=reg_date,
        )
        print(f"Payload: {payload}")
        print(f"kwargs: {kwargs['first_name']}")
        # get = requests.get(
        #     f"{self.url}/poc/{poc_handle}?apikey={self.api_key}",
        #     headers=self.headers,
        # )
        #
        # doc = xmltodict.parse(get.text)

        return
        # get.status_code, json.dumps(doc)


test = PyArin()
# print(test.get_ticket_summaries(ticket_type="ASN_REQUEST", ticket_status="CLOSED"))
# print(test.get_roas(orghandle='BTL-251'))
# print(test.whowas_asn(asn=20055))
# print(test.req_associations_report())
# print(test.get_ticket_details(ticket_number=f"20221015-X540551"))
# print(test.get_ticket_summary(ticket_number=f"20221015-X540551"))
# print(test.get_poc_info('JNB4-ARIN'))
print(
    test.create_poc(
        first_name="Chris",
        # middle_name=None,
        last_name="Adams",
        company_name="Ziply",
        contact_type="PERSON",
        email="chris.adams@ziply.com",
        # phone_description=None,
        phone_number="5099512726",
        # phone_extension=None,
        # phone_code=None,
        street_address=["3630 E 31st Ave", "Not an apartment"],
        city="Spokane",
        postal_code="99223",
        comments=["First line of comments", "second line of comments"],
        state_province="Wa",
        # coutry_code_2=None,
        # reg_date=None,
    )
)
