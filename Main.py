from Points import point
from Deckdata import handscores, hand, deck
from Gameplay import player1, player2, score, clearplayers
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
def scoreupdate():
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
    hand.build()
    return render_template('Card_selection.html',
                           image_name=hand.p1hand[0].path, image_name2=hand.p1hand[1].path,
                           image_name3=hand.p1hand[2].path, image_name4=hand.p1hand[3].path,
                           image_name5=hand.p1hand[4].path, image_name6=hand.p1hand[5].path)


class End(Resource):
    def get(self):
        winner = request.args['winner']
        score1 = handscores.get_var1()
        score2 = handscores.get_var2()
        handscores.reset()
        return make_response(render_template('End.html').format(winner, score1, score2, full.turn), 200, headers)


full = Game('player1', 'player2')


@app.route('/<selections>', methods=['GET', 'POST'])
def selections(selections):
    global realselections
    realselections = []
    reset()
    temp = selections.split(',')
    for i in range(len(temp)):
        if temp[i] == 'true':
            realselections.append(hand.p1hand[i])
    if full.turn == 'player1':
        for i in range(4):
            full.Playerturn('player1', realselections[i])
            full.Playerturn('player2', hand.p2hand[i])
    elif full.turn == 'player2':
        for i in range(4):
            full.Playerturn('player2', realselections[i])
            full.Playerturn('player1', hand.p2hand[i])
    update()  # refreshes key for js
    point.calculation(realselections, hand.Extra, 'p1')  # Calculation of each players points
    point.calculation(hand.p2hand[0:4], hand.Extra, 'p2')

    print(hand.p1hand, hand.p2hand)
    handscores.update(point.get_var1(), point.get_var2())  # adds those scores to variable of players scores
    page = make_response(render_template('Main_screen.html',
                                         extra=hand.Extra[0].path,
                                         image_name=realselections[0].path, image_name2=realselections[1].path,
                                         image_name3=realselections[2].path, image_name4=realselections[3].path,
                                         image_name5=hand.p2hand[0].path, image_name6=hand.p2hand[1].path,
                                         image_name7=hand.p2hand[2].path, image_name8=hand.p2hand[3].path,
                                         card1=score.cardsplayed[0].path, card2=score.cardsplayed[1].path,
                                         card3=score.cardsplayed[2].path, card4=score.cardsplayed[3].path,
                                         card5=score.cardsplayed[4].path, card6=score.cardsplayed[5].path,
                                         card7=score.cardsplayed[6].path, card8=score.cardsplayed[7].path).format(
        full.turn,
        point.p1points, point.p2points,
        handscores.get_var1(), handscores.get_var2(),
        player1.pointsearned, player2.pointsearned, score.pips), 200, headers)  # building main template
    deck.shuffle()
    clearplayers()
    point.__init__()
    # Checking to see if anyone won
    if full.turn == 'player1':
        if handscores.get_var1() >= 121:
            full.__init__('player2', 'player1')
            return redirect(url_for('end', winner='player 1'))
        elif handscores.get_var2() >= 121:
            full.__init__('player2', 'player1')
            return redirect(url_for('end', winner='player 2'))
        else:
            full.__init__('player2', 'player1')
            return page
    else:
        if handscores.get_var2() >= 121:
            full.__init__('player1', 'player2')
            return redirect(url_for('end', winner='player 2'))
        elif handscores.get_var1() >= 121:
            full.__init__('player1', 'player2')
            return redirect(url_for('end', winner='player 1'))
        else:
            full.__init__('player1', 'player2')
            return page


def update():
    global keys
    keys = {
        'card1': realselections[0],
        'card2': realselections[1],
        'card3': realselections[2],
        'card4': realselections[3],
        'card5': hand.p2hand[0],
        'card6': hand.p2hand[1],
        'card7': hand.p2hand[2],
        'card8': hand.p2hand[3]}


api.add_resource(End, '/end')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
