$(document).ready(function(){
  var typingTimer;                //timer identifier
  var doneTypingInterval = 1000;  //time in ms, 5 second for example
  var $input = $('#search-info');

  //on keyup, start the countdown
  $input.on('keyup', function () {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
  });
  //on keydown, clear the countdown
  $input.on('keydown', function () {
    clearTimeout(typingTimer);
    $('#close-search-button').fadeIn("slow", function() {
    });
  });
  //user is "finished typing," do something
  function doneTyping() {
    console.log("send");
    $.ajax({
      url: "/search",
      method: "get",
      data: $('#search-info').serialize(),
      success: function(serverResponse) {
        jsonTaken(serverResponse);
      }
   })
  }

  $('.search-form').submit(function(e){
       e.preventDefault();
  })

   $('#search-button').click(function(){
     menuStatus = "search"
     openSearch();
     closeStackMenu();
  });

  // $(".menu-button-main").click(function(){
  //   menuController();
  //
  // })
  var isDragging = false;
  $(".menu-button-main")
  .mousedown(function() {
    isDragging = false;
  })
  .mousemove(function() {
    isDragging = true;
  })
  .mouseup(function() {
    var wasDragging = isDragging;
    isDragging = false;
    if (!wasDragging) {
      menuController();
    }
  });
});//end of document listen


// functions for top nav open/close =============
function openSearch() {
  $('.search-div').css({display: 'inline-block'})
  document.forms['search-form'].elements['search-info'].focus();

};

function closeSearch(){
  $('.search-div').css({display: 'none'})
  $('.hamburger').animate({opacity: '1'});
  $('.icon-cancel').css({'fill': '#222222'});
  $('.icon-cancel').css({display: 'none'});
  $('.menu-button-main').animate({"background-color": "white"});
};


function jsonTaken(json){
  $('#search-results').html('')
  console.log(json);
  if (json.length == 0) {
    $("#search-results").append('<div class="no-results"><h2 class = "no-results-found" >No Results Found</h2></div>');
  }
  else {
  for (var i = 0; i < json.length; i++){
    var img_url = json[i].picture
    var id = json[i].id
    var name = json[i].name
    // var type = json[i].type
    console.log(id);
    console.log(img_url);
    $("#search-results").append('<a class="search-tag" href="/game/' + id + '"><div class="result-search center"><img class ="search-result-icon" src="'+ img_url +'""> <div class="title-holder"><h3 class="search-result-title">' + name + '</h3> </div> <a href="/addGame/' + id +'/'+ name + '" class="movie-type type">Add to GameList</a> </div> </a>');
    // if (type == 'movie'){
    // }
    // else if (type == 'tv') {
    //   $("#search-results").append('<a class="search-tag" href="/show/' + id + '"><div class="result-search center"><img class ="search-result-icon" src="'+ img_url +'""> <div class="title-holder"><h3 class="search-result-title">' + json[i].name + '</h3> </div> <h3 class="tv-type type">Television</h3> </div> </a>');
    //
    // }
    // else if (type =='person') {
    //   $("#search-results").append('<a class="search-tag" href="/people/' + id + '"><div class="result-search center"><img class ="search-result-icon" src="'+ img_url +'""> <div class="title-holder"><h3 class="search-result-title">' + json[i].name + '</h3> </div> <h3 class="person-type type">Person</h3> </div> </a>');
    // }

  }
}
}
