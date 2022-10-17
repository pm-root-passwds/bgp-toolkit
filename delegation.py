#!/usr/bin/python3
import requests
import xmltodict
from arin import Arin


def delegation_key_to_dict(key: dict) -> dict:
    new_key = dict()
    new_key['algorithm'] = int(key['algorithm']['#text'])
    new_key['digest'] = key['digest']
    new_key['digest_type'] = int(key['digestType']['#text'])
    new_key['key_tag'] = int(key['keyTag'])
    if 'ns2:ttl' in key.keys():
        new_key['ttl'] = int(key['ns2:ttl'])
    else:
        new_key['ttl'] = 86400
    return new_key


def delegation_nameserver_to_dict(nameserver: dict) -> dict:
    new_ns = dict()
    return new_ns


class Delegation(Arin):
    """
    https://www.arin.net/resources/manage/regrws/methods/#delegations
    """
    def __init__(self, delegation_name: str):
        super().__init__()
        self.name = delegation_name
        self.config = dict()
        self.keys = set()
        self.payload = str()
        self.nameservers = set()
        self.get()

    def get(self):
        url = f"{self.url}/delegation/{self.name}?apikey={self.api_key}"
        r = requests.get(
            url=url,
            headers=self.headers
        )
        self.config = xmltodict.parse(r.text)
        print(self.config)
        if self.config['delegation']['delegationKeys']:
            keys = self.config['delegation']['delegationKeys']['delegationKey']
            if isinstance(keys, list):
                for dk in keys:
                    new_key = delegation_key_to_dict(dk)
                    self.add_key(**new_key)
            else:
                new_key = delegation_key_to_dict(keys)
                self.add_key(**new_key)
        return r.status_code, self.config

    def rebuild_config(self):
        pass

    def push(self):
        url = f"{self.url}/delegation/{self.name}?apikey={self.api_key}"

        self.rebuild_config()

        r = requests.put(
            url=url,
            headers=self.headers,
            data=self.payload
        )
        self.config = xmltodict.parse(r.text)
        print(self.config)
        return r.status_code, self.config

    def add_key(self, digest: str, digest_type: int, algorithm: int, key_tag: int, ttl: int = 86400):
        """
        :param digest: Digest as string of hex
        :param digest_type:
                1  SHA-1    40
                2  SHA-256  64
                3  MD5      32
                4  SHA-384  96
        :param algorithm:
                5   RSA/SHA-1
                7   RSASHA1-NSEC3-SHA1
                8   RSA/SHA-256
                10  RSA/SHA-512
                13  ECDSA Curve P-256 with SHA-256
                14  ECDSA Curve P-384 with SHA-384
        :param key_tag: 2 byte identifier tag for the key
        :param ttl:
        :return:
        """
        self.keys.add((
            digest,
            digest_type,
            algorithm,
            key_tag,
            ttl
        ))
        return self.keys

    def delete_key(self, digest: str):
        tar = -1
        for i, server in enumerate(self.keys):
            if server[0].lower() == digest.lower():
                tar = i
                break
        if tar > -1:
            self.keys.discard(tar)
        return self.keys

    def add_nameserver(self, nameserver: str, ttl: int = 86400):
        self.nameservers.add((nameserver, ttl))
        return self.nameservers

    def delete_nameserver(self, nameserver: str):
        tar = -1
        for i, server in enumerate(self.nameservers):
            if server[0].lower() == nameserver.lower():
                tar = i
                break
        if tar > -1:
            self.nameservers.discard(tar)
        return self.nameservers

    def delete_all_nameservers(self):
        self.nameservers = set()
        return self.nameservers

    def delete_all_keys(self):
        self.keys = set()
        return self.keys


if __name__ == "__main__":
    test = Delegation('139.83.206.in-addr.arpa.')
    import pprint
    pprint.pprint(test.config, indent=4)

