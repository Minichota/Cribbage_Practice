console.log('JS loaded');
var count = 0
String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a
}
function myTrim(x) {
    return x.replace('.','');
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
console.log(newcard.toLowerCase());
$(".para").append("<img src={0} width='50'/>".format('static/'+newcard.toLowerCase()+'.png'));
}
var points = $.ajax({
type: "GET",
url: "/image_movement2",
async: false
}).responseText;
var List2 = points.split('_')
console.log(List2)
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