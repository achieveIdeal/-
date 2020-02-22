class NewCaregory {
  constructor() {

  }

  run() {
    this.addNewsEvent();
    this.editNewsCategory();
    this.delNewcategory();
  }

  addNewsEvent() {
    let addBtn = $('#add-btn')
    addBtn.click(function () {
      popBox.PopInput({
            'title': '添加一个新闻分类：',
            'placeholder': '请输入',
          },
          (value) => {
            Ajax.post({
              'url': '/cms/news_tags/',
              'data': {
                'name': value
              },
              'success': function (data) {
                if (data.code === 200) {
                  window.location.reload()
                } else {
                  popBox.showError(data.message);
                }
              }
            })
          })
    })
  }

  editNewsCategory() {
    let editBtn = $('.edit-btn');
    editBtn.click(function () {
      let self = $(this)
      let value = self.parent().parent().attr('data-name')
      let pk = self.parent().parent().attr('data-pk')
      popBox.PopInput({
        'title': '修改分类',
        'value': value,
      }, (val) => {
        Ajax.put({
          'url': '/cms/news_tags/',
          data: JSON.stringify({
            pk: pk,
            name: val
          },),
          // 请求内容的数据类型（前端发给后端的格式）
          contentType: "application/json; charset=utf-8",
          // 响应数据的格式（后端返回给前端的格式）
          dataType: "json",
          async: false,
          success: (data) => {
            if (data.code === 200) {
              window.location.reload()
            } else {
              popBox.showError(data.message)
            }
          }
        })
      })
    })
  }

  delNewcategory() {
    let delBtn = $('.del-btn')
    delBtn.click(function () {
      let self = $(this)
      let value = self.parent().parent().attr('data-name');
      let pk = self.parent().parent().attr('data-pk');
      console.log(pk);
      popBox.tooltip({
        'title': '确定要删除吗？',
        'danger': true
      }, function (value) {
        if (value) {
          Ajax.delete({
            'url': '/cms/news_tag/' + pk + '/',
            'success': function (data) {
              if (data.code === 200) {
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


var addCategory = new NewCaregory();
addCategory.run();