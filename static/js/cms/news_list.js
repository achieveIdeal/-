function CMSNewsList() {

}

CMSNewsList.prototype.deleteNews = function () {
  var deleteBtn = $('.del-staff');
  deleteBtn.click(function (e) {
    e.preventDefault();
    var user_id = $(this).attr('data-usrid');

    popBox.tooltip({
      'title': '确认要删除吗？',
      'danger': true
    }, function (value) {
      if (value) {
        Ajax.delete({
          'url': '/cms/del_staff/' + user_id + '/',
          'success': function (data) {
            if (data.code === 200) {
              console.log(data);

              popBox.showCurrent('删除成功');
              // window.location.reload()

            } else {
              popBox.showError(data.message)
            }
          }
        })
      }
    })
  })
}


CMSNewsList.prototype.initDatapicker = function () {
  var startPicker = $('#start-packer')
  var endPicker = $('#end-picker')
  var data = new Date()
  var todayStr = data.getFullYear() + '/' + (data.getMonth() + 1) + '/' + data.getDate()
  var options = {
    'showButtonPanel': true,
    'format': 'yyyy/mm/dd',
    'startDate': '2018/12/1',
    'endDate': todayStr,
    'todayHighlight': 'linked', //是否高亮显示选中的日期
    'language': 'zh-CN',
    'todayBtn': true, //是否显示今天的按钮
    'autoclose': true  //是否显示清除按钮
  }
  startPicker.datepicker(options) //点击会显示日历
  endPicker.datepicker(options)

}

CMSNewsList.prototype.run = function () {
  this.initDatapicker();
  this.deleteNews()
}

$(function () {
  var cmsNewsList = new CMSNewsList()
  cmsNewsList.run()
})