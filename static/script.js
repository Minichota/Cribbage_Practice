var count = 0
var selected = [false, false, false, false, false, false]
var counter = 0
var check = ['card1', 'card2', 'card3', 'card4', 'card5', 'card6']
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
var selection = selection
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
$(".para").append("<img src={0} width='50'/>".format('static/'+newcard.toLowerCase()+'.png'));
}
var points = $.ajax({
type: "GET",
url: "/image_movement2",
async: false
}).responseText;
var List2 = points.split('_')
if (count == 0){
$("#div5").append('<p class=one style="color:white" align="middle">The score from these cards is: {0} to {1}</p>'.format(List2[0], List2[1]));
$("#div5").append('<p class=two style="color:white" align="middle">{0}</p>'.format(List2[2]))
count++;
}else{
$(".one").replaceWith('<p class=one style="color:white" align="middle">The score from these cards is: {0} to {1}</p>'.format(List2[0], List2[1]))
$(".two").replaceWith('<p class=two style="color:white" align="middle">{0}</p>'.format(List2[2]))}
if(counter == 8){
var one = Number(List2[0]) + Number(List2[3]);
var two = Number(List2[1]) + Number(List2[4]);

$('#div3').replaceWith('<p style="color:white" align="center">The new score is {0} to {1}</p> <form method="get" action="/"><p align="center"><input type="submit" value="Next turn" name="Next turn" style="height:50px; width:200px" align="center"/></p></form>'.format(one, two))
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
selected = [false, false, false, false, false, false]
$(location).attr('href', '/{0}'.format(choices))
}else{//reset
alert('you must select 4 cards')
}}