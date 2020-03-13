# -*- coding: utf-8 -*-
# @Time    : 2020/3/1 13:52
# @Author  : Skylor Tang
# @Email   : 
# @File    : forms.py
# @Software: PyCharm
import re

from django import forms
from apps.operations.models import UserAsk


class AddAskForm(forms.ModelForm):
    mobile = forms.CharField(max_length=11, min_length=11, required=True)

    class Meta:
        model = UserAsk
        fields = ["name", "mobile", "course_name"]  # 指明生成form表单的字段

    def clean_mobile(self):  # 是使用clean_字段名，或自动验证
        """
        验证手机号码是否合法
        :return:
        """
        mobile = self.cleaned_data["mobile"]  # 提取form表单传递过来的值
        regex_mobile = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")
