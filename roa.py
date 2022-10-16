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


class ROA(Arin):
	def __init__(self):
		super().__init__()

	def get_roa(self, orghandle):
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

	def submit_roa_request(self, orghandle, resource_class):  # TODO: Test me
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