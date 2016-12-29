$(document).ready(function() {
var KEYSTRING = "player-container";
var allAudioDivs = $("div").filter("." + KEYSTRING);
var wavesurfers = {};
var id = [];
var j=0;

"use strict";

var slider = $('#slider');
 
slider.slider({
    range: "min",
    min: 1,
    value: 36,
    step: 2
});

for (var i=0; i < 100; i++) {          //counting player objects
    if (typeof allAudioDivs[i] !== "object" ) { break; }
    j++;
    }

for (i = 0; i < j; i++) {
    id[i] = allAudioDivs[i].id;
    let pk = id[i].slice(KEYSTRING.length);
    wavesurfers[pk] = WaveSurfer.create({
        container: ("#" + id[i]),
        //backend: 'MediaElement',
        //barWidth: 3,
        progressColor: "hsla(177, 82%, 30%, 0.5)",
        hideScrollbar: true
        });

    var play = "#play" + pk;
    $(play).on("click", function (e) {
        wavesurfers[pk].playPause();
        play = "#play" + pk;
        if (wavesurfers[pk].isPlaying() == true) {
            for (p in wavesurfers) {
                if (wavesurfers[p].isPlaying() == true & p !== pk) { 
                    wavesurfers[p].pause(); 
                    otherPlay = "#play" + p;
                    $(otherPlay + " span").attr("class", "glyphicon glyphicon-play");
                }
            }
            $(play + " span").attr("class", "glyphicon glyphicon-pause");
        } else {
            $(play + " span").attr("class", "glyphicon glyphicon-play");
        }
    });
        
    wavesurfers[pk].on("finish", function (event) {
        wavesurfers[pk].stop();
        play = "#play" + pk;
        $(play + " span").attr("class", "glyphicon glyphicon-play");
        }
    );    

    wavesurfers[pk].on("loading", function (percents) {
        progress = "#progress" + pk;
        //document.getElementById(progress).value = percents;
        $(progress).css("width", percents + '%').attr('aria-valuenow', percents + '%').text(percents);
    });

    wavesurfers[pk].on("ready", function (percents) {
        progress = "#progress" + pk;
        //document.getElementById(progress).style.display = 'none';
        $(progress).css("display", "none");
        $(progress).parent().css("display", "none");
    });

    $("#slider").on("slidechange", 
        function(event, ui) {
            wavesurfers[pk].setVolume(slider.slider('value') / 100);
            //$("#debug").text(slider.slider('value'));
        }
    );

    url = $("#" + id[i]).attr("src");
    wavesurfers[pk].load(url);
    wavesurfers[pk].setVolume(slider.slider('value') / 100);
} //end of main for


});
