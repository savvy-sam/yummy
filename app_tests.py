import unittest

from app import app

class TestApp(unittest.TestCase):
    

    def test_index(self):
        indx=self.app.get('/')
        self.assertEqual(indx.status_code, 200) 