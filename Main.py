from Points import PointCounter
from Deckdata import deck, Crib, Scoring
from Gameplay import gameplay
from Player import player1, player2, clearplayers
from flask import Flask, render_template, request, url_for, redirect, make_response
from flask_restful import Api, Resource
from random import randint
import os
import sqlite3
app = Flask(__name__, template_folder=os.getcwd() + '/templates')
api = Api(app)
headers = {'Content-Type': 'text/html'}
Played = []


def check_for_session(ip):
    global sessionID
    conn = sqlite3.connect('Session.db')
    c = conn.cursor()
    for i in c.execute("SELECT IP, sessionID FROM sessions"):
        if ip == i[0]:
            sessionID = i[1]
            return True


@app.route('/')
def create_session():
    global c, conn, sessionID
    conn = sqlite3.connect('Session.db')
    c = conn.cursor()
    int = randint(10000000, 99999999)
    print(request.remote_addr)
    if check_for_session(request.remote_addr) != True:
        c.execute("INSERT OR IGNORE INTO sessions(sessionID, player1score, player2score, IP) VALUES(?, ?, ?, ?)",
                  (int, 0, 0, request.remote_addr))
        conn.commit()
    else:
        pass
    for i in c.execute("SELECT sessionID FROM sessions WHERE IP = ?", (request.remote_addr,)):
        sessionID = i[0]
        print(i[0])
        break
    print(sessionID)
    return redirect('/cardselect')


def reset():
    global Played
    Played = []
    gameplay.reset()


def update():
    global keys
    keys = {
        'card1': player1Choices[0],
        'card2': player1Choices[1],
        'card3': player1Choices[2],
        'card4': player1Choices[3],
        'card5': player2Choices[0],
        'card6': player2Choices[1],
        'card7': player2Choices[2],
        'card8': player2Choices[3]}


class Game:
    def __init__(self, turn, other_turn):
        self.turn = turn
        self.other_turn = other_turn

    def player_turn(self, players_turn, card_selected):
        if players_turn == 'player1':
            player1.play_card(card_selected, players_turn)
        if players_turn == 'player2':
            player2.play_card(card_selected, players_turn)

    
    def switch(self):
        self.turn, self.other_turn = self.other_turn, self.turn


full = Game('player1', 'player2')


@app.route('/sessionID')
def sessionID():
    return str(sessionID)


@app.route('/favicon.ico')
def icon():
    return 'LOGO_icon.ico'


@app.route('/image_movement/<card>')
def play(card):
    card = card.strip('.')
    Played.append(keys[card])
    card2 = 'card' + str(int(card.strip('card')) + 4)
    Played.append(keys[card2])
    return str(keys[card]) + '/' + str(keys[card2])


@app.route('/image_movement2')
def scoreUpdate():
    conn = sqlite3.connect('Session.db')
    c = conn.cursor()
    gameplay.reset()
    clearplayers()
    for i in range(len(Played)):
        if i % 2 == 0:
            turn = 'player1'
        else:
            turn = 'player2'
        full.player_turn(turn, Played[i])

    if len(Played) == 8:
        crib = Crib(full.turn, crib_cards)  # Calculation of crib points
        crib.score()
        handScores.update(player1.points_earned, player2.points_earned, crib.points, temp)
        c.execute("UPDATE sessions SET player1score = ? WHERE IP = ?", (handScores.p1score, request.remote_addr,))
        c.execute("UPDATE sessions SET player2score = ? WHERE IP = ?", (handScores.p2score, request.remote_addr,))
        conn.commit()
        pips = gameplay.pips
        reset()

        return str(player1.points_earned) + '_' + str(player2.points_earned) + '_' + str(pips) + '_' + \
               str(handScores.p1score) + '_' + str(handScores.p2score) + '_' + str(crib.points) + '_' + str(crib_cards) \
               + '_' + str(full.other_turn.strip('player'))
    else:
        return str(player1.points_earned) + '_' + str(player2.points_earned) + '_' + str(gameplay.pips) + '_' + \
               str(handScores.p1score) + '_' + str(handScores.p2score)


