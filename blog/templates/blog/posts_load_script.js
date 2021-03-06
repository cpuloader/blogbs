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
    if (hasNextPage == false||document.getElementById('no-posts') !== null) {
        return false
    }

    var loadSign = document.createElement("div");
    loadSign.style.position = "absolute";
    loadSign.style.backgroundColor = "#AAAAAA";
    loadSign.style.display = "block";
    loadSign.style.width = "100px"
    loadSign.style.top = window.pageYOffset - 80;
    loadSign.style.left = document.documentElement.clientWidth / 2 - 50 + "px";
    loadSign.zIndex = "11";
    var loadText = document.createElement("p");
    loadText.innerHTML = "Loading...";
    loadText.style.margin = "20px";
    loadSign.append(loadText);
    $(".bloglist").append(loadSign);
    function animateLoad() {
        loadText.innerHTML = "Loading";
        setTimeout(function() { loadText.innerHTML = "Loading."; }, 200);
        setTimeout(function() { loadText.innerHTML = "Loading.."; }, 400);
        setTimeout(function() { loadText.innerHTML = "Loading..."; }, 600);
    }
    loadingNext = setInterval(function() {animateLoad();}, 800);
    pageNum = pageNum + 1;

    var url = baseUrl + "json/" + pageNum + '/';
    $.ajax({
        url: url, 
        dataType: 'json',
        success: function(data) {
            clearInterval(loadingNext);
            loadSign.parentNode.removeChild(loadSign);
            hasNextPage = data.hasNext;
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
                $('.bloglist').append(newPost);
            });
        },
        complete: function(data, textStatus){
            $(window).bind('scroll', loadOnScroll);
        },
        error: function(xhr, errmsg, err) {
            //console.log(xhr.status + ": " + errmsg + ": "+ xhr.responseText);
        }
    });
};

$(document).ready(function(){     
   $(window).bind('scroll', loadOnScroll);
});