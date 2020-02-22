class Comment {
  constructor() {
    template.defaults.imports.timesince = function (datatime) {
      var data = new Date(datatime)
      var datats = data.getTime()
      var now = (new Date()).getTime()
      var timestamp = (now - datats) / 1000
      if (timestamp < 60) {
        return '刚刚'
      } else if (timestamp > 60 && timestamp < 60 * 60
      ) {
        var minutes = parseInt(timestamp / 60)
        return minutes + '分钟前'
      } else if (timestamp > 60 * 60 && timestamp < 60 * 60 * 24
      ) {
        var hours = parseInt(timestamp / 60 / 60)
        return hours + '小时前'
      } else if (timestamp > 60 * 60 * 24 && timestamp < 60 * 60 * 20 * 30) {
        var days = parseInt(timestamp / 60 / 60 / 24)
        return days + '天前'
      } else {
        var year = data.getFullYear()
        var month = data.getMonth() + 1
        var day = data.getDay()
        var hour = data.getHours()
        var minute = data.getMinutes()
        var second = data.getSeconds()
        return year + '年' + month + '月' + day + '日' + hour + '时' + minute + '分' + second + '秒'
      }
    }
    this.replyBtn = $('.reply');
  }

  addComment() {
    var commentBtn = $('.comment-btn')
    commentBtn.click(function (e) {
      e.preventDefault();
      var commentContent = $('.comment-input').val()
      var commentGroup = $('.comment-group')
      var authorId = commentGroup.attr('data-author-name')
      var newsId = commentGroup.attr('data-news-id')
      Ajax.post({
        'url': '/news/comment/',
        'data': {
          'content': commentContent,
          'newsId': newsId
        },
        'success': function (result) {
          if (result.code === 200) {
            console.log(result.message);
            var comment = result.data;
            console.log(comment);
            var tep = template('comment-item', {'comment': comment});
            var ul = $('.comment-list');
            ul.prepend(tep);
          } else {
            popBox.showError(result.message)
          }
        }
      })

    })
  }

  noLoginBtn() {
    $('.nologin-comment-btn').click(function (e) {
      e.preventDefault()

      window.location = '/user/login/'
    })
  }

  reply() {
    var self = this;
    var target = null;
    self.replyBtn.click(function () {
      let input = $(this).prev('input[name="parent-comment"]')
      let comment_id = input.attr('data-comment-id');

      let replyContent = input.val();
      target = input;

      Ajax.post({
        'url': '/news/parent_comment/',
        'data': {
          'comment_id': comment_id,
          'content': replyContent
        },
        'success': function (result) {
          if(result.code ===200) {
            var comment = result.data;
          var tep = template('parent-comment-item', {'comment': comment});
          var ul = target.prev('ul');
          ul.append(tep);
          target.val('')
          }else {
            window.location = '/user/login/'
          }
        }
      })
    })
  }

  run() {
    this.addComment();
    this.noLoginBtn();
    this.reply();
  }
}

$(function () {
  var comment = new Comment()
  comment.run()
})



