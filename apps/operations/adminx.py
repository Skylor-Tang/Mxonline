# -*- coding: utf-8 -*-
# @Time    : 2019/11/2 8:54
# @Author  : Skylor Tang
# @Email   : 
# @File    : adminx.py
# @Software: PyCharm


import xadmin

from apps.operations.models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse, Banner


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', "index"]
    search_fields = ['title', 'image', 'url', "index"]
    list_filter = ['title', 'image', 'url', "index"]


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_time']


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']

    def save_models(self):
        '''
        在后台管理系统中对数据进行保存时会经过该操作
        :return:
        '''
        obj = self.new_obj  # 当修改操作时，该属性的id为添加的数据ID，当是添加的时候没有值为None
        if not obj.id:  # 该对象，实际就是usercourse的表数据对象。
            obj.save()
            course = obj.course
            course.students += 1
            course.save()
            send_message = UserMessage(user=obj.user)
            send_message.message = "欢迎学习"+obj.course.name+"课程"
            send_message.save()




xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
