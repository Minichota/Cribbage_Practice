import Points
from flask import Flask, render_template, request, url_for, redirect, make_response
from flask_restful import Api, Resource
from Tands import Handscore, Deck, Hands
from Gameplay import player1, player2, score, clearplayers
import os
app = Flask(__name__, template_folder=os.getcwd() + '/templates')
api = Api(app)
headers = {'Content-Type': 'text/html'}
handscores = Handscore()
point = Points.Point_Counter()
deck = Deck()
Hand = Hands()
Played = []

def reset():
    global Played
    Played = []
    score.reset()
class full_game:
    def __init__(self, turn, otherturn):
        self.turn = turn
        self.otherturn = otherturn

    def Playerturn(self, playersturn, cardselected):
        if playersturn == 'player1':
            player1.playcard(cardselected, playersturn)
        if playersturn == 'player2':
            player2.playcard(cardselected, playersturn)


@app.route('/image_movement/<card>')
def minimalplay(card):
    card = card.strip('.')
    Played.append(keys[card])
    return str(keys[card])


@app.route('/image_movement2')
def minimalplaychecker():
    score.reset()
    clearplayers()
    for i in range(len(Played)):
        if i % 2 == 0:
            turn = full.turn
        else:
            turn = full.otherturn
        full.Playerturn(turn, Played[i])
    return str(player1.pointsearned)+'_'+str(player2.pointsearned)+'_'+str(score.pips)


class end(Resource):
    def post(self):
        if request.form['submit'] == 'Restart':
            handscores.reset()
    def get(self):
        winner = request.args['winner']
        score1 = handscores.get_var1()
        score2 = handscores.get_var2()
        handscores.reset()
        return make_response(render_template('End.html').format(winner, score1, score2, full.turn), 200, headers)

full = full_game('player1', 'player2')

@app.route('/', methods=['GET', 'POST'])
def index():
    reset()
    Hand.build()
    if full.turn == 'player1':
        for i in range(4):
            full.Playerturn('player1', Hand.p1hand[i])
            full.Playerturn('player2', Hand.p2hand[i])
    elif full.turn == 'player2':
        for i in range(4):
            full.Playerturn('player2', Hand.p2hand[i])
            full.Playerturn('player1', Hand.p1hand[i])

    point.calculation(Hand.p1hand[0:4], Hand.Extra, 'p1')  # Calculation of each players points
    point.calculation(Hand.p2hand[0:4], Hand.Extra, 'p2')
    print(score.cardsplayed)
    handscores.update(point.get_var1(), point.get_var2())  # adds those scores to variable of players scores
    keyupdate()
    page = make_response(render_template('Main_screen.html',
            extra=Hand.Extra[0].path,
            image_name=Hand.p1hand[0].path, image_name2=Hand.p1hand[1].path,
            image_name3=Hand.p1hand[2].path, image_name4=Hand.p1hand[3].path,
            image_name5=Hand.p2hand[0].path, image_name6=Hand.p2hand[1].path,
            image_name7=Hand.p2hand[2].path, image_name8=Hand.p2hand[3].path,
            card1=score.cardsplayed[0].path, card2=score.cardsplayed[1].path,
            card3=score.cardsplayed[2].path, card4=score.cardsplayed[3].path,
            card5=score.cardsplayed[4].path, card6=score.cardsplayed[5].path,
            card7=score.cardsplayed[6].path, card8=score.cardsplayed[7].path).format(
            full.turn,
            point.p1points, point.p2points,
            handscores.get_var1(), handscores.get_var2(),
            player1.pointsearned, player2.pointsearned, score.pips), 200, headers)  # building main template

    clearplayers()
    point.__init__()
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
def keyupdate():
    global keys
    keys = {
    'card1': Hand.p1hand[0],
    'card2': Hand.p1hand[1],
    'card3': Hand.p1hand[2],
    'card4': Hand.p1hand[3],
    'card5': Hand.p2hand[0],
    'card6': Hand.p2hand[1],
    'card7': Hand.p2hand[2],
    'card8': Hand.p2hand[3]
    }


api.add_resource(end, '/end')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)