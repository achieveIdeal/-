class LoginClass {
  constructor() {
    this.loginBtn = $('.login-btn')
  }

  sendLoginData() {
    var self = this
    self.loginBtn.click(function (e) {
      e.preventDefault();
      var login = $('.login-contain')
      var mobile = login.find('input[name="mobile"]').val();
      var password = login.find('input[name="password"]').val();
      var remember = login.find('input[name="remember"]').prop('checked')
      Ajax.post({
        'url': '/user/login/',
        'data': {
          'mobile': mobile,
          'password': password,
          'remember': remember
        },
        'success': function (data) {
          if (data.code === 200) {
            window.location.href = document.referrer
          } else {
            console.log(data.message);
            popBox.showError(data.message)
          }
        }
      })
    })
  }

  run() {
    this.sendLoginData();
  }

}

var signin = new LoginClass();
signin.run();