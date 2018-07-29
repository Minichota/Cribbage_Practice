from Points import point
from Deckdata import handScores, deck
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
        'card5': player2.hand[0],
        'card6': player2.hand[1],
        'card7': player2.hand[2],
        'card8': player2.hand[3]}


class Game:
    def __init__(self, turn, otherturn):
        self.turn = turn
        self.otherturn = otherturn

    def Playerturn(self, playersturn, cardselected):
        if playersturn == 'player1':
            player1.play_card(cardselected, playersturn)
        if playersturn == 'player2':
            player2.play_card(cardselected, playersturn)


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
            turn = full.turn
        else:
            turn = full.otherturn
        full.Playerturn(turn, Played[i])
    return str(player1.pointsearned) + '_' + str(player2.pointsearned) + '_' + str(score.pips)


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


full = Game('player1', 'player2')


@app.route('/<selections>', methods=['GET', 'POST'])
def selection(selections):
    global player1Choices
    player1Choices = []
    crib = []
    temp = selections.split(',')
    for i in range(len(temp)):
        if temp[i] == 'true':
            player1Choices.append(player1.hand[i])
        else:
            crib.append(player1.hand[i])
    reset()
    # if full.turn == 'player1':
    #     for i in range(4):
    #         full.Playerturn('player1', player1Choices[i])
    #         full.Playerturn('player2', player2.hand[i])
    # elif full.turn == 'player2':
    #     for i in range(4):
    #         full.Playerturn('player2', player2.hand[i])
    #         full.Playerturn('player1', player1Choices[i])

    update()  # refreshes key for js
    point.calculation(player1Choices, deck.Extra, 'p1')  # Calculation of each players points
    point.calculation(player2.hand[0:4], deck.Extra, 'p2')

    print(player1.hand, player2.hand)
    handScores.update(point.get_var1(), point.get_var2())  # Adds those scores to variable of players scores

    page = make_response(render_template('Main_screen.html',
                                         extra=deck.Extra[0].path,
                                         image_name=player1Choices[0].path, image_name2=player1Choices[1].path,
                                         image_name3=player1Choices[2].path, image_name4=player1Choices[3].path,
                                         image_name5=player2.hand[0].path, image_name6=player2.hand[1].path,
                                         image_name7=player2.hand[2].path, image_name8=player2.hand[3].path).format(
        full.turn,
        point.p1points, point.p2points,
        handScores.get_var1(), handScores.get_var2(),
        player1.pointsearned, player2.pointsearned, score.pips), 200, headers)  # building main template
    deck.shuffle()
    clearplayers()
    point.__init__()
    # Checking to see if anyone won
    if full.turn == 'player1':
        if handScores.get_var1() >= 121:
            full.__init__('player2', 'player1')
            return redirect(url_for('end', winner='player 1'))
        elif handScores.get_var2() >= 121:
            full.__init__('player2', 'player1')
            return redirect(url_for('end', winner='player 2'))
        else:
            full.__init__('player2', 'player1')
            return page
    else:
        if handScores.get_var2() >= 121:
            full.__init__('player1', 'player2')
            return redirect(url_for('end', winner='player 2'))
        elif handScores.get_var1() >= 121:
            full.__init__('player1', 'player2')
            return redirect(url_for('end', winner='player 1'))
        else:
            full.__init__('player1', 'player2')
            return page


api.add_resource(End, '/end')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
