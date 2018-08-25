from Points import PointCounter
from Deckdata import deck, Crib, Scoring
from Gameplay import gameplay
from Player import player1, player2, clear_players
from Game import Game
from flask import Flask, render_template, request, url_for, redirect, make_response, jsonify
from flask_restful import Api, Resource
from random import randint
import os
import sqlite3

app = Flask(__name__, template_folder=os.getcwd() + '/templates')
api = Api(app)
headers = {'Content-Type': 'text/html'}
conn = sqlite3.connect('Session.db', check_same_thread=False)
c = conn.cursor()


@app.route('/check_for_game')
def check_for_session():
    ip = request.remote_addr

    for i in c.execute("SELECT IP FROM sessions"):
        if ip == i[0]:
            return redirect('/cardselect')
    return 'You do not have a session' \
           '<form method="get" action="/">' \
           '<p align="center">' \
           '<input type="submit" value="Back to main screen" style="height:50px; width:200px" align="center"/>' \
           '</p>' \
           '</form>'


def quick_check():
    ip = request.remote_addr
    for i in c.execute("SELECT IP FROM sessions"):
        if ip == i[0]:
            return True


@app.route('/')
def base():
    return render_template('Start_page.html')


@app.route('/new_session')
def create_session():
    session_id = randint(10000000, 99999999)
    c.execute("DELETE FROM sessions WHERE IP = ?", (request.remote_addr,))
    full2 = Game('player1', 'player2')
    full2 = full2.serialize()
    print(full2)
    c.execute("INSERT INTO sessions(sessionID, player1score, player2score, IP, turn, other_turn) "
              "VALUES(?, ?, ?, ?, ?, ?)",
              (session_id, 0, 0, request.remote_addr, full2['turn'], full2['other_turn']))
    conn.commit()
    return redirect('/cardselect')


def reset():
    global Played
    Played = []
    gameplay.reset()


def js():
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


@app.route('/favicon.ico')
def icon():
    return 'LOGO_icon.ico'


@app.route('/onload')
def onload():
    turn = c.execute("SELECT turn FROM sessions WHERE IP = ?", (request.remote_addr,))
    turn = [i[0] for i in turn][0]
    print(turn)
    if turn == 'player2':
        Played.append(player2Choices[0])

    return jsonify(played=[e.serialize() for e in Played])


@app.route('/image_movement/<card>')
def play(card):
    Played.append(keys[card.strip('.')])
    if len(Played) < 8:
        Played.append(player2.best_play(Played, player2Choices))
    return jsonify(played=[card.serialize() for card in Played])


@app.route('/bot_cards')
def cards():
    return jsonify([x[1].serialize() for x in keys.items()])


@app.route('/image_movement2')
def scoreUpdate():
    conn = sqlite3.connect('Session.db')
    sql = conn.cursor()
    global point1, point2
    gameplay.reset()
    clear_players()

    point1 = PointCounter(player1Choices, True)
    point2 = PointCounter(player2Choices, True)

    info = sql.execute("SELECT turn, other_turn FROM sessions WHERE IP = ?", (request.remote_addr,))
    lil()

    info = list(info)
    game = Game(info[0][0], info[0][1])

    for i in range(len(Played)):
        if i % 2 == 0:
            player1.play_card(Played[i], game.turn, gameplay)
        else:
            player2.play_card(Played[i], game.other_turn, gameplay)
    if len(Played) == 8:
        deck.set_extra()
        player1.build('1')
        player2.build('2')
        game.switch()

        deck.shuffle()
        crib = Crib(crib_cards)
        crib.score()

        handScores.update(point1.calculation(), point2.calculation())
        handScores.update(player1.points_earned, player2.points_earned, crib.points, temp)

        sql.execute("UPDATE sessions SET turn = ?, other_turn = ? WHERE IP = ?",
                    (game.turn, game.other_turn, request.remote_addr))
        sql.execute("UPDATE sessions SET player1score = ?, player2score = ? WHERE IP = ?",
                    (handScores.p1score, handScores.p2score, request.remote_addr,))
        conn.commit()

        pips = gameplay.pips
        reset()

        return jsonify([player1.points_earned, player2.points_earned, [' ' + pip for pip in pips],
                        handScores.p1score, handScores.p2score,
                        crib.points, [x.serialize() for x in crib_cards], game.other_turn.strip('player'),
                        point1.calculation(), point2.calculation()])
    else:
        return jsonify([player1.points_earned, player2.points_earned, gameplay.pips,
                        handScores.p1score, handScores.p2score, gameplay.current_value])


