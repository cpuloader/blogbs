$(document).ready(function() {
const KEYSTRING = "player-container";
var allAudioDivs = $("div").filter("." + KEYSTRING);
var wavesurfers = {};
var id = [];
var pks = [];
var j = 0;

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
    id[j] = allAudioDivs[j].id;
    pks[j] = id[j].slice(KEYSTRING.length);
    j++;
}

function buildPeaks(pk) {
    let peakStr = $('#peaks' + pk).text();
    let peakData = peakStr.split(',');
    return peakData;
}

for (let pk of pks) {
    wavesurfers[pk] = WaveSurfer.create({
        container: ("#" + id[pks.indexOf(pk)]),
        backend: 'MediaElement',
        //barWidth: 3,
        progressColor: "hsla(177, 82%, 30%, 0.5)",
        hideScrollbar: true,
        responsive: 100
    });

    url = $("#" + id[pks.indexOf(pk)]).attr("audiosrc");
    //let peaks = buildPeaks(pk);
    //console.log(pk, 'peaks len', peaks.length);
    wavesurfers[pk].load(url, buildPeaks(pk), 'auto');
    wavesurfers[pk].setVolume(slider.slider('value') / 100);

    $("#play" + pk).on("click", function (e) {
        wavesurfers[pk].playPause();
    });

    wavesurfers[pk].on("play", function (event) {
        if (wavesurfers[pk].isPlaying() == true) {
            for (let pk2 of pks) {                  // pause all other players
                if (wavesurfers[pk2].isPlaying() == true && pk !== pk2) { 
                    wavesurfers[pk2].pause(); 
                    $("#play" + pk2 + " span").attr("class", "glyphicon glyphicon-play");
                }
            }
            $("#play" + pk + " span").attr("class", "glyphicon glyphicon-pause");
        }
    });

    wavesurfers[pk].on("pause", function (event) {
        $("#play" + pk + " span").attr("class", "glyphicon glyphicon-play");
    });
        
    wavesurfers[pk].on("finish", function (event) {
        wavesurfers[pk].stop();
        $("#play" + pk + " span").attr("class", "glyphicon glyphicon-play");
        }
    );    

    wavesurfers[pk].on("loading", function (percents) {
        //console.log('loading', percents);
        $("#progress" + pk).css("width", percents + '%').attr('aria-valuenow', percents + '%').text(percents);
    });

    // use 'ready' event on webaudio
    wavesurfers[pk].on("ready", function (percents) {
        //document.getElementById(progress).style.display = 'none';
        $("#progress" + pk).css("display", "none");
        $("#progress" + pk).parent().css("display", "none");
        //$("#duration" + pk).text(' / ' + Math.floor(wavesurfers[pk].getDuration()) + ' sec.');
        let time = $("#real-duration" + pk).text();
        $("#real-duration" + pk).text(showTime(parseFloat(time)));
        $("#real-duration" + pk).css("display", "inline");
    });
    /*
    wavesurfers[pk].on("seek", function (pos) {
        //console.log('getDuration', wavesurfers[pk].getDuration());
        $("#seek-position" + pk).text(Math.floor(wavesurfers[pk].getDuration() * pos));
    });

    wavesurfers[pk].on("audioprocess", function (pos) {
        $("#seek-position" + pk).text(Math.floor(pos));
    });*/

    $("#slider").on("slidechange", 
        function(event, ui) {
            wavesurfers[pk].setVolume(slider.slider('value') / 100);
            //$("#debug").text(slider.slider('value'));
        }
    );

} //end of main for


});

function showTime(time) {
    let h = '00'; 
    let m = '00'; 
    let s = '00';
    if (time >= 3600) {
        h = Math.floor(time / 3600);
        time = time % 3600;
        if (h < 10) { h = '0' + h; }
    }
    if (time >= 60) {
        m = Math.floor(time / 60);
        time = time % 60;
        if (m < 10) { m = '0' + m; }
    } 
    if (time < 60) {
        s = Math.floor(time);
        if (s < 10) { s = '0' + s; }
    }
    return h + ':' + m + ':' + s;
}
