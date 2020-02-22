class Staff {
  constructor () {

  }

  delStaff () {
    let delBtn = $('.del-staff');
    delBtn.click(function () {
      let self = $(this);
      let user_id = self.attr('data-usrid');
      popBox.tooltip({
      'title': '确认要删除吗？',
      'danger': true
    }, function (value) {
      if (value) {
        Ajax.delete({
          'url': '/cms/del_staff/'+user_id + '/',
          'success': function (data) {
            if (data.code === 200) {
              popBox.showCurrent('删除成功');
              window.location.reload()

            } else {
              popBox.showError(data.message)
            }
          }
        })
      }
      })
    })

  }

}

$(function () {
  let staff = new Staff();
  staff.delStaff()
})