var count = 1;
function bgVideo(){
    var video = document.getElementById('video-background');
    var videoSrc = document.getElementById('videoSrc');
    if(count<6){
        count = count + 1;
    }else{
        count = 1;
    }

    videoSrc.src = 'static/videos/' + count + '.mp4';
    video.load();
}
setInterval(bgVideo, 8000);