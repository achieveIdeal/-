class PopOut {
  constructor() {

  }

  popUp(message, icon) {
    swal({
      'title': message ? message : 'nothing',
      'icon': icon,
      'buttons': false,
      'timer': 4000,
      'closeOnClickOutside': true,
      'closeOnEsc': false,
    })
  }

  tooltip(params,callback=null) {

    swal({
      'title': params.title ? params.title : 'nothing',
      'buttons':
          {
            cancel: {
              text: "取消",
              value: null,
              visible: true,
            },
            confirm: {
              text: "确认",
              value: true,
            }
          },
      dangerMode: params.danger,
    }).then((value)=>{
      if (value&&callback) return callback(value)
    })
  }

  showError(message) {
    this.popUp(message, 'error')
  }

  showCurrent(message) {
    this.popUp(message, 'success')
  }

  showInfo(message) {
    this.popUp(message, 'info')
  }

  showwarning(message) {
    this.popUp(message, 'warning')
  }

  PopInput(params, callback) {
    let self = this;
    swal({
      'title': params.title ? params.title : '',
      'text': params.text ? params.text : '',
      'content': {
        'element': 'input',
        'attributes': {
          'placeholder': params.placeholder ? params.placeholder : '',
          'value': params.value ? params.value : '',
          'type': 'text'
        }
      },
      'buttons': {
        cancel: {
          text: "取消",
          value: null,
          visible: true,
        },
        confirm: {
          text: "确定",
          value: true,
        },
      },
    }).then((value) => {
      if (!callback) {
        self.showError('callback不能为空')
      } else {
        if (!value) return null;
        callback(value)
      }
    })
  }

}



var popBox = new PopOut();
