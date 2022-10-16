#!/usr/bin/python3
import requests
import xmltodict
from arin import Arin


class Delegation(Arin):
    def __init__(self):
        super().__init__()
