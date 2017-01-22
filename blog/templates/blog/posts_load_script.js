// Scroll globals
//var pageNum = {{ page.number }}; // The latest page loaded
//var hasNextPage = {{ page.has_next|lower }}; // Indicates whether to expect another page after this one
//var baseUrl = '{% url "list" %}'; // The root for the JSON calls
// loadOnScroll handler

var loadOnScroll = function() {
   // If the current scroll position is past out cutoff point...
    if ($(window).scrollTop() > $(document).height() - ($(window).height()*1.5)) {
        // temporarily unhook the scroll event watcher so we don't call a bunch of times in a row
        $(window).unbind();
        // execute the load function below that will visit the JSON feed and stuff data into the HTML
        loadItems();
    }
};

var loadItems = function() {
    // If the next page doesn't exist, just quit now 
    //console.log(document.getElementById('no-posts'));
    if (hasNextPage == false||document.getElementById('no-posts') !== null) {
        return false
    }
    // Update the page number
    pageNum = pageNum + 1;
    // Configure the url we're about to hit
    var url = baseUrl + "json/" + pageNum + '/';
    $.ajax({
        url: url, 
        dataType: 'json',
        success: function(data) {
            // Update global next page variable
            hasNextPage = data.hasNext;
            //console.log(hasNextPage);
            // Loop through all items
            var firstPost = document.querySelector(".blogpost");
            $.each(data.itemList, function(index, item) {
                var newPost = firstPost.cloneNode(true);
                newPost.querySelector(".created-date").innerHTML = item.datetime;
                newPost.querySelector(".post-title-link").innerHTML = item.title;
                newPost.querySelector(".post-title-link").href = item.postUrl;
                newPost.querySelector(".blog-content").innerHTML = item.content;
                var basePostChange = firstPost.querySelector(".post-change").href;
                var postChange = basePostChange.slice(0, basePostChange.lastIndexOf('/')) + "/" + item.postPk;
                newPost.querySelector(".post-change").href = postChange;
                var basePostDelete = firstPost.querySelector(".post-delete").action;
                var postDelete = basePostDelete.slice(0, basePostDelete.lastIndexOf('/')) + "/" + item.postPk;
                newPost.querySelector(".post-delete").action = postDelete;
                newPost.querySelector(".author-link").innerHTML = item.author;
                var baseProfileLink = firstPost.querySelector(".author-link").href;
                var authorProfile = baseProfileLink.slice(0, baseProfileLink.lastIndexOf('/')) + "/" + item.authorPk;
                newPost.querySelector(".author-link").href = authorProfile;
                newPost.querySelector(".author-extra").innerHTML = item.authorText;
                if (+item.comments > 0) {
                    newPost.querySelector(".comments-count").innerHTML = 'Комментариев: ' + item.comments;
                }
                else { 
                    newPost.querySelector(".comments-count").innerHTML = 'Комментариев нет.';
                }
                //newPost.querySelector(".author-pk").innerHTML = item.author;
                $('.bloglist').append(newPost);
            });
        },
        complete: function(data, textStatus){
            // Turn the scroll monitor back on
            $(window).bind('scroll', loadOnScroll);
        },
        error: function(xhr,errmsg,err) {
            //console.log(xhr.status + ": " + errmsg + ": "+ xhr.responseText);
        }
    });
};

$(document).ready(function(){     
   $(window).bind('scroll', loadOnScroll);
});