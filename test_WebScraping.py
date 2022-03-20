import unittest
from WebScraping import main

class TestWebScraping(unittest.TestCase):

  def test_response_code(self):
    results = main.response_code()
    self.assertEqual(results,200) 
