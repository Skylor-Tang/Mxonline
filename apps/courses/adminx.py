# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 22:39
# @Author  : Skylor Tang
# @Email   : 
# @File    : adminx.py
# @Software: PyCharm


import xadmin
from xadmin import views

from import_export import resources

from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag, BannerCourse
from xadmin.layout import Fieldset, Main, Side, Row



class GlobalSettings(object):
    site_title = "慕学网后台管理系统"  # 左上角标题（网站的主题）
    site_footer = "慕学在线网"  # 页脚标题
    # menu_style = "accordion"  # 菜单风格 设置了就是可伸缩的， 默认不设置的时候是全部显示，不可伸缩


class BaseSettings(object):
    """xadmin 提供的主题的功能，默认是关闭的"""
    enable_themes = True  # 开启主题功能
    use_bootswatch = True  # 使用bootstrip主题样式库， 注意一定要设置为True


class CourseAdmin(object):
    list_display = ["teacher", 'name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ['degree', 'desc']


class LessonInline(object):
    model = Lesson
    # style = 'tab' # 用于设置显示数据的样式
    extra = 0  # 用于设置，是否要自动打开一个tab，值为打开的个数
    exclude = ['add_time']  # 设置隐藏的字段


class CourseResourceInline(object):
    model = CourseResource
    style = 'tab'
    extra = 1


class MyResource(resources.ModelResource):
    class Meta:
        model = Course
        # fields = ('name', 'description',)
        # exclude = ()


class NewCourseAdmin(object):
    import_export_args = {'import_resource_class': MyResource, 'export_resource_class': MyResource}
    list_display = ["teacher", 'name', 'desc', 'show_image', 'go_to', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ['degree', 'desc']
    readonly_fields = ['click_nums', 'fav_nums', 'students', 'add_time']
    # exclude = ['click_nums', 'fav_nums']
    ordering = ['-click_nums']
    model_icon = 'fa fa-address-book'
    inlines = [LessonInline, CourseResourceInline]
    style_fields = {
        "detail": "ueditor",
    }

    def queryset(self):
        qs = super(NewCourseAdmin, self).queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher=self.request.user.teacher) # 一对一关系的表可以直接取外键对象
        return qs

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset("讲师信息",
                             'teacher', 'course_org',
                             css_class='unsort no_title'
                             ),
                    Fieldset("基本信息",
                             'name', 'desc',
                             Row('learn_times', 'degree'),
                             Row('category', 'tag'),
                             'youneed_know', 'teacher_tell', 'detail',
                             ),
                ),
                Side(
                    Fieldset("访问信息",
                             'fav_nums', 'click_nums', 'students', 'add_time'
                             ),
                ),
                Side(
                    Fieldset("选择信息",
                             'is_banner', 'is_classics'
                             ),
                )
            )
        return super(NewCourseAdmin, self).get_form_layout()


class CourseTagAdmin(object):
    list_display = ['course', 'tag', 'add_time']
    search_fields = ['course', 'tag']
    list_filter = ['course', 'tag', 'add_time']
    model_icon = 'fa fa-tag'


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]
    model_icon = 'fa fa-image'

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(is_banner=True) # 无论谁查看，该项中只显示标记为轮播图的课程信息
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']
    model_icon = 'fa fa-address-book-o'


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']
    model_icon = 'fa fa-video-camera'


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'file', 'add_time']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'add_time']



xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Course, NewCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseTag, CourseTagAdmin)


# 注册xadmin的全局配置
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSettings)

