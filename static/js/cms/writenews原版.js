class WriteNews {
  constructor() {

  }

  run() {
    this.upThumbnailUrl();
    this.AddNewsData();
  }

  upThumbnailUrl() {
    var self = this;
    var thumbnail = $('.up-thumbnail');
    thumbnail.change(function (e) {
      var file = thumbnail[0].files[0];
      var formdata = new FormData();
      formdata.append('file', file);  //名字与后端一至
      Ajax.post({
        url: '/cms/up_thumbnail/',
        data: formdata,
        processData: false,
        contentType: false,
        success: function (data) {
          if (data.code === 200) {
            var url = data.data.url;
            var thumbnailInput = $('#thumbnail-form[name="thumbnail"]');
            thumbnailInput.val(url);
          }
        }
      })
    })
  }

  AddNewsData() {

    let upBtn = $('#up-news');

    upBtn.click(function (e) {
      e.preventDefault();
      let title = $('#title-form').val();
      let category = $('#category-form').val();
      let desc = $('#desc-form').val();
      let thumbnail = $('#thumbnail-form').val();
      let content = $('#content-form').val();
      var news_id = $('#write-news-body').attr('data-news');
      var url = null;
      let data = {
        'title': title,
        'tag_id': category,
        'digest': desc,
        'image_url': thumbnail,
        'content': content,
      };
      let type = '';
      if (news_id) {
        url = '/cms/new/' + news_id + '/';
        data = JSON.stringify(data);
        type = 'put'
      } else {
        url = '/cms/news/';
        type = 'post'
      }
      Ajax.request_({
        'url': url,
        'data': data,
        'type': type,
        'success': function (data) {
          if (data.code === 200) {
            if (news_id) {
              window.location.href = document.referrer

            } else {
              window.location.reload()
            }
          } else {
            popBox.showError(data.message)
          }
        }
      })
    })
  }
}

var upFile = new WriteNews();
upFile.run()
