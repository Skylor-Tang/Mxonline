# -*- coding: utf-8 -*-
# @Time    : 2020/3/1 20:40
# @Author  : Skylor Tang
# @Email   : 
# @File    : urls.py.py
# @Software: PyCharm


from django.conf.urls import url
from apps.courses.views import CourseListView, CourseDetailView, CourseLessonView, CourseCommentsView, VideoView

urlpatterns = [
    # 课程列表
    url(r'^list/$', CourseListView.as_view(), name='list'),  # 因为使用了命名空间，所以之前的命令和此处冲突没有问题

    # 课程详情
    url(r'^(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="detail"),

    # 课程详情
    url(r'^(?P<course_id>\d+)/lesson/$', CourseLessonView.as_view(), name="lesson"),

    # 课程评论
    url(r'^(?P<course_id>\d+)/comments/$', CourseCommentsView.as_view(), name="comments"),

    # 视频播放
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)$', VideoView.as_view(), name="video"),
]