import Points
from flask import Flask, render_template, request, url_for, redirect
from Tands import Hands, Deck, Scores, update_hands
from Gameplay import player1hand, player2hand, score_points, player1, player2, game
import os
#no beyond that dude, because that's a windows path
#Only thing I can think of is other mentions to that file,
#THat line is the problem, do you see? yea the spaceno
app = Flask(__name__, template_folder= (os.getcwd() + '/templates'))
addscore = Scores(0, 0)
point = Points.Point_Counter()
deck, Hand = update_hands()
class full_game:
    def __init__(self, turn):
        self.turn = turn

    def Playerturn(self, playersturn, cardselected):
        if playersturn == 'player1':
            game.player1(cardselected)
        if playersturn == 'player2':
            game.player2(cardselected)

    def Play(self):
        # Hand.p1hand[Hand.p1hand.index(Card)] = 'Blank.png'
        print('wow')

@app.route('/end', methods=['GET', 'POST'])
def end():
    score1 = addscore.get_var1()
    score2 = addscore.get_var2()
    if request.method == 'POST':
        if request.form['submit'] == 'Restart':
            addscore.__init__(0, 0)
    elif request.method == 'GET':
        addscore.__init__(0, 0)
    return render_template('End.html').format(score1, score2, full.turn)


@app.route('/end1', methods=['GET', 'POST'])
def end1():
    score1 = addscore.get_var1()
    score2 = addscore.get_var2()
    if request.method == 'POST':
        if request.form['submit'] == 'Restart':
            addscore.__init__(0, 0)
    elif request.method == 'GET':
        addscore.__init__(0, 0)
        return render_template('End1.html').format(score1, score2, full.turn)


full = full_game('player1')

@app.route('/', methods=['GET', 'POST'])
def index():
    deck, Hand = update_hands()  # resets/shuffles deck and updates hands
    score = score_points(game.cardsplayed)
    if full.turn == 'player1':
        for i in range(4):
            full.Playerturn('player1', Hand.p1hand[i])
            full.Playerturn('player2', Hand.p2hand[i])
    elif full.turn == 'player2':
        for i in range(4):
            full.Playerturn('player2', Hand.p2hand[i])
            full.Playerturn('player1', Hand.p1hand[i])

    print(player1.pointsearned, player2.pointsearned)
    point.calculation(Hand.p1hand[0:4], Hand.Extra)  # returns player1's points
    point.calculation2(Hand.p2hand[0:4], Hand.Extra)  # returns player2's points
    addscore.update(point.get_var1(), point.get_var2())  # adds those scores to variable of players scores
    page = render_template('Main Screen.html',
            extra=Hand.Extra[0].path,
            image_name=Hand.p1hand[0].path, image_name2=Hand.p1hand[1].path,
            image_name3=Hand.p1hand[2].path, image_name4=Hand.p1hand[3].path,
            image_name5=Hand.p2hand[0].path, image_name6=Hand.p2hand[1].path,
            image_name7=Hand.p2hand[2].path, image_name8=Hand.p2hand[3].path).format(
            full.turn,
            point.get_var1(), point.get_var2(),
            addscore.get_var1(), addscore.get_var2(),
            player1.pointsearned, player2.pointsearned) #building main template
    print(addscore.get_var1(), addscore.get_var2())
    if full.turn == 'player1':
        if addscore.get_var1() >= 121:
            full.__init__('player2')
            player1.__init__()
            player2.__init__()
            return redirect(url_for('end'))
        elif addscore.get_var2() >= 121:
            full.__init__('player2')
            player1.__init__()
            player2.__init__()
            return redirect(url_for('end1'))
        else:
            full.__init__('player2')
            player1.__init__()
            player2.__init__()
            return page
    else:
        if addscore.get_var2() >= 121:
            full.__init__('player1')
            player1.__init__()
            player2.__init__()
            return redirect(url_for('end1'))
        elif addscore.get_var1() >= 121:
            full.__init__('player1')
            player1.__init__()
            player2.__init__()
            return redirect(url_for('end'))
        else:
            full.__init__('player1')
            player1.__init__()
            player2.__init__()
            return page


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
