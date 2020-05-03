from unittest import TestCase
from app import app
from flask import session

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class BoggleTestCase(TestCase):
    """TEST FOR OUR BOGGLE APP"""

    def test_index(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertIn('table', html)
            self.assertIn('form', html)

    def test_board(self):
        with app.test_client() as client:
            resp = client.get('/')
            self.assertTrue(session['board'])