@app.route('/cardselect')
def index():
    global handScores

    for i in c.execute("SELECT * FROM sessions WHERE IP = ?", (request.remote_addr,)):
        handScores = Scoring(i[1], i[2])

    if ([x for x in c.execute("SELECT player1score FROM sessions WHERE IP = ?", (request.remote_addr,))][0][0]) >= 121:
        return redirect(url_for('end', winner='player 1'))
    elif (
        [x for x in c.execute("SELECT player2score FROM sessions WHERE IP = ?", (request.remote_addr,))][0][0]) >= 121:
        return redirect(url_for('end', winner='player 2'))
    return render_template('Card_selection.html',
                           image_name=player1.hand[0].path, image_name2=player1.hand[1].path,
                           image_name3=player1.hand[2].path, image_name4=player1.hand[3].path,
                           image_name5=player1.hand[4].path, image_name6=player1.hand[5].path)


class End(Resource):
    def get(self):
        winner = request.args['winner']
        print(winner)
        score1 = handScores.p1score
        score2 = handScores.p2score
        info = c.execute("SELECT other_turn FROM sessions WHERE IP = ?", (request.remote_addr,))
        turn = list(info)[0][0]
        c.execute("DELETE FROM sessions WHERE IP = ?", (request.remote_addr,))
        conn.commit()
        handScores.reset()

        return make_response(render_template('End.html').format(winner, score1, score2, turn), 200, headers)


@app.route('/<selections>', methods=['GET', 'POST'])
def selection(selections):
    global player1Choices, player2Choices, page, crib_cards, temp, handScores, turns
    for i in c.execute("SELECT * FROM sessions WHERE IP = ?", (request.remote_addr,)):
        handScores = Scoring(i[1], i[2])
    turn = c.execute("SELECT turn, other_turn FROM sessions WHERE IP = ?", (request.remote_addr,))
    turns = list(turn)

    turns = Game(turns[0][0], turns[0][1])
    player1Choices = []
    player2Choices = []
    player2best = player2.best_hand()
    crib_cards = []
    temp = turns.turn
    selections = selections.split(',')
    reset()
    for i in range(6):
        if selections[i] == 'true':
            player1Choices.append(player1.hand[i])
        else:
            crib_cards.append(player1.hand[i])
    for i in range(6):
        if player2.hand[i] in player2best:
            player2Choices.append(player2.hand[i])
        else:
            crib_cards.append(player2.hand[i])

    point1 = PointCounter(player1Choices, True)
    p1_points = point1.calculation()  # Calculation of each players points
    page = make_response(render_template('Main_screen.html',
                                         extra=deck.Extra[0].path,
                                         image_name=player1Choices[0].path, image_name2=player1Choices[1].path,
                                         image_name3=player1Choices[2].path, image_name4=player1Choices[3].path).format(
        turns.turn.strip('player'),
        p1_points, handScores.p1score, handScores.p2score, turns.turn.strip('player')), 200, headers)
    js()
    clear_players()

    return check(turns)


def check(turns):
    if turns.turn == 'player1':
        if get_winner('player1') != 'nah':
            return redirect(url_for('end', winner=get_winner('player1')))
        else:
            return page
    else:
        if get_winner('player2') != 'nah':
            return redirect(url_for('end', winner=get_winner('player2')))
        else:
            return page


def get_winner(starting_player):
    if starting_player == 'player1':
        if handScores.p1score >= 121:
            return 'player1'
        elif handScores.p2score >= 121:
            return 'player2'
        else:
            return 'nah'
    else:
        if handScores.p2score >= 121:
            return 'player2'
        elif handScores.p1score >= 121:
            return 'player1'
        else:
            return 'nah'


def lil():
    if ([x for x in c.execute("SELECT player1score FROM sessions WHERE IP = ?", (request.remote_addr,))][0][0]) + \
        point1.calculation() >= 121:

        return redirect(url_for('end', winner='player 1'))
    elif ([x for x in c.execute("SELECT player2score FROM sessions WHERE IP = ?", (request.remote_addr,))][0][0]) + \
        point2.calculation() >= 121:

        return redirect(url_for('end', winner='player 2'))


api.add_resource(End, '/end')

if __name__ == '__main__':
    Played = []
    deck.set_extra()
    player1.build('1')
    player2.build('2')
    try:
        c.execute(
            "CREATE TABLE sessions(sessionID int, player1score int, player2score int, IP TEXT, turn TEXT, other_turn TEXT,"
            "UNIQUE(sessionID, player1score, player2score, IP, turn, other_turn))")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    app.run(host='0.0.0.0', port=80, debug=False)
