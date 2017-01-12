$(document).ready(function() {

"use strict";

//var pk = $(".player-container").attr("id").slice(-1);
//console.log(pk);

$('#comment-form').on('submit', function(event){
    event.preventDefault();
    //console.log("form submitted!")  // sanity check
    create_comment();
});

function create_comment() {
    if ($('#id_content').val() == '') return;
    //console.log("create post is working!") // sanity check
    $.ajax({
        url : "comment/add/", // the endpoint
        type : "POST", // http method
        data : { 
               comment : $('#id_content').val(),
               'csrfmiddlewaretoken': '{{csrf_token}}'
               }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#id_content').val(''); // remove the value from the input
            if (json['content'] == undefined) return;
            $(function() {
            var newComment = $('#comment-template').html();
            $('#comments-list').append(newComment);
            $('#comments-list .comment-content').last().text(json['content']);
            $('#comments-list .comment-author').last().text(json['author']);
            var commentDate = new Date();
            commentDate.setTime(Date.parse(json['datetime']))
            var options = {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
              timezone: 'UTC',
              hour: 'numeric',
              minute: 'numeric'
            };
            var lang = $('#current-language').text();
            $('#comments-list .comment-created-date').last().text(commentDate.toLocaleString(lang, options));

            });
            //console.log(json); // log the returned json to the console
            //console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Error happened: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};


});
