from Points import PointCounter, point
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

    def Playerturn(self, playersturn, cardselected):
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
    score.reset()
    clearplayers()
    for i in range(len(Played)):
        if i % 2 == 0:
            turn = 'player1'
        else:
            turn = 'player2'
        full.Playerturn(turn, Played[i])
    if len(score.cardsplayed) == 8:
        handScores.update(player1.pointsearned, player2.pointsearned)
    return str(player1.pointsearned) + '_' + str(player2.pointsearned) + '_' + str(score.pips) + '_' + \
           str(temp1) + '_' + str(temp2)


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
        score1 = handScores.get_var1()
        score2 = handScores.get_var2()
        handScores.reset()
        return make_response(render_template('End.html').format(winner, score1, score2, full.turn), 200, headers)


@app.route('/<selections>', methods=['GET', 'POST'])
def selection(selections):
    global player1Choices, player2Choices, temp1, temp2, point, full, page
    player1Choices = []
    player2Choices = []
    cribcards = []
    selections = selections.split(',')
    for i in range(len(selections)):
        if selections[i] == 'true':
            player1Choices.append(player1.hand[i])
            player2Choices.append(player2.hand[i])
        else:
            cribcards.append(player1.hand[i])
            cribcards.append(player2.hand[i])
    reset()
    update()  # refreshes key for js
    point.calculation(player1Choices, deck.Extra, 'p1')  # Calculation of each players points
    point.calculation(player2Choices, deck.Extra, 'p2')

    crib = Crib(full.turn, cribcards)
    crib.score()

    print(player1.hand, player2.hand)
    print(cribcards, deck.Extra)
    handScores.update(point.get_var1(), point.get_var2(), crib.points,
                      full.turn)  # Adds those scores to variable of players scores
    print(crib.points)
    temp1, temp2 = handScores.get_var1(), handScores.get_var2()
    print('wow')
    page = make_response(render_template('Main_screen.html',
                                         extra=deck.Extra[0].path,
                                         image_name=player1Choices[0].path, image_name2=player1Choices[1].path,
                                         image_name3=player1Choices[2].path, image_name4=player1Choices[3].path,
                                         image_name5=player2Choices[0].path, image_name6=player2Choices[1].path,
                                         image_name7=player2Choices[2].path, image_name8=player2Choices[3].path,
                                         crib1=cribcards[0].path, crib2=cribcards[1].path,
                                         crib3=cribcards[2].path, crib4=cribcards[3].path).format(
        full.turn.strip('player'),
        point.p1points, point.p2points,
        handScores.get_var1(), handScores.get_var2(),
        full.turn.strip('player'), crib.points), 200, headers)  # building main template
    deck.shuffle()
    clearplayers()
    point = PointCounter()
    # Checking to see if anyone won
    return check()


def check():
    if full.turn == 'player1':
        full.switch()
        if handScores.get_var1() >= 121:
            return redirect(url_for('end', winner='player 1'))
        elif handScores.get_var2() >= 121:
            return redirect(url_for('end', winner='player 2'))
        else:
            return page
    else:
        full.switch()
        if handScores.get_var2() >= 121:
            return redirect(url_for('end', winner='player 2'))
        elif handScores.get_var1() >= 121:
            return redirect(url_for('end', winner='player 1'))
        else:
            return page


api.add_resource(End, '/end')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
