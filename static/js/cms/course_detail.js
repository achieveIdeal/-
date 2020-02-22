function CourseDetail() {

}

CourseDetail.prototype.run = function () {
  this.init()
}

CourseDetail.prototype.init = function () {
  var videoInfo = $('#video-info');
  var video_url = videoInfo.attr('data-video_url')
  var cover_url = videoInfo.attr('data-cover_url')
  var player = cyberplayer("playercontainer").setup({

    file: video_url,
    ak: "112fec2c658d480dbd35954afa01cea6",
    width: '100%',
    height: '100%',
    image: "http://jmdsaknupx9e3a9v26c.exp.bcevod.com/mda-jmdsg1r3wtdyjxha/mda-jmdsg1r3wtdyjxha.jpg",
    autostart: false,
    stretching: "uniform",
    repeat: false,
    volume: 100,
    controls: true,
    tokenEncrypt: true,

  });
  player.on('beforePlay', function (e) {
    if (!/m3u8/.test(e.file)) {
      return null
    }
    Ajax.get({
      'url': '/course/course_video/',
      'data': {
        'video': video_url
      },
      'success': function (data) {
        if(data.code === 200) {
          var token = data.data.token;
          player.setToken(e.file,token)
        }else {
          alert('错误')
        }
      },
      'fail': function (error) {
        console.log(error);
      }

    })

  })
}
$(function () {
  var video = new CourseDetail()
  video.run()
})