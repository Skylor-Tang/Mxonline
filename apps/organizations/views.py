from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q

from apps.organizations.models import CourseOrg, City, Teacher
from apps.organizations.forms import AddAskForm
from apps.operations.models import UserFavorite


class TeacherDetailView(View):

    def get(self, request, teacher_id, *args, **kwargs):
        teacher = Teacher.objects.get(id=int(teacher_id))

        teacher_fav = False
        org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                org_fav = True

        # 讲师排行榜
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "teacher_fav": teacher_fav,
            "org_fav": org_fav,
            "hot_teachers": hot_teachers,
        })


class TeacherListView(View):
    def get(self, request, *args, **kwargs):
        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()

        # 讲师排行榜
        hot_teachers = all_teachers.order_by("-click_nums")[:3]

        keywords = request.GET.get("keywords", '')
        search_type = "teacher"
        if keywords:
            # 使用like语句
            all_teachers = all_teachers.filter(Q(name__icontains=keywords))

        # 对讲师进行排序
        sort = request.GET.get("sort", '')
        if sort == "hot":
            all_teachers = all_teachers.order_by("-click_nums")

        # 对课程机构讲师数据进行分页, 调用第三方库django-pure-pagination
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, per_page=3, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html',{
            "teachers": teachers,
            "teacher_nums": teacher_nums,
            "sort": sort,
            'hot_teachers': hot_teachers,
            "search_type": search_type,
            "keywords": keywords,
        })


class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 设置收藏的标记
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,

        })


class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 设置收藏的标记
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        all_courses = course_org.course_set.all()

        # 对课程机构数据进行分页, 调用第三方库django-pure-pagination
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=3, request=request)
        courses = p.page(page)

        return render(request, "org-detail-course.html", {
            "all_courses": courses,
            "course_org": course_org,    # 该对象每次都要传递，因为使用该变量的为模板的公共部分
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 设置收藏的标记
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        all_teacher = course_org.teacher_set.all()
        return render(request, "org-detail-teachers.html", {
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))  # 此处使用get，因为是从列表页获得的id来的，该id一定是存在的
        course_org.click_nums += 1
        course_org.save()

        # 设置收藏的标记
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]
        return render(request, "org-detail-homepage.html", {
            "all_courses": all_courses,
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class AddAskView(View):
    """
    处理用户的咨询
    """
    def post(self, request, *args, **kwargs):
        userask_form = AddAskForm(request.POST)   # 表单对象均要接受request.POST参数，获取上传的表单的值
        if userask_form.is_valid():
            # modelform同时具有form和model的特性，使用model的save()方法，即可将数据存放到对应的数据库
            # 但是一定要设置commit=True参数（默认是该参数），表示将表单数据保存到数据库
            # 若commit设置为False，则是生成一个数据库model对象，可以对该对象进行增删改查之后，再使用save()进行保存
            userask_form.save(commit=True)  # 无论commit参数如何，该方法均返回一个数据库对象，区别是保存到数据库没有
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "添加出错"
            })


class OrgView(View):

    def get(self, request, *args, **kwargs):
        """
        授课机构的整个显示的逻辑过程就是对数据进行筛选，所以在开始的时候获得所有的数据对象，
        在之后进行各种过滤操作，最后显示
        之所以能进行各种筛选是因为每次操作后的数据类型都是QuerySet类型，所以可以进行重复操作

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 从数据库中获取数据
        all_orgs = CourseOrg.objects.all()
        all_citys = City.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 搜索关键词-- 全局搜索功能组件
        keywords = request.GET.get("keywords", '')
        search_type = 'org'
        if keywords:
            # 使用like语句
            all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        # 通过机构类别对课程机构进行筛选 通过get传进的参数进行判断
        category = request.GET.get('ct', "")  # 因为GET属性是一个dict对象
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 通过所在城市对课程机构进行筛选
        city_id = request.GET.get('city', "")
        if city_id:  # 注意前端传递过来的是个字符串，所以此处要使用int进行转换
            # 因为是通过get传递参数的方式接受值的，所以用户可以直接在url中添加参数，为了防止错误
            # 如用户传递一个非数字的内容，这里int转换就会异常，所以添加一个判断
            if city_id.isdigit():
                # 这里的all_rogs在上面的筛选之后再次进行筛选，使满足两个条件
                all_orgs = all_orgs.filter(city_id=int(city_id))

        # 对机构进行排序 （注意顺序，写在次数时，上面的过滤依然有效）
        sort = request.GET.get("sort", '')
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")


        # 统计的调用对象为all_orgs，是经过筛选之后的数据的统计（所以放在了最后）
        org_nums = all_orgs.count()

        # 对课程机构数据进行分页, 调用第三方库django-pure-pagination
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, per_page=3, request=request)
        orgs = p.page(page)
        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "org_nums": org_nums,
            "all_citys": all_citys,
            "category": category,       # 将这些选择的字段你都带上，保存每次的选择状态
            "city_id": city_id,
            "sort": sort,
            "hot_orgs": hot_orgs,
            "keywords": keywords,
            "search_type": search_type,
        })

