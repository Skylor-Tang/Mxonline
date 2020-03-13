from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER_CHOICES = (
    ("male", "男"),
    ("female", "女"),
)


class BaseModel(models.Model):
    # 注意这里的datetime不要直接使用now()方法，理由是这里实际是类的一个类属性，如果使用now()的话，会在编译的时候（创建类）
    # 的时候，就调用了now()，这个时间是不对的，不应该写方法的调用，而该是传递一个方法
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        abstract = True  # 设置了之后，就不会将这个类创建为一个数据表了，这样就可以只用来做继承表了


class UserProfile(AbstractUser):
    # nick_name = models.CharField(max_length=50, verbose_name="昵称", null=True, blank=True)  # 字段允许为空或不填
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default='')  # 与不填时使用默认值
    birthday = models.DateTimeField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(verbose_name='性别', choices=GENDER_CHOICES, max_length=6)  # 因为female是6个字符，所以按照最大长度来
    address = models.CharField(max_length=100, verbose_name="地址", default="")
    mobile = models.CharField(max_length=11, verbose_name="手机号码")  # unique=True表示该字段不能重复
    # 使用Django自带的ImageField （文件上传的是FileField），能够将图片（文件）自动上传至指定的目录，比如我们设置了media最为默认的文件目录，
    # upload_to会自动在media带中创建upload_to中设置的子路径进行文件的保存
    # ImageField实际上本质上也是一个CharField，是将文件的地址存起来，所以若是我们想设置默认的图片，则可以设置default即可，即使用默认的default中的图片做头像
    # 另外需要注意的是，ImageField 依赖第三方的包pillow
    image = models.ImageField(verbose_name="用户头像", upload_to="head_image/%Y/%m", default="default.jpg")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def unread_nums(self):
        # 未读消息的数量
        return self.usermessage_set.filter(has_read=False).count()

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username  # username是AbstractUser的必备的类属性，继承了AbstractUser后能够使用

