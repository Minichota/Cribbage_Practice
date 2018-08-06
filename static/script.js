var count = 0
var selected = [false, false, false, false, false, false]
var counter = 0
var check = ['card1', 'card2', 'card3', 'card4', 'card5', 'card6']
var temp1 = 0
var temp2 = 0
String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a
}

function myTrim(x) {
    x.replace(',', '');
    return x;
}
function remove(selection){
counter += 1;
if(counter == 8){
$("#div1").remove()
}
$(selection).remove();
var List = [];
List.push($.ajax({
  type: "get",
  url: "/image_movement/{0}".format(selection),
  async: false
}).responseText);
for (i = 0; i < List.length; i++){
var card = List[i].replace(' ', '_');
var newcard = card.replace(' ', '_');
$(".para").append("<img src={0} width='50'/>".format('../static/'+newcard.toLowerCase()+'.png'));
}
var points = $.ajax({
type: "GET",
url: "/image_movement2",
async: false
}).responseText;
var List2 = points.split('_')
if (count == 0){
temp1 = List2[3]
temp2 = List2[4]
$("#div5").append('<p class=one style="color:white" align="middle">The score from these cards is: {0} to {1}</p>'.format(List2[0], List2[1]));
$("#div5").append('<p class=two style="color:white" align="middle">{0}</p>'.format(List2[2]))
count++;
}else{
console.log(temp1, temp2)
$(".one").replaceWith('<p class=one style="color:white" align="middle">The score from these cards is: {0} to {1}</p>'.format(List2[0], List2[1]))
$(".two").replaceWith('<p class=two style="color:white" align="middle">{0}</p>'.format(List2[2]))}
if(counter == 8){
console.log(List2)
var one = Number(List2[3]);
var two = Number(List2[4]);
var three = List2[6].replace('[', '').replace(']', '').split(', ')
for(i=0;i<4;i++){
three[i] = '../static/'+three[i].replace(' ', '_').replace(' ', '_').toLowerCase() + '.png'
console.log(three[i])
}
    $('#div3').replaceWith('<p style="color:white" align="center">The new score is {0} to {1}</p><p style="color:white" align="center">Player {2}\'s crib: {3} points<br>Score from play: {4} points<br>Original score: {5}</p> <form method="get" action="/cardselect"><p align="center"><input type="submit" value="Next turn" name="Next turn" style="height:50px; width:200px" align="center"/></p></form>'.format(one, two, List2[7], List2[5], [List2[0] + ' and ' + List2[1]], [temp1 + ' to ' + temp2]))
$('.second').replaceWith("<p align='center' style='color:white' class='second'><img src='/static/{0}' width='50'/><img src='/static/{1}' width='50'/><img src='/static/{2}' width='50'/><img src='/static/{3}' width='50'/><br>This is worth {4} points</p>".format(three[0], three[1], three[2], three[3], List2[5]))
counter = 0;
}}

function select(card1){
if (selected[check.indexOf(card1)] == false){
selected[check.indexOf(card1)] = true;
}else{
selected[check.indexOf(card1)] = false;
}
var updated = '.'+card1
$(updated).toggleClass('selectedIMG');
}

function submit(){
var choices = [];
var count = 0;
for(i = 0; i <6; i++){
if (selected[i] == true){
count += 1;//checks if four are selected
}}
if (count == 4){
choices = selected;

for(i=0;i<6;i++){        //reset
if(selected[i] == true){
$('.'+check[i]).toggleClass('selectedIMG')
}}
var sessionID = $.ajax({
type: "GET",
url: "/sessionID",
async: false
}).responseText;
console.log('success')
selected = [false, false, false, false, false, false]
$(location).attr('href', '/{0}/{1}'.format(choices, sessionID))
}else{//reset
alert('you must select 4 cards')
}}
