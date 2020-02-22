from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, mobile, username, password, email,**extra_fields):
        print(password)
        if not mobile:
            raise ValueError('必须传递telephone')
        if not password:
            raise ValueError('必须传递password')
        user = self.model(mobile=mobile, username=username,password=password, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,  mobile, username, password, email=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user( mobile, username, password, email, **extra_fields)

    def create_superuser(self, mobile, username, password, email=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(mobile, username, password, email, **extra_fields)


class MyUser(AbstractUser):
    mobile = models.CharField(max_length=11,unique=True,
                              verbose_name='手机号',
                              error_messages={
                                  'unique': '手机号不唯一'
                              })
    email_ac = models.BooleanField(default=False,verbose_name='邮箱状态')
    email = models.EmailField(default=None,null=True,max_length=100)
    USERNAME_FIELD = 'mobile'   #指定登录时验证的字段
    REQUIRED_FIELDS = ['username']  # 创建用户时必须指定的字段
    objects = UserManager()
    class Meta:
        db_table = 'my_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<%s>"%self.username


