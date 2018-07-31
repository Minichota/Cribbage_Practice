from Points import PointCounter
from Deckdata import handScores, deck, Crib
from Gameplay import score
from Player import player1, player2, clearplayers
from flask import Flask, render_template, request, url_for, redirect, make_response
from flask_restful import Api, Resource
import os

app = Flask(__name__, template_folder=os.getcwd() + '/templates')
api = Api(app)
headers = {'Content-Type': 'text/html'}
Played = []


def reset():
    global Played
    Played = []
    score.reset()


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
    def __init__(self, turn, otherturn):
        self.turn = turn
        self.otherturn = otherturn

    def playerturn(self, playersturn, cardselected):
        if playersturn == 'player1':
            player1.play_card(cardselected, playersturn)
        if playersturn == 'player2':
            player2.play_card(cardselected, playersturn)

    def switch(self):
        self.turn, self.otherturn = self.otherturn, self.turn


full = Game('player1', 'player2')


@app.route('/image_movement/<card>')
def play(card):
    card = card.strip('.')
    Played.append(keys[card])
    return str(keys[card])


@app.route('/image_movement2')
def scoreUpdate():
    if len(Played) == 8:
        score.reset()
        clearplayers()
        handScores.update(player1.pointsearned, player2.pointsearned, crib.points, temp)

    temp1, temp2 = handScores.p1score, handScores.p2score
    score.reset()
    clearplayers()

    for i in range(len(Played)):
        if i % 2 == 0:
            turn = 'player1'
        else:
            turn = 'player2'
        full.playerturn(turn, Played[i])
    return str(player1.pointsearned) + '_' + str(player2.pointsearned) + '_' + str(score.pips) + '_' + \
           str(temp1) + '_' + str(temp2) + '_' + str(crib.points) + '_' + str(crib_cards) + '_' + \
           str(full.turn.strip('player'))


@app.route('/')
def index():
    player1.build('1')
    player2.build('2')
    return render_template('Card_selection.html',
                           image_name=player1.hand[0].path, image_name2=player1.hand[1].path,
                           image_name3=player1.hand[2].path, image_name4=player1.hand[3].path,
                           image_name5=player1.hand[4].path, image_name6=player1.hand[5].path)


class End(Resource):
    def get(self):
        winner = request.args['winner']
        score1 = handScores.p1score
        score2 = handScores.p2score
        handScores.reset()
        return make_response(render_template('End.html').format(winner, score1, score2, full.turn), 200, headers)


@app.route('/<selections>', methods=['GET', 'POST'])
def selection(selections):
    global player1Choices, player2Choices, full, page, crib, crib_cards, temp
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

    reset()
    update()  # refreshes key for js

    point1 = PointCounter(player1Choices)
    p1_points = point1.calculation()  # Calculation of each players points
    point2 = PointCounter(player2Choices)
    p2_points = point2.calculation()

    crib = Crib(full.turn, crib_cards)  # Calculation of crib points
    crib.score()

    handScores.update(p1_points, p2_points)

    page = make_response(render_template('Main_screen.html',
                                         extra=deck.Extra[0].path,
                                         image_name=player1Choices[0].path, image_name2=player1Choices[1].path,
                                         image_name3=player1Choices[2].path, image_name4=player1Choices[3].path,
                                         image_name5=player2Choices[0].path, image_name6=player2Choices[1].path,
                                         image_name7=player2Choices[2].path, image_name8=player2Choices[3].path).format(
        full.turn.strip('player'),
        p1_points, p2_points,
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
    app.run(host='0.0.0.0', port=80, debug=False)
