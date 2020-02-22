from django.http import JsonResponse

'''
3xx（重定向）)表示要完成请求，需要进一步操作。通常，这些状态代码用来重定向。代码说明300(多种选择)针对请求，服务器可执行多种操作。服务器可根据请求者(users agent)选择一项操作，或提供操作列表供请求者选择
301--（永久移动）请求的网页已永久移动到新位置。服务器返回此响应(对GET或HEAD请求的响应)时，会自动将请求者转到新位置
302--(临时移动)服务器目前从不同位置的网页响应请求，但请求者应继续使用原有位置来进行以后的请求
303--(查看其他位置)请求者应当对不同的位置使用单独的GET请求来检索响应时，服务器返回此代码
304--(未修改)自从上次请求后，请求的网页未修改过。服务器返回此响应时，不会返回网页内容
305--(使用代理)请求者只能使用代理访问请求的网页。如果服务器返回此响应，还表示请求者应使用代理
307--(临时重定向)服务器目前从不同位置的网页响应请求，但请求者应继续使用原有位置来进行以后的请求
400–（请求错误）这些状态代码表示请求可能出错，妨碍了服务器的处理
400--（错误请求）)服务器不理解请求的语法
401--（未授权）请求要求身份验证。对于需要登录的网页，服务器可能返回此响应
403--(禁止)服务器拒绝请
404--(未找到)服务器找不到请求的网页
405--(方法禁用)禁用请求中指定的方法
406--(不接受)无法使用请求的内容特性响应请求的网页
407--(需要代理授权)此状态代码与401(未授权)类似但指定请求者应当授权使用代理
408--(请求超时)服务器等候请求时发生超时
409--(冲突)服务器在完成请求时发生冲突。服务器必须在响应中包含有关冲突的信息
410--(已删除)如果请求的资源已永久删除，服务器就会返回此响应
411--(需要有效长度)服务器不接受不含有效内容长度标头字段的请求
412--(需要有效长度)服务器不接受不含有效内容长度标头字段的请求
413--(请求实体过大)服务器无法处理请求，因为请求实体过大，超出服务器的处理能力
414--(请求的URI过长)请求的URI(通常为网址)过长，服务器无法处理
415--(不支持的媒体类型)请求的格式不受请求页面的支持
416--(请求范围不符合要求)如果页面无法提供请求的范围，则服务器会返回此状态代码
417--(未满足期望值)服务器未满足"期望"请求标头字段的要求
500--(服务器内部错误)服务器遇到错误，无法完成请求
501--(尚未实施)服务器不具备完成请求的功能。例如，服务器无法识别请求方法时可能会返回此代码
502--(错误网关)服务器作为网关或代理，从上游服务器收到无效响应
503--(服务不可用)服务器目前无法使用(由于超载或停机维护)。通常，这只是暂时状态
504--(网关超时)服务器作为网关或代理，但是没有及时从上游服务器收到请求
505--(HTTP版本不受支持)服务器不支持请求中所用的HTTP协议版本**
'''


class ToJsonData():
    __ok = 200  #请求顺利
    __paramserr = 400  # 参数错误
    __unauth = 401  # 验证错误
    __methoderr = 405  # 请求方法错误
    __servererr = 500 #  服务器错误

    def __result(self,code,message,data,**kwargs):
        json_data = {
            'code':code,
            'message': message,
            'data': data
        }
        if kwargs and isinstance(kwargs,dict) and kwargs.keys():
            json_data.update(kwargs)
        return JsonResponse(json_data)

    def ok(self,message='ok',data=None,**kwargs):
        return self.__result(self.__ok,message,data,**kwargs)

    def paramserr(self,message,data=None,**kwargs):
        return self.__result(self.__paramserr,message,data,**kwargs)

    def unauth(self,message,data=None,**kwargs):
        return self.__result(self.__unauth,message,data,**kwargs)

    def methoderr(self,message,data=None,**kwargs):
        return self.__result(self.__methoderr,message,data,**kwargs)

    def servererr(self,message,data=None,**kwargs):
            return self.__result(self.__servererr,message,data,**kwargs)

from django.http import JsonResponse

# class Code:
#     OK = "0"
#     DBERR = "4001"
#     NODATA = "4002"
#     DATAEXIST = "4003"
#     DATAERR = "4004"
#     METHERR = "4005"
#     SMSERROR = "4006"
#     SMSFAIL = "4007"
#
#     SESSIONERR = "4101"
#     LOGINERR = "4102"
#     PARAMERR = "4103"
#     USERERR = "4104"
#     ROLEERR = "4105"
#     PWDERR = "4106"
#
#     SERVERERR = "4500"
#     UNKOWNERR = "4501"
#
#
# error_map = {
#     Code.OK: "成功",
#     Code.DBERR: "数据库查询错误",
#     Code.NODATA: "无数据",
#     Code.DATAEXIST: "数据已存在",
#     Code.DATAERR: "数据错误",
#     Code.METHERR: "方法错误",
#     Code.SMSERROR: "发送短信验证码异常",
#     Code.SMSFAIL: "发送短信验证码失败",
#
#     Code.SESSIONERR: "用户未登录",
#     Code.LOGINERR: "用户登录失败",
#     Code.PARAMERR: "参数错误",
#     Code.USERERR: "用户不存在或未激活",
#     Code.ROLEERR: "用户身份错误",
#     Code.PWDERR: "密码错误",
#
#     Code.SERVERERR: "内部错误",
#     Code.UNKOWNERR: "未知错误",}
#
#
# def to_json_data(errno=Code.OK, errmsg='', data=None, **kwargs):
#     json_dict = {'errno': errno, 'errmsg': errmsg, 'data': data}
#
#     if kwargs:
#         json_dict.update(kwargs)
#
#     return JsonResponse(json_dict)