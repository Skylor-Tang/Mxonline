# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 22:39
# @Author  : Skylor Tang
# @Email   : 
# @File    : adminx.py
# @Software: PyCharm


import xadmin

from apps.organizations.models import Teacher, CourseOrg, City


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']
    style_fields = {
        "desc": "ueditor",
    }


class CityAdmin(object):
    list_display = ['id', 'name', 'desc']  # 列表页可以显示的字段，字段名必须是创建表时类的属性名 id是未指明PRIMARY KEY时默认自动创建的
    search_fields = ['name', 'desc']  # 指明搜索的时候可以搜索的字段名（列）
    list_filter = ['name', 'desc', 'add_time']  # 设置可以过滤的字段
    list_editable = ['name', 'desc']  # 配置可以直接在展示就可以修改的字段名（列）


xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(City, CityAdmin)
