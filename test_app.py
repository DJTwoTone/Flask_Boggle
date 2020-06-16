import os
os.environ['FLASK_ENV'] = 'test'

from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


# app.config['TESTING'] = True
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class BoggleTestCase(TestCase):
    """TEST FOR OUR BOGGLE APP"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

#Test if page loads correctly
    def test_index_setup(self):
        with self.client as client:
            # import pdb
            # pdb.set_trace()

            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('form', html)

# Test that items in session are correct for initial use
# Check default length
# Test that items in session are correct for after initial use



# Test if play displays correctly
    def test_play_display(self):
        with self.client as client:
            resp = client.get('/play?length=60&width=5&height=5')
            html = resp.get_data(as_text=True)
            # import pdb
            # pdb.set_trace()

#Test if play responds
    def test_play_response(self):
        with self.client as client:
            resp = client.get('/play?length=60&width=5&height=5')
            status = resp.status_code
            self.assertEqual(status, 200)
    

#Test if play adds board to session
    def test_play_session(self):
        with self.client as client:
            client.get('/play?length=60&width=5&height=5')
            board = session['board']
            self.assertIn('board', session)
            self.assertEqual(len(board), 5)
            self.assertEqual(len(board[0]), 5)
            self.assertIsInstance(board[0][0], str)



#test if html displays correctlt
    def test_play_html(self):
        with self.client as client:
            resp = client.get('/play?length=60&width=5&height=5')
            html = resp.get_data(as_text=True)
            rowCount = html.count('</tr>')
            #how to get the colunm count?
            cellCount = html.count('</td>')
            self.assertEqual(rowCount, 5)
            self.assertEqual(cellCount, 25)
            self.assertIn('<p id="score">0</p>', html)
            self.assertIn('<p id="timer">60</p>', html)


#test if the word_check class functions correctly
    def test_word_check(self):
        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [
                    ['c','a','t','t','y'],
                    ['a','t','e','r','e'],
                    ['t','c','a','y','s']]
                # import pdb
                # pdb.set_trace()
                res1 = self.client.get('/word_check?word=cat')
                self.assertEqual(res1, 'ok')
                res2 = self.client.get('/word_check?word=yes')
                self.assertEqual(res2, 'ok')
                res3 = self.client.get('/word_check?word=supercaliblahblahblah')
                self.assertEqual(res3, 'not-on-board')
                res4 = self.client.get('/word_check?word=ttt')
                self.assertEqual(res4, 'not-word')

    def test_endgame_session(self):
        with self.client as client:
            resp = client.get('/end_game?high_score=100&score=10')
            status = resp.status_code
            high_score = session['high_score']
            game_nums = session['game_nums']
            self.assertEqual(status, 200)
            self.assertEqual(high_score, 100)
            self.assertEqual(game_nums, 5)


