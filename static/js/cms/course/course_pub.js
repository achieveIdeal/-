/**
 * Created 蓝羽教学 on 2019/12/29.
 */
$(function () {
  let $thumbnailUrl = $("#news-thumbnail-url");   // 获取缩略图输入框元素
  let $courseFileUrl = $("#docs-file-url");    // 获取课程地址输入框元素

  // ================== 上传图片文件至服务器 ================
  let $upload_image_server = $("#upload-image-server");
  $upload_image_server.change(function () {
    // let _this = this;
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
          popBox.showCurrent("图片上传成功");
          let sImageUrl = res.data.url;
          // let $inpuUrl = $(_this).parents('.input-group').find('input:nth-child(1)');
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



  let sdk = baidubce.sdk;
  let VodClient = sdk.VodClient;

  const CONFIG = {
  endpoint: 'http://vod.bj.baidubce.com',	// 默认区域名
  credentials: {
    ak: '112fec2c658d480dbd35954afa01cea6',	 // 填写你的百度云中ak和sk
    sk: ' 5df7f81a44c6422a'    // 在百度vod 安全认证里面
  }
  };
      // 百度云vod域名在多媒体/全局设置/发布设置里面
  let BAIDU_VOD_DOMAIN = 'jmdsaknupx9e3a9v26c.exp.bcevod.com';	// 百度云VOD域名

  const CLIENT = new VodClient(CONFIG);




  $(function () {
  	// 其他js代码省略
    // ......

  // ================== 上传文件至服务器 ================
  let $upload_file_server = $("#upload-file-server");
  $upload_file_server.change(function () {

    // 先判断课程标题是否为空
    let sTitle = $("#news-title").val();  // 获取课程标题
    if (!sTitle) {
      popBox.showError('请先填写课程标题之后，再上传视频！');
      return
    }

    // 判断课程简介是否为空
    let sDesc = $("#news-desc").val();  // 获取课程简介
    if (!sDesc) {
      popBox.showError('请先填写课程描述之后，再上传视频！');
      return
    }

    let video_file = this.files[0];   // 获取文件
    let video_file_type = video_file.type;

    // 调用百度云VOD接口
    let blob = new Blob([video_file], {type: video_file_type});

    CLIENT.createMediaResource(sTitle, sDesc, blob)
    // Node.js中<data>可以为一个Stream、<pathToFile>；在浏览器中<data>为一个Blob对象
      .then(function (response) {
        // 上传完成
        popBox.showCurrent("视频上传成功");
        let sMediaId = response.body.mediaId;
        console.log('媒资ID为：', sMediaId);
        let sVideoUrl = 'http://' + BAIDU_VOD_DOMAIN + '/' + sMediaId + '/' + sMediaId + '.m3u8';
        $courseFileUrl.val('');
        $courseFileUrl.val(sVideoUrl);

      })
      .catch(function (error) {
        console.log(error);   // 上传错误
        popBox.showError(error)
      });

  });


});



  // ================== 发布文章 ================
  let $docsBtn = $("#btn-pub-news");
  $docsBtn.click(function () {
    // 判断课程标题是否为空
    let sTitle = $("#news-title").val();  // 获取文件标题
    if (!sTitle) {
      popBox.showError('请填写课程标题！');
      return
    }

    // 判断课程简介是否为空
    let sDesc = $("#news-desc").val();  // 获取课程简介
    if (!sDesc) {
      popBox.showError('请填写课程描述！');
      return
    }

    // 判断课程缩略图url是否为空
    let sThumbnailUrl = $thumbnailUrl.val();
    if (!sThumbnailUrl) {
      popBox.showError('请上传课程缩略图');
      return
    }

    // 判断课程url是否为空
    let sCourseFileUrl = $courseFileUrl.val();
    if (!sCourseFileUrl) {
      popBox.showError('请上传视频或输入视频地址');
      return
    }

    // 判断视频时长是否为空
    // let sCourseTime = $('#course-time').val();  // 获取视频时长
    // if (!sCourseTime) {
    //   popBox.showError('请填写视频时长！');
    //   return
    // }

    // 判断是否选择讲师
    let sTeacherId = $("#course-teacher").val();
    if (!sTeacherId || sTeacherId === '0') {
      popBox.showError('请选择讲师');
      return
    }

    // 判断是否选择课程分类
    let sCategoryId = $("#course-category").val();
    if (!sCategoryId || sCategoryId === '0') {
      popBox.showError('请选择课程分类');
      return
    }

    // 判断课程大纲是否为空
    let sContentHtml = $(".markdown-body").html();
    // let sContentHtml = window.editor.txt.html();
    // let sContentText = window.editor.txt.text();
    if (!sContentHtml || sContentHtml === '<p><br></p>') {
        popBox.showError('请填写课程大纲！');
        return
    }

    // 获取coursesId 存在表示更新 不存在表示发表
    let coursesId = $(this).data("news-id");
    let url = coursesId ? '/cms/course/' + coursesId + '/' : '/cms/courses/';
    let data = {
      "title": sTitle,
      "profile": sDesc,
      "cover_url": sThumbnailUrl,
      "video_url": sCourseFileUrl,
      "outline": sContentHtml,
      "teacher": sTeacherId,
      "category": sCategoryId

    };

    $.ajax({
      // 请求地址
      url: url,
      // 请求方式
      type: coursesId ? 'PUT' : 'POST',
      data: JSON.stringify(data),
      // 请求内容的数据类型（前端发给后端的格式）
      contentType: "application/json; charset=utf-8",
      // 响应数据的格式（后端返回给前端的格式）
      dataType: "json",
    })
      .done(function (res) {
        if (res.code === 200) {
          if (coursesId) {
            popBox.showCurrent("课程更新成功");
            setTimeout( window.location.href = '/cms/courses/',1500)

          } else {
            fAlert.alertNewsSuccessCallback("课程发表成功", '跳到课程管理页', function () {
              window.location.href = '/cms/courses_list/'
            });
          }
        } else {
          popBox.showError(res.message);
        }
      })
      .fail(function () {
        popBox.showError('服务器超时，请重试！');
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
