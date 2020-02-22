/**
 * Created 蓝羽教学 on 2019/12/23.
 */


$(function () {
  // let $e = window.wangEditor;
  // window.editor = new $e('#news-content');
  // window.editor.create();

  // 获取缩略图输入框元素
  let $thumbnailUrl = $("#news-thumbnail-url");

  // ================== 上传图片文件至服务器 ================
  let $upload_to_server = $("#upload-news-thumbnail");
  $upload_to_server.change(function () {
    let file = this.files[0];   // 获取文件
    let oFormData = new FormData();  // 创建一个 FormData
    oFormData.append("file", file); // 把文件添加进去
    // 发送请求
    $.ajax({
      url: "/cms/up_thumbnail/",
      method: "POST",
      data: oFormData,
      processData: false,   // 定义文件的传输
      contentType: false,
    })
    .done(function (res) {
      if (res.code === 200) {
        // 更新标签成功
        popBox.showCurrent("图片上传成功");
        let sImageUrl = res["data"]["url"];
        // console.logs(thumbnailUrl);
        $thumbnailUrl.val('');
        $thumbnailUrl.val(sImageUrl);
      } else {
        popBox.showError(res.message)
      }
    })
    .fail(function () {
      popBox.showError('服务器超时，请重试！');
    });

  });

  // ================== 发布文章 ================
  let $newsBtn = $("#btn-pub-news");
  $newsBtn.click(function () {
    // 判断文章标题是否为空
    let sTitle = $("#news-title").val();  // 获取文章标题
    if (!sTitle) {
      popBox.showError('请填写文章标题！');
      return
    }
    // 判断文章摘要是否为空
    let sDesc = $("#news-desc").val();  // 获取文章摘要
    if (!sDesc) {
      popBox.showError('请填写文章摘要！');
      return
    }

    let sTagId = $("#news-category").val();
    if (!sTagId || sTagId === '0') {
      popBox.showError('请选择文章标签')
      return
    }

    let sThumbnailUrl = $thumbnailUrl.val();
    if (!sThumbnailUrl) {
      popBox.showError('请上传文章缩略图')
      return
    }
    let sContentHtml = $(".markdown-body").html();
    console.log(sContentHtml);
    // let sContentHtml = $("#content").val();
    if (!sContentHtml || sContentHtml === '<p><br></p>') {
      popBox.showError('请填写文章内容！');
      return
    }

    // 获取news_id 存在表示更新 不存在表示发表
    let newsId = $(this).data("news-id");
    let url = newsId ? '/cms/new/' + newsId + '/' : '/cms/news/';
    let data = {
      "title": sTitle,
      "digest": sDesc,
      "tag": sTagId,
      "image_url": sThumbnailUrl,
      "content": sContentHtml,
    };

    Ajax.request_({
      // 请求地址
      url: url,
      // 请求方式
      type: newsId ? 'PUT' : 'POST',
      data: JSON.stringify(data),
      // 请求内容的数据类型（前端发给后端的格式）
      contentType: "application/json; charset=utf-8",
      // 响应数据的格式（后端返回给前端的格式）
      dataType: "json",
      'success': function (res) {
        if (res.code === 200) {
          if (newsId) {
            popBox.showCurrent("文章更新成功");
            setTimeout(function () {
              window.location.href = '/cms/news/';
            }, 1000)

          } else {
            popBox.showCurrent("文章添加成功");
            setTimeout(function () {
              window.location.reload();
            }, 1000)
          }

        } else {
          popBox.showError(res.message);
        }
      },
      'fail': function () {
        popBox.showError('服务器超时，请重试！');
      }
    });
  });

  // get cookie using jQuery
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      let cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        let cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  // Setting the token on the AJAX request
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
  });

});