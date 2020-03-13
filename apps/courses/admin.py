from django.contrib import admin
from apps.courses.models import Course
# Register your models here.


class NewCourseAdmin(admin.ModelAdmin):
    list_display = ["teacher", 'name', 'desc', 'show_image', 'go_to', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ['degree', 'desc']
    readonly_fields = ['students', 'add_time']
    exclude = ['click_nums', 'fav_nums']
    ordering = ['-click_nums']


admin.site.register(Course, NewCourseAdmin)