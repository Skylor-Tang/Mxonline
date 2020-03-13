# -*- coding: utf-8 -*-
# @Time    : 2020/2/28 19:02
# @Author  : Skylor Tang
# @Email   : 
# @File    : urls.py.py
# @Software: PyCharm

from django.urls import path
from django.conf.urls import url, include

from apps.organizations.views import OrgView, AddAskView, OrgHomeView, OrgTeacherView, OrgCourseView, \
    OrgDescView, TeacherListView, TeacherDetailView

urlpatterns = [
    url(r'list/$', OrgView.as_view(), name="list"),
    url(r'add_ask/$', AddAskView.as_view(), name="add_ask"),
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="home"),
    url(r'^(?P<org_id>\d+)/teacher/$', OrgTeacherView.as_view(), name="teacher"),
    url(r'^(?P<org_id>\d+)/course/$', OrgCourseView.as_view(), name="course"),
    url(r'^(?P<org_id>\d+)/desc/$', OrgDescView.as_view(), name="desc"),

    # 讲师列表页
    url(r'^teachers/$',  TeacherListView.as_view(), name="teachers"),
    # 讲师详情页
    url(r'^teachers/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),

]
