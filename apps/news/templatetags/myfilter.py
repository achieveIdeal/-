from django import template
from datetime import datetime                       #将utc时间转换为本地（settings中的时间）时间
from django.utils.timezone import now as native_now,localtime

register = template.Library()

@register.filter
def time_since(value):
    # try:
    #     value = datetime.strptime(value,'%Y-%m-%d %H:%M:%s')
    # except:
    #     value = value[0:20]
    #     print(value)
    #     print('装换失败')
    #     return value
    if isinstance(value,datetime):

        now = localtime(native_now())
        '''获取时间间隔秒'''
        timestamp = (now-value).total_seconds()

        if timestamp<60:
            return '刚刚'
        elif timestamp>60 and timestamp<60*60:
            minutes = int(timestamp/60)
            return '%s分钟前'%minutes
        elif timestamp>60*60 and timestamp<60*60*24:
            hours = int(timestamp/60/60)
            return '%s小时前'%hours
        elif timestamp>60*60*24 and timestamp<60*60*20*30:
            days = int(timestamp/60/60/24)
            return '%s天前'%days
        else:
            return datetime.strftime(value,'%Y年%m月%d日 %H:%M:%S')
    else:
        return value



@register.filter()
def page_bar(page):
    page_list = []
    # 左边
    if page.number !=1:
        page_list.append(1)
    if page.number -3 >1:
        page_list.append('...')
    if page.number -2 >1:
        page_list.append(page.number -2)
    if page.number - 1>1:
        page_list.append(page.number-1)

    page_list.append(page.number)
    # 右边
    if page.paginator.num_pages >page.number + 1:
        page_list.append(page.number+1)

    if page.paginator.num_pages >page.number+2:
        page_list.append(page.number+2)
    if page.paginator.num_pages > page.number+3:
        page_list.append('...')
    if page.paginator.num_pages != page.number:
        page_list.append(page.paginator.num_pages)
    return page_list

