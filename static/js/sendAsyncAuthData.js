$(document).ready(function(){
$('#id_login').click(function(){
  var input_username =document.getElementById('inputUsername')
  var username = input_username.text





$.ajax({
  url: 'login/',
  data: {
    'username': username,
  },
  dataType: 'json',
  success: function (data) {
  s = cleanJson(data)
}
});
});
})
