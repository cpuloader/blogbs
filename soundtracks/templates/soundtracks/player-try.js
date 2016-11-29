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
        //backend: 'MediaElement',
        //barWidth: 3,
        progressColor: "hsla(177, 82%, 30%, 0.5)",
        hideScrollbar: true
        });

    var play = "#play" + pk;
    $(play).on("click", onClick);
        
    wavesurfers[pk].on("finish", onFinish);    

    wavesurfers[pk].on("loading", onLoading);

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

function onLoading(e, percents) {
    console.log(e, percents);
    progress = "#progress" + pk;
    //document.getElementById(progress).value = percents;
    $(progress).css("width", percents + '%').attr('aria-valuenow', percents + '%').text(percents);
}

function onClick(e) {
    var pkx = e.target.id.slice(4);
    wavesurfers[pkx].playPause();
    play = "#play" + pkx;
    console.log(wavesurfers[pkx].isPlaying());
    if (wavesurfers[pkx].isPlaying() == true) {
        $(play + " span").attr("class", "glyphicon glyphicon-pause");
    } else {
        $(play + " span").attr("class", "glyphicon glyphicon-play");
    }
}

function onFinish(e) {
    console.log(e.target.id);
    var pkx = e.target.id.slice(4);
    wavesurfers[pkx].stop();
    play = "#play" + pkx;
    $(play + " span").attr("class", "glyphicon glyphicon-play");
}


});
