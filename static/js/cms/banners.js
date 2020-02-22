class Banners {
  constructor() {

  }

  run() {
    this.loadBannerData();
    this.listenAddBanner();
  }

  //添加轮播图
  listenAddBanner() {
    var bannerListGroup = $('.banner-list-group');
    var self = this;
    var btn = $('#add-banner-btn');

    btn.click(function () {
      var bannerItemLength = bannerListGroup.children().length;
      if (bannerItemLength >= 6) {
        popBox.showError('轮播图最多只能添加6张！');
        return
      }
      self.addBannerTemplate()
    })
  }

//添加轮播图模板
  addBannerTemplate(banner = null) {
    var self = this;
    var tpl = null;
    var bannerListGroup = null;
    var bannerItem = null
    if (!banner) {
      tpl = template('banner-item')
      bannerListGroup = $('.banner-list-group')
      bannerListGroup.prepend(tpl)
      bannerItem = bannerListGroup.find('.banner-item:first')

    } else {
      tpl = template('banner-item', {'banner': banner})
      bannerListGroup = $('.banner-list-group')
      bannerListGroup.append(tpl)
      bannerItem = bannerListGroup.find('.banner-item:last')

    }

    self.addImageSelectEvent(bannerItem)
    self.removeBannerEvent(bannerItem)
    self.saveBannaerEvent(bannerItem)
  }

//加载轮播图数据
  loadBannerData() {
    var self = this;
    Ajax.get({
      'url': '/cms/banner_list/',
      'success': function (data) {
        var banners = data.data;
        for (var i = 0; i < banners.length; i++) {
          self.addBannerTemplate(banners[i])
        }
      }
    })
  }

//上传缩略图
  addImageSelectEvent(bannerItem) {
    var fileIbput = bannerItem.find('.thumbnail-input')
    var image = bannerItem.find('.thumbnail')
    image.click(function () {
      fileIbput.click();
      fileIbput.change(function () {
        var file = this.files[0];
        var formData = new FormData();
        formData.append('file', file)
        Ajax.post({
          'url': '/cms/up_thumbnail/',
          'data': formData,
          'processData': false,
          'contentType': false,
          'success': function (data) {
            if (data.code === 200) {
              var url = data.data.url;
              image.prop('src', url)
            }
          }
        })
      })
    })
  }

//删除轮播图
  removeBannerEvent(bannerItem) {
    var closeBtn = bannerItem.find('#close-btn');
    closeBtn.click(function () {
      var bannerId = bannerItem.attr('data-banner-id');
      if (!bannerId) {
        bannerItem.remove()
      } else {
        popBox.tooltip({
          'title': '确定要删除吗？',
          'danger': true
        }, function (value) {
          Ajax.delete({
            'url': '/cms/banner/' + bannerId + '/',
            'success': function (data) {
              if (data.code === 200) {
                popBox.showCurrent('删除成功');
                bannerItem.remove();
              }
            }
          })

        })

      }
    })
  }

  myrefresh() {
    window.location.reload();
  }

//保存轮播图
  saveBannaerEvent(bannerItem) {
    var self = this;
    var saveBannerBtn = bannerItem.find('#save-banner-btn');
    var imageTag = bannerItem.find('.thumbnail');
    var priorityTag = bannerItem.find('input[name="priority"]');
    var link_toTag = bannerItem.find('input[name="news_id"]');
    var prioritySpan = bannerItem.find('.priority');

    saveBannerBtn.click(function () {
      var img_url = imageTag.attr('src');
      var priority = parseInt(priorityTag.val());
      var news_id = link_toTag.val();
      let bannerId = bannerItem.attr('data-banner-id');
      var url = null;
      var data = {
        'pk': bannerId,
        'priority': priority,
        'image_url': img_url,
        'news_id': news_id,
      };
      let type = '';
      if (!bannerId) {
        url = '/cms/banners/';
        type = 'post'
      } else {
        url = '/cms/banner/' + bannerId + "/";
        data = JSON.stringify(data);
        type = 'put';
      }
      Ajax.request_({
        'url': url,
        'type': type,
        'data': data,
        'success': function (data) {
          if (data.code === 200) {
            if (bannerId) {
              popBox.showCurrent('修改完成');
              setTimeout(self.myrefresh, 1500);

            } else {
              window.popBox.showCurrent('保存成功');
              bannerItem.attr('data-banner-id', data.data.banner_id)
              setTimeout(self.myrefresh, 1500);

            }
            prioritySpan.text('优先级：' + data.data.priority)

          } else {
            popBox.showError(data.message)
          }
        }
      })
    })
  }

}

$(function () {
  var banners = new Banners();
  banners.run()
});