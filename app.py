from flask import Flask, request, render_template, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle


app = Flask(__name__)
app.config['SECRET_KEY'] = 'booglybogglydoo'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)





boggle_game = Boggle(width=5, height=5)
# this is global


@app.route('/')
def boggle_home():
    """Start and setup screen for Boggle"""
    return render_template('index.html')

@app.route('/play')
def boggle_play():
    """Makes and inits the board to begin game play"""
    time = int(request.args['length'])
    width = int(request.args['width'])
    height = int(request.args['height'])
    boggle_game = Boggle(width, height)
    # this is local
    boggle_board = boggle_game.make_board()
    
    session['board'] = boggle_board
    try:
        games = session['game_nums']
    except KeyError:
        games = 0
    try:
        high_score = session['high_score']
    except KeyError:
        high_score = 0
    print(session)
    return render_template('play.html', boggle_board=boggle_board, games=games, high_score=high_score, time=time)

@app.route('/word_check')
def word_check():
    """Takes in a word from a JS request and returns whether it is a valid word or not"""
    word = request.args['word']
    boggle_board = session['board']
    res = boggle_game.check_valid_word(boggle_board, word)
    # this calls on the global
    # I'm not really sure why they want us to jsonify this data
    return res

@app.route('/end_game')
def end_game():
    games = request.args['games_num']
    high_score = request.args['high_score']
    score = request.args['score']
    session['game_nums'] = games
    session['high_score'] = high_score
    return render_template('endgame.html', games=games, high_score=high_score, score=score)