# -*- coding: utf-8 -*-
# @Time    : 2020/3/1 20:40
# @Author  : Skylor Tang
# @Email   : 
# @File    : urls.py.py
# @Software: PyCharm


from django.conf.urls import url
from apps.operations.views import AddFavView, CommentView

urlpatterns = [
    # 用户收藏
    url(r'^fav/$', AddFavView.as_view(), name='fav'),
    # 用户评论
    url(r'^comment/$', CommentView.as_view(), name='comment'),
]