$(document).ready(function() {

  function playNext(domObj) {
      var autoNext = document.getElementById('auto-next').innerHTML;
      if (autoNext == 'True') {
          document.getElementById('submit-btn').click();
      } else {
          return;
      }
  }

  function setPlayingTitle(domObj) {
    var title = $(domObj).parents('.audiotracks-list-entry')
                         .find('.track-title').text();
    $('title').html('&#9654; ' + title);
  }

  var oldTitle = $('title').html();

  function revertTitle() {
    $('title').html(oldTitle);
  }

  $('audio').mediaelementplayer({
    audioWidth: '90%', 
    pluginPath: '{{ STATIC_URL }}mediaelement-2.8.2/',
    error: function(domObj) {
        $(domObj).bind('play', function() { playNext(domObj); });
    },
    success: function(me, domObj) {
      var container = $(domObj).parents('.player-container');
      container.next().find('.audio-type').html( me.pluginType );

      $(me).bind('play', function() { setPlayingTitle(domObj); });
      $(me).bind('pause', revertTitle);
      $(me).bind('ended', function() { playNext(domObj); });

      var firstPlayer = mejs.players[0];
      if (me === firstPlayer.media) {
        firstPlayer.play();
      }
    }
  });


});
