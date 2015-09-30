from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from InfoUpei.form import AddCourseForm,UserProfileForm,RegisterCourseForm
from InfoUpei.models import Course,UserProfile,Role,StudentProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def index(request):
    context_dict={}
    user=request.user
    logined=False
    if user.is_authenticated():
        try:
            user_profile=UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            user_profile=None
        logined=True
        context_dict={'user':user,'user_profile':user_profile,'logined':logined}

    return render(request,'InfoUPEI/index.html',context_dict)


def user_login(request):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(password=password,username=username)

        if user:
            try:
                profile=UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                profile=None

            if profile and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/InfoUpei/')
            else:
                messages.add_message(request, messages.WARNING, 'Your rango account is disabled or not exist')
                return HttpResponseRedirect("/InfoUpei/")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            messages.add_message(request, messages.WARNING, 'Invalid login details supplied.')
            return HttpResponseRedirect("/InfoUpei/")

    return render(request,'InfoUPEI/login.html')


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/InfoUpei/')


@login_required
def add_course(request):
    user=request.user
    if user.is_authenticated() and UserProfile.objects.get(user=user).role.name.lower() == 'teacher':
        if request.method == 'POST':
                form=AddCourseForm(request.POST)
                if form.is_valid():
                    course=form.save(commit=False)
                    course.instructor=user

                    if 'course_description_file' in request.FILES:
                        course.course_description_file = request.FILES['course_description_file']

                    course.save()

                    return index(request)
                else:
                    print(form.errors)
        else:
            form=AddCourseForm()

        return render(request,'InfoUPEI/add_course.html',{'form':form})

    else:
            messages.add_message(request, messages.WARNING, 'Please use your teacher account to login first')
            return HttpResponseRedirect("/InfoUpei/")


@login_required
def course_menu(request):
    user = request.user
    if user.is_authenticated():
        profile=UserProfile.objects.get(user=user)
        role=profile.role.name.lower()
        if role == 'teacher':
            courses = user.intructor_courses_set.all()
        elif role == 'student':
            student_profile=StudentProfile.objects.get_or_create(student=user)[0]
            courses=student_profile.registered_courses.all()
        elif role == 'hr':
            courses=Course.objects.all()

    return render(request,'InfoUPEI/course_menu.html',{'courses':courses, 'role':role})


@login_required
def register(request):
    user = request.user
    if user.is_authenticated() and UserProfile.objects.get(user=user).role.name.lower() == 'hr':
        registered=False
        if request.method == 'POST':
            profile_form=UserProfileForm(request.POST)

            if profile_form.is_valid():
                profile=profile_form.save(commit=False)

                #both username and password cannot be set by register office,they are generated from the name and birthday of the student
                user_name=profile.first_name+profile.last_name
                password=str(profile.birthday.year)+str(profile.birthday.month)+str(profile.birthday.day)

                # check if there is duplicated user name,if so, add a number to identify them
                duplicated_name_count=UserProfile.objects.filter(first_name=profile.first_name,last_name=profile.last_name).count()
                if duplicated_name_count>0:
                    user_name+=str(duplicated_name_count)

                #Save the student to database
                user=User(password=password,username=user_name)
                user.set_password(password)
                user.save()

                profile.user=user

                # Did the user provide a profile picture?
                # If so, we need to get it from the input form and put it in the UserProfile model.
                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']

                profile.save()
                registered=True

            else:
                print(profile_form.errors)
        else:
            profile_form=UserProfileForm()
        return render(request,'InfoUPEI/register.html',{'profile_form':profile_form,'registered':registered })

    else:
            messages.add_message(request, messages.WARNING, 'Please use your teacher account to login first')
            return HttpResponseRedirect("/InfoUpei/")


@login_required
def register_course(request):
    user = request.user
    registered=False
    course_was_chosen=False

    if user.is_authenticated() and UserProfile.objects.get(user=user).role.name.lower() == 'student':
        if request.method=='POST':
            register_form=RegisterCourseForm(request.POST)
            if register_form.is_valid():
                profile=StudentProfile.objects.get_or_create(student=user)[0]
                chosen_course_name=register_form.cleaned_data['course_list']
                chosen_course=Course.objects.get(name=chosen_course_name)
                # check if the student has registered this course before
                try:
                    if profile.registered_courses.get(name=chosen_course.name):
                        course_was_chosen=True
                        return  render(request,'InfoUPEI/register_course.html',{'course_was_chosen':course_was_chosen,'chosen_course_name':chosen_course.name})
                    else:
                        profile.registered_courses.add(chosen_course)
                        profile.save()
                        registered=True
                        return render(request,'InfoUPEI/register_course.html',{'registered':registered})
                except Course.DoesNotExist:
                        profile.registered_courses.add(chosen_course)
                        profile.save()
                        registered=True
                        return render(request,'InfoUPEI/register_course.html',{'registered':registered})
        else:
            register_form=RegisterCourseForm()
            return render(request,'InfoUPEI/register_course.html',{'form':register_form})

    else:
            messages.add_message(request, messages.WARNING, 'Please use your student account to login first')
            return HttpResponseRedirect("/InfoUpei/")


def error_page(request):
    return render(request,'InfoUPEI/error_page.html')


def course_detail(request,coursename):
    course=Course.objects.get(name=coursename)

    return render(request,'InfoUPEI/course_detail.html',{'course':course})


def user_detail(request,username):
    user=User.objects.get(username=username)
    user_profile=UserProfile.objects.get(user=user)

    return render(request,'InfoUPEI/user_detail.html',{'user':user,'user_profile':user_profile})
