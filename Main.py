import Points
from flask import Flask, render_template, request, url_for, redirect, make_response
from flask_restful import Api, Resource
from Tands import Hands, Deck, Scores, update_hands
from Gameplay import player1, player2, score
import os
app = Flask(__name__, template_folder=os.getcwd() + '/templates')
api = Api(app)
headers = {'Content-Type': 'text/html'}
addscore = Scores(0, 0)
point = Points.Point_Counter()
deck, Hand = update_hands()
class full_game:
    def __init__(self, turn):
        self.turn = turn

    def Playerturn(self, playersturn, cardselected):
        if playersturn == 'player1':
            player1.playcard1(cardselected)
        if playersturn == 'player2':
            player2.playcard2(cardselected)


class end(Resource):
    def post(self):
        if request.form['submit'] == 'Restart':
            addscore.__init__(0, 0)
    def get(self):
        score1 = addscore.get_var1()
        score2 = addscore.get_var2()
        addscore.__init__(0, 0)
        return make_response(render_template('End.html').format(score1, score2, full.turn), 200, headers)


class end1(Resource):
    def post(self):
        if request.form['submit'] == 'Restart':
            addscore.__init__(0, 0)
    def get(self):
        score1 = addscore.get_var1()
        score2 = addscore.get_var2()
        addscore.__init__(0, 0)
        return make_response(render_template('End1.html').format(score1, score2, full.turn), 200, headers)


full = full_game('player1')


class brain(Resource):
    def get(self):
        score.pips = []
        score.cardsplayed = []
        deck, Hand = update_hands()  # resets/shuffles deck and updates hands
        if full.turn == 'player1':
            for i in range(4):
                full.Playerturn('player1', Hand.p1hand[i])
                full.Playerturn('player2', Hand.p2hand[i])
        elif full.turn == 'player2':
            for i in range(4):
                full.Playerturn('player2', Hand.p2hand[i])
                full.Playerturn('player1', Hand.p1hand[i])

        print(player1.pointsearned, player2.pointsearned)
        point.calculation(Hand.p1hand[0:4], Hand.Extra, 'p1')  # returns player1's points
        point.calculation(Hand.p2hand[0:4], Hand.Extra, 'p2')
        addscore.update(point.get_var1(), point.get_var2())  # adds those scores to variable of players scores
        page = make_response(render_template('Main_screen.html',
                extra=Hand.Extra[0].path,
                image_name=Hand.p1hand[0].path, image_name2=Hand.p1hand[1].path,
                image_name3=Hand.p1hand[2].path, image_name4=Hand.p1hand[3].path,
                image_name5=Hand.p2hand[0].path, image_name6=Hand.p2hand[1].path,
                image_name7=Hand.p2hand[2].path, image_name8=Hand.p2hand[3].path,
                card1=score.cardsplayed[0].path, card2=score.cardsplayed[1].path,
                card3 = score.cardsplayed[2].path, card4=score.cardsplayed[3].path,
                card5=score.cardsplayed[4].path, card6=score.cardsplayed[5].path,
                card7=score.cardsplayed[6].path, card8=score.cardsplayed[7].path).format(
                full.turn,
                point.p1points, point.p2points,
                addscore.get_var1(), addscore.get_var2(),
                player1.pointsearned, player2.pointsearned, score.pips),200,headers)  # building main template
        player1.__init__()
        player2.__init__()
        point.__init__()
        if full.turn == 'player1':
            if addscore.get_var1() >= 121:
                full.__init__('player2')
                return redirect(url_for('end'))
            elif addscore.get_var2() >= 121:
                full.__init__('player2')
                return redirect(url_for('end1'))
            else:
                full.__init__('player2')
                return page
        else:
            if addscore.get_var2() >= 121:
                full.__init__('player1')
                return redirect(url_for('end1'))
            elif addscore.get_var1() >= 121:
                full.__init__('player1')
                return redirect(url_for('end'))
            else:
                full.__init__('player1')
                return page
    def post(self):
        headers = {'Content-Type': 'text/html'}
        score.pips = []
        score.cardsplayed = []
        deck, Hand = update_hands()  # resets/shuffles deck and updates hands
        if full.turn == 'player1':
            for i in range(4):
                full.Playerturn('player1', Hand.p1hand[i])
                full.Playerturn('player2', Hand.p2hand[i])
        elif full.turn == 'player2':
            for i in range(4):
                full.Playerturn('player2', Hand.p2hand[i])
                full.Playerturn('player1', Hand.p1hand[i])

        print(player1.pointsearned, player2.pointsearned)
        point.calculation(Hand.p1hand[0:4], Hand.Extra, 'p1')  # returns player1's points
        point.calculation(Hand.p2hand[0:4], Hand.Extra, 'p2')
        addscore.update(point.get_var1(), point.get_var2())  # adds those scores to variable of players scores
        page = make_response(render_template('Main_screen.html',
                extra=Hand.Extra[0].path,
                image_name=Hand.p1hand[0].path, image_name2=Hand.p1hand[1].path,
                image_name3=Hand.p1hand[2].path, image_name4=Hand.p1hand[3].path,
                image_name5=Hand.p2hand[0].path, image_name6=Hand.p2hand[1].path,
                image_name7=Hand.p2hand[2].path, image_name8=Hand.p2hand[3].path,
                card1=score.cardsplayed[0].path, card2=score.cardsplayed[1].path,
                card3 = score.cardsplayed[2].path, card4=score.cardsplayed[3].path,
                card5=score.cardsplayed[4].path, card6=score.cardsplayed[5].path,
                card7=score.cardsplayed[6].path, card8=score.cardsplayed[7].path).format(
                full.turn,
                point.p1points, point.p2points,
                addscore.get_var1(), addscore.get_var2(),
                player1.pointsearned, player2.pointsearned, score.pips),200,headers)  # building main template
        player1.__init__()
        player2.__init__()
        point.__init__()
        if full.turn == 'player1':
            if addscore.get_var1() >= 121:
                full.__init__('player2')
                return redirect(url_for('end'))
            elif addscore.get_var2() >= 121:
                full.__init__('player2')
                return redirect(url_for('end1'))
            else:
                full.__init__('player2')
                return page
        else:
            if addscore.get_var2() >= 121:
                full.__init__('player1')
                return redirect(url_for('end1'))
            elif addscore.get_var1() >= 121:
                full.__init__('player1')
                return redirect(url_for('end'))
            else:
                full.__init__('player1')
                return page
api.add_resource(brain, '/')
api.add_resource(end, '/end')
api.add_resource(end1, '/end1')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
