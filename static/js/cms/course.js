class Course {
  constructor() {
  }

  run() {
    this.submitCourse();
  }

  submitCourse() {
    var submitBtn = $('#up-course-btn')
    var titleTag = $('#title-course')
    var categoryTag = $('#category-course')
    var teacherTag = $('#teacher-form')
    var videoTag = $('#video-form')
    var thumbnailTag = $('#course-thumbnail')
    var priceTag = $('#price-form')
    var durationTag = $('#duration-form')
    var introTag = $('#intro-form')

    submitBtn.click(function () {
      var title = titleTag.val()
      var category = categoryTag.val()
      var teacher = teacherTag.val()
      var thumbnail = thumbnailTag.val()
      var video = videoTag.val()
      var price = priceTag.val()
      var duration = durationTag.val()
      var intro = introTag.val()
      Ajax.post({
        'url': '/cms/pub_course/',
        'data': {
          'title': title,
          'teacher': teacher,
          'cover_url': thumbnail,
          'category': category,
          'video_url': video,
          'price': price,
          'duration': duration,
          'profile': intro
        },
        'success': function (data) {
          if (data.code === 200) {
            popBox.showCurrent('上传成功')
          } else {
            popBox.showError(data.message)

          }
        }
      })

    })
  }

}
$(function () {
  var course = new Course();
  course.run()
});