__author__ = 'zhuol_000'
from django import forms
from InfoUpei.models import Course
from InfoUpei.models import UserProfile
from django.contrib.auth.models import User


class AddCourseForm(forms.ModelForm):

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Course
        fields = ('name','course_description_text','course_description_file')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model=UserProfile
        fields=('first_name','middle_name','last_name','website','picture','birthday','role')


class RegisterCourseForm(forms.Form):
    course_list=forms.ModelChoiceField(queryset=Course.objects.all())

    def __str__(self):
        return "register_course_form:"


