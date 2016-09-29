$(document).ready(function() {
var KEYSTRING = "player-container";
var allAudioDivs = $("div").filter("." + KEYSTRING);
var wavesurfers = {};
var id = [];
var j=0;

var slider = $('#slider');
 
slider.slider({
    range: "min",
    min: 1,
    value: 36,
    step: 5 
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
        hideScrollbar: true
        });

    var play = "#play" + pk;
    $(play).on("click", 
        function (event) {
            wavesurfers[pk].playPause();
            play = "#play" + pk;
            console.log(wavesurfers[pk].isPlaying());
            if (wavesurfers[pk].isPlaying() == true) {
                $(play + " span").attr("class", "glyphicon glyphicon-pause");
            } else {
                $(play + " span").attr("class", "glyphicon glyphicon-play");
            }
        }
    );

    wavesurfers[pk].on("finish",
        function (event) {
            wavesurfers[pk].stop();
            play = "#play" + pk;
            $(play + " span").attr("class", "glyphicon glyphicon-play");
        }
    );    

    $("#slider").on("slidechange", 
        function(event, ui) {
            wavesurfers[pk].setVolume(slider.slider('value') / 100);
            //$("#debug").text(slider.slider('value'));
        }
    );

    url = $("#" + id[i]).attr("src");
    wavesurfers[pk].load(url);
    wavesurfers[pk].setVolume(slider.slider('value') / 100);
    }
    //$("#debug").text(slider.slider('value'));


});