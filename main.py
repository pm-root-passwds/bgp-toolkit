#!/usr/bin/python3
import os
import json
from sys import prefix
import xmltodict
import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape
import templates
import urllib3
import re

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
        self.headers_rpsl = json.loads(self.env.get_template("headers_rpsl.json").render())
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
###IRR###
    def create_route(self, prefix, asn, descr, admin_c, tech_c, mnt_by):
        body = (f"""route: {prefix}
origin: {asn}
descr: {descr}
admin-c: {admin_c}
tech-c: {tech_c}
mnt-by: {mnt_by}
source: ARIN""")
        req = requests.post(f'{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}', 
        headers=self.headers_rpsl,
        data=body,
        )
        return req

    def create_route6(self, prefix, asn, descr, admin_c, tech_c, mnt_by):
        body = (f"""route6: {prefix}
origin: {asn}
descr: {descr}
admin-c: {admin_c}
tech-c: {tech_c}
mnt-by: {mnt_by}
source: ARIN""")
        req = requests.post(f'{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}', 
        headers=self.headers_rpsl,
        data=body,
        )
        return req
    

    def get_route_object(self, prefix, asn):
        get = requests.get(f'{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}',
        headers=self.headers_rpsl)
        splitter = re.compile(r'^(\S+): +(.*)$')
        lines = get.text.split('\n')
        results = dict()
        for line in lines:
            match = splitter.findall(line)
            if match:
                results[match[0][0]] = match[0][1]
        return results

    def modify_route_object(self, prefix, asn, descr):
        existing = self.get_route_object(prefix, asn)
        body = (f"""route: {prefix}
origin: {asn}
descr: {descr}
admin-c: {existing['admin-c']}
tech-c: {existing['tech-c']}
mnt-by: {existing['mnt-by']}
source: ARIN""")
        put = requests.put(f'{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}',
        headers=self.headers_rpsl,
        data = body)
        return put

    def modify_route6_object(self, prefix, asn, descr):
        existing = self.get_route_object(prefix, asn)
        body = (f"""route6: {prefix}
origin: {asn}
descr: {descr}
admin-c: {existing['admin-c']}
tech-c: {existing['tech-c']}
mnt-by: {existing['mnt-by']}
source: ARIN""")
        put = requests.put(f"{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}",
        headers=self.headers_rpsl,
        data = body)
        return put

    def delete_route_object(self, prefix, asn):
        delete = requests.delete(f"{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}", headers=headers_rpsl)
        return delete

test = PyArin()
# print(test.get_ticket_summaries(ticket_type="ASN_REQUEST", ticket_status="CLOSED"))
# print(test.get_roas(orghandle='BTL-251'))
# print(test.whowas_asn(asn=20055))
print(test.req_associations_report())
