var count = 0;
var selected = [false, false, false, false, false, false];
var counter = 0;
var check = ['card1', 'card2', 'card3', 'card4', 'card5', 'card6'];
var temp1 = 0;
var temp2 = 0;
var divClone;
var lil = ['.card1', '.card2', '.card3', '.card4'];

String.prototype.format = function () {
    a = this;
    for (k in arguments) {
        a = a.replace("{" + k + "}", arguments[k])
    }
    return a
};

function initialize() {
    var played = $.parseJSON($.ajax({
        type: "get",
        url: "/onload",
        async: false
    }).responseText);
    played = played.played;
    if (played.length > 0) {
        $('.card5').remove();
        $(".para").empty().append("<img src={0} width='50'/>".format('../static/' + played[0].path));
    }
}

function remove(selection) {
    $(".para").empty();
    counter += 1;
    $(selection).remove();
    $('.card' + String(counter + 4)).remove();
    var List = $.parseJSON($.ajax({
        type: "get",
        url: "/image_movement/{0}".format(selection),
        async: false
    }).responseText);
    List = List["played"];

    for (i = 0; i < List.length; i++) {
        $(".para").append("<img src={0} width='50'/>".format('../static/' + List[i].path));
    }


    var List2 = $.parseJSON($.ajax({
        type: "GET",
        url: "/image_movement2",
        async: false
    }).responseText);

    if (count === 0) {
        temp1 = List2[3]
        temp2 = List2[4]
        $("#div5").append('<p class=one style="color:white; position: fixed; text-align: center; width: 100%; top: 330px">The score from these cards is: {0} to {1} and the current value is: {2}</p>'.format(List2[0], List2[1], List2[5]));
        $("#div5").append('<p class=two style="color:white; position: fixed; text-align: center; width: 100%; top: 350px">{0}</p>'.format(List2[2]));
        count++;
    } else {
        if (counter != 4) {
            $(".one").replaceWith('<p class=one style="color:white; position: fixed; text-align: center; width: 100%; top: 330px">The score from these cards is: {0} to {1} and the current value is: {2}</p>'.format(List2[0], List2[1], List2[5]));
            $(".two").replaceWith('<p class=two style="color:white; position: fixed; text-align: center; width: 100%; top: 350px">{0}</p>'.format(List2[2]))
        } else {
            $(".one").replaceWith('<p class=one style="color:white; position: fixed; text-align: center; width: 100%; top: 80px">The score from these cards is: {0} to {1}</p>'.format(List2[0], List2[1]));
            $(".two").replaceWith('<p class=two style="color:white; position: fixed; text-align: center; width: 100%; top: 95px">{0}</p>'.format(List2[2]))
        }
    }

    if (counter === 4) {
        $('.para').css({'text-align': 'center', 'position': 'fixed', 'top': '0'})
        var playercards = $.parseJSON($.ajax({
            type: "get",
            url: "/bot_cards".format(lil[i]),
            async: false
        }).responseText);

        for (i = 0; i < playercards.length; i++) {
            playercards[i] = '../static/' + playercards[i].path
        }
        $('.p1').replaceWith('<p style="color:white; position: fixed; text-align: left; width: 100%; top: 200px">Your hand is:<br><img src="{0}"  width="50"/><img src="{1}" width="50"/><img src="{2}" width="50" /><img src="{3}" width="50" /><br>This is worth: {4} points</p>'.format(playercards[0], playercards[2], playercards[4], playercards[6], List2[8]));
        $(".p2").replaceWith('<p style="color:white; position: fixed; text-align: right; width: 99%; top: 200px">Your enemy\'s hand is:<br><img src="{0}"  width="50"/><img src="{1}" width="50"/><img src="{2}" width="50" /><img src="{3}" width="50" /><br>This is worth: {4} points</p>'.format(playercards[1], playercards[3], playercards[5], playercards[7], List2[9]));
        for (i = 0; i < 4; i++) {
            List[i] = '../static/' + List[i].path
        }
        $('#div3').replaceWith('<p style="color:white; position: fixed; text-align: center; width: 100%; top: 150px"><font size="6">The new score is {0} to {1}<br>Original score: {2}<br>Score from player hands: {3} points<br>Score from play: {4} points<br>Player {5}\'s crib: {6} points</font></p> <form method="get" action="/cardselect"><\'<p style="color:white; position: fixed; text-align: center; width: 100%; top: 430px"><input type="submit" value="Next turn" style="height:50px; width:200px" align="center"/></p></form>'.format(Number(List2[3]), Number(List2[4]), [temp1 + ' to ' + temp2], [List2[8] + ' and ' + List2[9]], [List2[0] + ' and ' + List2[1]], List2[7], List2[5]))
        $('.first').css({
            'color': 'white',
            'position': 'fixed',
            'text-align': 'center',
            'width': '100%',
            'top': '668px'
        })
        $('.second').replaceWith("<p style='color:white; position: fixed; text-align: center; width: 100%; top: 700px' class='second'><img src='/static/{0}' width='50'/><img src='/static/{1}' width='50'/><img src='/static/{2}' width='50'/><img src='/static/{3}' width='50'/><br>This is worth {4} points</p>".format(List[0], List[1], List[2], List[3], List2[5]))

        counter = 0;
    }
}

function select(card1) {
    updated = '.' + card1
    if (selected[check.indexOf(card1)] == false) {
        selected[check.indexOf(card1)] = true;
        $(document).ready(function () {
            $(updated).animate({
                "top": 30
            }, 100);
        })
    } else {
        selected[check.indexOf(card1)] = false;
        $(document).ready(function () {
            $(updated).animate({
                "top": 0
            }, 100);
        })
    }
}

function submit() {
    var choices = [];
    var count = 0;
    for (i = 0; i < 6; i++) {
        if (selected[i] === true) {
            count += 1;     //checks if four are selected
        }
    }
    if (count === 4) {
        choices = selected;
        for (i = 0; i < 6; i++) {        //reset
            if (selected[i] === true) {
                $('.' + check[i]).toggleClass('selectedIMG')
            }
        }
        selected = [false, false, false, false, false, false];

        $(location).attr('href', '/{0}'.format(choices))
    } else {//reset
        alert('you must select 4 cards')
    }
}