@app.route('/cardselect')
def index():
    player1.build('1')
    player2.build('2')
    return render_template('Card_selection.html',
                           image_name=player1.hand[0].path, image_name2=player1.hand[1].path,
                           image_name3=player1.hand[2].path, image_name4=player1.hand[3].path,
                           image_name5=player1.hand[4].path, image_name6=player1.hand[5].path)


class End(Resource):
    def get(self):
        conn = sqlite3.connect('Session.db')
        c = conn.cursor()
        winner = request.args['winner']
        score1 = handScores.p1score
        score2 = handScores.p2score
        c.execute("UPDATE sessions SET player1score = ? WHERE IP = ?", (0, request.remote_addr,))
        c.execute("UPDATE sessions SET player2score = ? WHERE IP = ?", (0, request.remote_addr,))
        conn.commit()
        handScores.reset()
        return make_response(render_template('End.html').format(winner, score1, score2, full.turn), 200, headers)


@app.route('/<selections>/<int:sessionID>', methods=['GET', 'POST'])
def selection(selections, sessionID):
    global player1Choices, player2Choices, full, page, crib_cards, temp, handScores
    conn = sqlite3.connect('Session.db')
    c = conn.cursor()
    print(sessionID)
    ip = request.remote_addr
    print(ip)
    for i in c.execute("SELECT * FROM sessions WHERE IP = ?", (ip,)):
        handScores = Scoring(i[1], i[2])
    player1Choices = []
    player2Choices = []
    crib_cards = []
    temp = full.turn
    selections = selections.split(',')

    for i in range(len(selections)):
        if selections[i] == 'true':
            player1Choices.append(player1.hand[i])
            player2Choices.append(player2.hand[i])
        else:
            crib_cards.append(player1.hand[i])
            crib_cards.append(player2.hand[i])

    update()  # refreshes key for js
    point1 = PointCounter(player1Choices)
    p1_points = point1.calculation()  # Calculation of each players points
    point2 = PointCounter(player2Choices)
    p2_points = point2.calculation()

    handScores.update(p1_points, p2_points)
    print(handScores.p1score, handScores.p2score)
    c.execute("UPDATE sessions SET player1score = ? WHERE IP = ?", (handScores.p1score, ip,))
    c.execute("UPDATE sessions SET player2score = ? WHERE IP = ?", (handScores.p2score, ip,))
    conn.commit()
    page = make_response(render_template('Main_screen.html',
                                         extra=deck.Extra[0].path,
                                         image_name=player1Choices[0].path, image_name2=player1Choices[1].path,
                                         image_name3=player1Choices[2].path, image_name4=player1Choices[3].path).format(
        full.turn.strip('player'),
        p1_points,
        handScores.p1score, handScores.p2score,
        full.turn.strip('player')), 200, headers)  # building main template

    deck.shuffle()
    clearplayers()
    # Checking to see if anyone won
    return check()


def check():
    if full.turn == 'player1':
        full.switch()
        if handScores.p1score >= 121:
            return redirect(url_for('end', winner='player 1'))
        elif handScores.p2score >= 121:
            return redirect(url_for('end', winner='player 2'))
        else:
            return page
    else:
        full.switch()
        if handScores.p2score >= 121:
            return redirect(url_for('end', winner='player 2'))
        elif handScores.p1score >= 121:
            return redirect(url_for('end', winner='player 1'))
        else:
            return page


api.add_resource(End, '/end')

if __name__ == '__main__':
    conn = sqlite3.connect('Session.db')
    c = conn.cursor()
    try:
        c.execute(
            "CREATE TABLE sessions(sessionID int, player1score int, player2score int, IP TEXT, UNIQUE(sessionID, player1score, player2score, IP))")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    app.run(host='0.0.0.0', port=80, debug=False)
