function Ajax_() {
}

Ajax_.prototype.request_ = function (obj, kwargs=null) {
  obj.headers = {"X-CSRFToken": $.cookie('csrftoken')}
  $.ajax(obj)
};
Ajax_.prototype.get = function (obj) {
  obj.type = 'get';
  this.request_(obj)
};
Ajax_.prototype.post = function (obj) {
  obj.type = 'post';
  this.request_(obj)
};
Ajax_.prototype.put = function (obj) {
  obj.type = 'put';
  this.request_(obj)
};
Ajax_.prototype.delete = function (obj) {
  obj.type = 'delete';
  this.request_(obj)
};
Ajax_.prototype.patch = function (obj) {
  obj.type = 'patch';
  this.request_(obj)
};



var Ajax = new Ajax_();


