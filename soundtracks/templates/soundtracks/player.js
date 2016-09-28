$(document).ready(function() {
var ctx = document.createElement('canvas').getContext('2d');
    var linGrad = ctx.createLinearGradient(0, 64, 0, 200);
    linGrad.addColorStop(0.5, 'rgba(255, 255, 255, 1.000)');
    linGrad.addColorStop(0.5, 'rgba(183, 183, 183, 1.000)');
var KEYSTRING = "player-container";
var allAudioDivs = $("div").filter("." + KEYSTRING);
var wavesurfers = {};
var id = [];
    console.log(typeof KEYSTRING.length);
var j=0;

for (var i=0; i < 100; i++) {
    if (typeof allAudioDivs[i] !== "object" ) { break; }
    j++;
    }

for (i = 0; i < j; i++) {
    id[i] = allAudioDivs[i].id;
    var pk = id[i].slice(KEYSTRING.length);
    wavesurfers[pk] = WaveSurfer.create({
    container: ("#" + id[i])
    });

    var play = "#play" + pk;
    $(play).bind("click", {currentIndex: pk}, 
        function (event) {
            wavesurfers[event.data.currentIndex].playPause();
        }
    );

    url = $("#" + id[i]).attr("src");
    wavesurfers[pk].load(url);
    }
});
