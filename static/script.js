var count = 0
var selected = [false, false, false, false, false, false]
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
$("#div5").append('<p class=one style="color:white">The score from these cards is: {0} to {1}</p>'.format(List2[0], List2[1]));
$("#div5").append('<p class=two style="color:white">They were scored as follows: {0}</p>'.format(List2[2]))
count += 1
}
else{
$(".one").replaceWith('<p class=one style="color:white">The score from these cards is: {0} to {1}</p>'.format(List2[0], List2[1]))
$(".two").replaceWith('<p class=two style="color:white">They were scored as follows: {0}</p>'.format(List2[2]))
}
}

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

for(i=0;i<6;i++){//reset
if(selected[i] == true){
$('.'+check[i]).toggleClass('selectedIMG')
}}

selected = [false, false, false, false, false, false]
$(location).attr('href', '/{0}'.format(choices))
}else{
alert('you must select 4 cards')
}}