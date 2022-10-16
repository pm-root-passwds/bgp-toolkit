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


class IRR(Arin):
    def __init__(self):
        self.nl = '\n'
        super().__init__()

    def create_route(self, prefix, asn, descr, admin_c, tech_c, mnt_by):
        body = f"""route6: {prefix}
origin: {asn}
descr: {descr}
admin-c: {admin_c}
tech-c: {tech_c}
mnt-by: {mnt_by}
source: ARIN"""
        req = requests.post(
            f'{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}',
            headers=self.headers_rpsl,
            data=body,
        )
        return req

    def create_route6(self, prefix, asn, descr, admin_c, tech_c, mnt_by):
        body = f"""route6: {prefix}
origin: {asn}
descr: {descr}
admin-c: {admin_c}
tech-c: {tech_c}
mnt-by: {mnt_by}
source: ARIN"""
        req = requests.post(
            f'{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}',
            headers=self.headers_rpsl,
            data=body,
        )
        return req

    def get_route_object(self, prefix, asn):
        get = requests.get(
            f'{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}',
            headers=self.headers_rpsl
        )
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
        body = f"""route: {prefix}
origin: {asn}
descr: {descr}
admin-c: {existing['admin-c']}
tech-c: {existing['tech-c']}
mnt-by: {existing['mnt-by']}
source: ARIN"""
        put = requests.put(
            f'{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}',
            headers=self.headers_rpsl,
            data=body
        )
        return put

    def modify_route6_object(self, prefix, asn, descr):
        existing = self.get_route_object(prefix, asn)
        body = (
            f'route: {prefix}\n'
            f'origin: {asn}\n'
            f'descr: {descr}\n'
            f"admin-c: {existing['admin-c']}\n"
            f"tech-c: {existing['tech-c']}\n"
            f"mnt-by: {existing['mnt-by']}\n"
            "source: ARIN")
        put = requests.put(
            f"{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}",
            headers=self.headers_rpsl,
            data=body
        )
        return put

    def delete_route_object(self, prefix, asn):
        delete = requests.delete(
            f"{self.url}/irr/route/{prefix}/{asn}?apikey={self.api_key}",
            headers=self.headers_rpsl
        )
        return delete
    
    #AUT-NUM
    def create_autnum(self,asn, as_name, descr, admin_c, tech_c, mnt_by, member_of, importstatement, exportstatement, **kwargs):
        body = (
            f'aut-num: {asn}{self.nl}'
            f'as-name: {as_name}{self.nl}'
            f'descr: {descr}{self.nl}'
            f'import: {importstatement}{self.nl}'
            f'export: {exportstatement}{self.nl}'
            f'admin-c: {admin_c}{self.nl}'
            f'tech-c: {tech_c}{self.nl}'
            f'mnt-by: {mnt_by}{self.nl}'
            f'{"default: "+kwargs.get("default")+"{self.nl}" if kwargs.get("default") else ""}'
            f'{"memberOf: "+kwargs.get("member_of")+"{self.nl}" if kwargs.get("member_of") else ""}'
            f'{"mpDefault: "+kwargs.get("mpDefault")+"{self.nl}" if kwargs.get("mpDefault") else ""}'
            f'{"mpExport: "+kwargs.get("mpExport")+"{self.nl}" if kwargs.get("mpExport") else ""}'
            f'{"mpImport: "+kwargs.get("mpImport")+"{self.nl}" if kwargs.get("mpImport") else ""}'
        )
        post = requests.post(
            f"{self.url}/irr/aut-num/{asn}?apikey={self.api_key}",
            headers=self.headers_rpsl,
            body=body
        )
        return post
    
    def get_autnum(self, asn):
        get = requests.get(
            f'{self.url}/irr/aut-num/{asn}?apikey={self.api_key}',
            headers=self.headers
        )
        xmldict = xmltodict.parse(get.text)
        response = {
            "autnum": xmldict['autnum']['asNumber'],
            "asName": xmldict['autnum']['asName'],
            "orgHandle": xmldict['autnum']['orgHandle'],
            "description": xmldict['autnum']['description']['line']['#text'],
            "lastModifiedDate": xmldict['autnum']['lastModifiedDate'],
            "memberOf": xmldict['autnum']['memberOf']['@name'],
            "pocs": xmldict['autnum']['pocLinks']
        }
        return response

    def delete_autnum(self,asn):
        delete = requests.delete(
            f'{self.url}/irr/aut-num/{asn}?apikey={self.api_key}',
            headers=self.headers
        )
        return delete
    
    #AS-SET
    def create_as_set(self, as_set, descr, admin_c, tech_c, mnt_by, members, orghandle):
        memberlist = ""
        for member in members:
            memberlist+="members: "+member+self.nl
        body = (
            f'as-set: {as_set}{self.nl}'
            f'mnt-by: {mnt_by}{self.nl}'
            f'descr: {descr}{self.nl}'
            f'tech-c: {tech_c}{self.nl}'
            f'admin-c: {admin_c}{self.nl}'
            f'{memberlist}'
            f'source: ARIN'
        )
        post = requests.post(
            f'{self.url}/irr/as-set?apikey={self.api_key}&orgHandle={orghandle}',
            headers=self.headers_rpsl,
            data=body
        )
        print(body)
        return post

    def get_as_set(self, as_set):
        get = requests.get(
            f'{self.url}/irr/as-set/{as_set}?apikey={self.api_key}',
            headers=self.headers
        )
        xml = xmltodict.parse(get.text)
        members = []
        for member in xml['asSet']['members']['member']:
            members.append(member['@name'])
        response = {
            "name": xml['asSet']['name'],
            "members": members,
            "description": xml['asSet']['description']['line']['#text'],
            "orgHandle": xml['asSet']['orgHandle'],
            "lastModifiedDate": xml['asSet']['lastModifiedDate'],
            "creationDate": xml['asSet']['creationDate'],
            "tech-c": xml['asSet']['pocLinks']['pocLinkRef'][0]['@handle'],
            "admin-c": xml['asSet']['pocLinks']['pocLinkRef'][1]['@handle']
        }
        return response
    
    def add_member_as_set(self, as_set, asn):
        memberlist=""
        asset = self.get_as_set(as_set=as_set)
        asset['members'].append(asn)
        for member in asset['members']:
            memberlist+="members: "+member+self.nl
        body = (
            f'as-set: {as_set}{self.nl}'
            f'descr: {asset["description"]}{self.nl}'
            f'{memberlist}'
            f'mnt-by: MNT-{asset["orgHandle"]}{self.nl}'
            f'tech-c: {asset["tech-c"]}{self.nl}'
            f'admin-c: {asset["admin-c"]}{self.nl}'
            f'source: ARIN'
        )
        put = requests.put(
            f'{self.url}/irr/as-set/{as_set}?apikey={self.api_key}',
            headers = self.headers_rpsl,
            data = body
        )
        print(body)
        return put