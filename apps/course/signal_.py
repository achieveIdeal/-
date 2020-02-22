from django.db.models.signals import post_save  #模型信号

from django.dispatch import receiver  #接收信号并分发

from users.models import MyUser

@receiver(post_save,sender=MyUser)  #必须定义在模型中，或者在模型的最后导入
def siginal_test(sender,**kwargs):
    created = kwargs.get('created',False)  #获取当模型save之后会自动传递的created参数为True。
    if created:
        instance = kwargs.get('instance',None)
        print(instance)
