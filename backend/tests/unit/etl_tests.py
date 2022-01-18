import pytest
import requests
from unittest import TestCase
from pyquery import PyQuery as pq



url = 'https://www.texaslottery.com/export/sites/lottery/Games/Lotto_Texas/index.html'


# class EtlTestFixture(TestCase):

#     def test_get_winning_numbers(self):
#         resp = requests.get(url)

#         self.assertIsNotNone(resp)

def test_get_winning_numbers():
    resp = requests.get(url)

    assert resp is not None