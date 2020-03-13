from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import redis
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm, \
    RegisterPostForm, UploadImageForm, UserInfoForm, ChangePwdForm, UpdateMobileForm
from apps.utils.YunPian import send_single_sms
from apps.utils.random_str import generate_random
from MxOnline.settings import yp_apikey, REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile
from apps.operations.models import UserFavorite, UserMessage
from apps.organizations.models import CourseOrg, Teacher
from apps.courses.models import Course
from apps.operations.models import Banner


class CustomAuth(ModelBackend):
    # 重写ModelBackend的authenticate方法，添加用户手机验证
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def message_nums(request):
    """
    Add message_nums context variables to the context.
    """
    if request.user.is_authenticated:
        return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}


class MyMessageView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        messages = UserMessage.objects.filter(user=request.user)
        current_page = "message"
        for message in messages:
            message.has_read = True
            message.save()

        # 对讲师数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(messages, per_page=2, request=request)
        messages = p.page(page)

        return render(request, "usercenter-message.html", {
            "messages": messages,
            "current_page": current_page
        })


class MyFavCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_course"
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            try:
                course = Course.objects.get(id=fav_course.fav_id)
                course_list.append(course)
            except Course.DoesNotExist as e:
                pass
        return render(request, "usercenter-fav-course.html", {
            "course_list": course_list,
            "current_page": current_page
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfavorg"
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            org = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(org)
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,
            "current_page": current_page
        })


class MyFavOrgView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfavorg"
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
            "current_page": current_page,
        })


class MyCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "mycourse"

        return render(request, "usercenter-mycourse.html", {

            "current_page": current_page
        })


class ChangeMobileView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        mobile_form = UpdateMobileForm(request.POST)
        if mobile_form.is_valid():
            mobile = mobile_form.cleaned_data["mobile"]
            #已经存在的记录不能重复注册
            # if request.user.mobile == mobile:
            #     return JsonResponse({
            #         "mobile": "和当前号码一致"
            #     })
            if UserProfile.objects.filter(mobile=mobile):
                return JsonResponse({
                    "mobile": "该手机号码已经被占用"
                })
            user = request.user
            user.mobile = mobile
            user.username = mobile  # 同时更新时候手机做用户名的状况
            user.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(mobile_form.errors)
            # logout(request)


class ChangePwdView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            # 可以将密码一致性验证放到modelform中进行，定义一个全局的clean
            # pwd1 = request.POST.get("password1", "")
            # pwd2 = request.POST.get("password2", "")
            #
            # if pwd1 != pwd2:
            #     return JsonResponse({
            #         "status":"fail",
            #         "msg":"密码不一致"
            #     })
            pwd1 = request.POST.get("password1", "")
            user = request.user
            user.set_password(pwd1)
            user.save()
            # login(request, user)

            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(pwd_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    login_url = "/login/"

    # def save_file(self, file):
    #     with open("C:/Users/Administrator/PycharmProjects/MxOnline/media/head_image/uploaded.jpg", "wb") as f:
    #         for chunk in file.chunks():
    #             f.write(chunk)

    def post(self, request, *args, **kwargs):
        # 处理用户上传的头像
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })
        # files = request.FILES["image"]  # 上传图片的时候，文件不会放到POST中，而是单独的一个属性FILES中
        # self.save_file(files)

        #1. 如果同一个文件上传多次，相同名称的文件应该如何处理
        #2. 文件的保存路径应该写入到user数据库中
        #3. 还没有做表单验证


class UserInfoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(selfs, request, *args, **kwargs):
        current_page = "info"
        captcha_form = RegisterGetForm()
        return render(request, "usercenter-info.html", {
            "captcha_form": captcha_form,
            "current_page": current_page,
        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(user_info_form.errors)  # errors的返回值就是一个dict类型


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        return render(request, "register.html", {
            "register_get_form": register_get_form,
        })

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]
            # 新建用户，（UserProfile有几个必填的字段）使用手机号做用户名
            user = UserProfile(username=mobile)
            # 使用set_password的自带加密的
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            register_get_form = RegisterGetForm()  # 用于输入验证错误后，返回得到新的验证码
            return render(request, "register.html", {
                "register_get_form": register_get_form,  # 是为了得到那个验证码字段，因为这段使用验证码表单在前端生成的表单
                "register_post_form": register_post_form,  # 用于请求时错误，回显请求时输入的字段，以及报错的内容的html格式，用于在前端显示
            })


class DynamicLoginView(View):
    def get(self, request, *args, **kwargs):
        # 已经在登录了的情况下点击动态登录的话会直接进行跳转到index
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        banners = Banner.objects.all()[:3]
        next = request.GET.get('next', '')
        login_form = DynamicLoginForm()
        return render(request, "login.html", {
            "login_form": login_form,
            "next": next,
            "banners": banners,
        })

    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        dynamic_login = True
        banners = Banner.objects.all()[:3]
        if login_form.is_valid():
            # 对于没有注册的账号，使用手机号码注册的同时依然可以登录
            mobile = login_form.cleaned_data["mobile"]
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                # 新建用户，（UserProfile有几个必填的字段）使用手机号做用户名
                user = UserProfile(username=mobile)
                # 手机验证登录没有密码，设置默认的随机初始密码
                password = generate_random(10, 2)
                # user.password = password
                user.set_password(password)  # 使用Django自带的set_password方法，创建加密的密文密码
                user.mobile = mobile
                user.save()
            login(request, user)
            next = request.GET.get('next', '')  # 此处是无法获得地址的，因为是post请求，所以没有GET，得不到url中的next值
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse("index"))
        else:
            d_form = DynamicLoginForm()
            return render(request, "login.html", {"login_form": login_form,
                                                  "dynamic_login": dynamic_login,
                                                  "d_form": d_form,
                                                  "banners": banners})


class SendSmsView(View):
    """
    发送信息的验证直接放在DynamicLoginForm表中，所以要对默认的DynamicLoginForm表做一点修改
    """
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():  # 此时已经自动完成了验证码的识别，通过DynamicLoginForm中的captcha = CaptchaField()
            mobile = send_sms_form.cleaned_data['mobile']
            # 随机生成数字验证码 （模仿云片网需要的返回给用户的验证码）
            code = generate_random(4, 0)
            re_json = send_single_sms(yp_apikey, code, mobile=mobile)
            if re_json['code'] == 0:
                re_dict['status'] = "success"
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset="utf8", decode_responses=True)
                r.set(str(mobile), code)
                r.expire(str(mobile), 60*5)  # 设置验证码五分钟过期
            else:
                re_dict['msg'] = re_json['msg']
        else:
            for key, value in send_sms_form.errors.items():
                re_dict['key'] = value[0]
        # 因为采用的是ajax的传输方式，所以元素都不在前端页面中，使用render返回数据，模板是拿不到的，此时可以使用JsonResponse
        # 接受的参数为{}，
        return JsonResponse(re_dict)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        """所有继承自View的方法都必须实现相应的请求的方法，被View内的dispatch方法返回，
        因为每次只会返回一种请求类型，并且因为是http_method_names列表中限定好的，
        所以只能是标准的http请求名
        """
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        banners = Banner.objects.all()[:3]
        next = request.GET.get('next', '')
        login_form = DynamicLoginForm()
        return render(request, 'login.html', {
            "login_form": login_form,
            "next": next,
            "banners": banners,
        })

    def post(self, request, *args, **kwargs):
        """完成登录 验证的逻辑
        获取表单对象的时候，字段就是对应的name的值
        """
        banners = Banner.objects.all()[:3]
        # Django提供的表单验证：只是根据定义的要求，对数据格式方法进行验证，对于正确性，用户名和密码是否对应这个验证还是需要交给authenticate
        login_form = LoginForm(request.POST)  # django自带的表单功能除了有验证功能，还可以对数据进行一定的处理
        if login_form.is_valid():  # 会对字段进行LoginForm中设置的类型进行基本的验证，即是否有值，长度是否符合进行验证，错误信息显示在error属性中
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=password)  # 自带的用户名和密码验证功能，用于通过用户名和密码查询用户是否存在，不存在时为None
            if user is not None:
                # 查询到用户
                login(request, user)  # 自动完成session的设置，如何取到user对应的sessionid，以及如何将sessionid传递到cookie中都自动完成
                next = request.GET.get('next', '')  # 此处是无法获得地址的，因为是post请求，所以没有GET，得不到url中的next值
                if next:
                    return HttpResponseRedirect(next)
                # 登录成功后应该如何返回页面
                return HttpResponseRedirect(reverse("index"))
            else:
                # 未查询到用户
                return render(request, "login.html", {"msg": "用户名或 密码错误", "login_form": login_form, 'banners': banners })
        else:
            return render(request, "login.html", {"login_form": login_form, 'banners': banners})










