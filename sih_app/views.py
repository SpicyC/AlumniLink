import random
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from django.views.generic.base import View
from django.core import mail
from .models import Alumni, College, Course, Notices, Events
from email.message import EmailMessage
import smtplib, ssl


# Create your views here.
class InitialView(View):
    template_name = 'landing.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('username')
        try:
            alumni = Alumni.objects.get(email=email)
            return redirect(reverse('signup', kwargs={'email': email}))
        except Alumni.DoesNotExist:
            mail.send_mail('Alumni_Link', 'Please dont make a fake account', settings.EMAIL_HOST_USER, [email],
                           fail_silently=True)
            return render(request, self.template_name)


class Signup(View):
    model = Alumni
    template_name = 'signup.html'

    def get(self, request, email):
        alumni = Alumni.objects.get(email=email)
        college = College.objects.get(id=alumni.college.id)
        otp = random.randint(900000, 999999)
        mail.send_mail('Alumni-Link', 'Your OTP is: ' + str(otp), settings.EMAIL_HOST_USER,
                       [
                           'newalkarpranjal2410@gmail.com',
                           email,
                       ], fail_silently=False)
        return render(request, self.template_name, {'profile': alumni, 'college': college, 'otp': otp})

    def post(self, request, email):
        try:
            email = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.get(username=email)
            otp = request.POST.get('otp')
            print(otp)
            otp1 = request.POST.get('otp1')
            print(otp1)
            if user is not None:
                try:
                    if otp == otp1:
                        alumni = Alumni.objects.get(email=email)
                        college = College.objects.get(id=alumni.college.id)
                        auth.login(request, alumni.user)
                        return redirect(reverse('home'))
                    else:
                        return redirect(reverse('signup', kwargs={'email': email}))
                except Alumni.DoesNotExist:
                    return render(request, self.template_name, {'msg': 'No user in our college'})

        except User.DoesNotExist:
            email = request.POST.get('username')
            password = request.POST.get('password')
            otp = request.POST.get('otp')
            otp1 = request.POST.get('otp1')
            if otp1 == otp:
                user = User.objects.create_user(username=email, password=password)
                auth.login(request, user)
                return redirect(reverse('home'))
            else:
                return redirect(reverse('signup', kwargs={'email': email}))


class Signin(View):
    template_name = 'signin.html'
    model = Alumni

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            email = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.get(email=email)
            if user:
                if authenticate(request, username=email, password=password):
                    auth.login(request, user)
                    alumni = Alumni.objects.get(user=user)
                    mail.send_mail('Alumni-Link', 'You have been logged in successfully', settings.EMAIL_HOST_USER,
                                   [])
                    return redirect(reverse('home'))
                else:
                    return render(request, self.template_name, {'msg': 'Password is incorrect'})

            else:
                return render(request, self.template_name, {'msg': 'User does not exists'})
        except User.DoesNotExist:
            return render(request, self.template_name, {'msg': 'User does not exists'})


class Home(View):
    template_name = 'AltHome.html'
    model = Alumni

    def get(self, request):
        profile = Alumni.objects.get(user=request.user)
        list1 = Notices.objects.all()
        list2 = Events.objects.all()
        users = Alumni.objects.all()
        return render(request, self.template_name, {'profile': profile, 'users': users, 'News': list1,
                                                    'event': list2})


class Profile(View):
    model = Alumni
    template_name = 'profile.html'

    def get(self, request):
        profile = Alumni.objects.get(user=request.user)
        return render(request, self.template_name, {'profile': profile, 'val': 1})


class Logout(View):

    def get(self, request):
        auth.logout(request)
        return redirect(reverse('land'))


class Search(View):
    model = Alumni
    template_name = 'profile.html'

    def post(self, request):
        list1 = []
        profile = Alumni.objects.get(user=request.user)
        search = request.POST.get('search')
        db = Alumni.objects.all()
        for i in db:
            if search == i.f_name + ' ' + i.l_name:
                list1.append(i)
        if len(list1) == 1:
            profile1 = list1[0]
            return render(request, self.template_name, {'profile1': profile1, 'profile': profile, 'val': 0})


class C_DLS(ListView):
    template_name = 'C-DLS.html'
    model = Alumni

    def post(self, request):
        list1 = []
        alumni = Alumni.objects.get(user=request.user)
        if 'DLS' in request.POST:
            college = request.POST.get('college')
            course = request.POST.get('cmbcourse')
            syear = request.POST.get('syear')
            eyear = request.POST.get('eyear')
            db = Alumni.objects.all()

            if college and course and syear and eyear:
                list1 = Alumni.objects.filter(college_id=college, start_year=syear, end_year=eyear, course_id=course)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif college and course and syear:
                list1 = Alumni.objects.filter(college_id=college, start_year=syear, course_id=course)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif college and course:
                list1 = Alumni.objects.filter(college_id=college, course_id=course)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif college and syear:
                list1 = Alumni.objects.filter(start_year=syear, end_year=eyear, college_id=college)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif college and eyear:
                list1 = Alumni.objects.filter(start_year=syear, end_year=eyear, college_id=college)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif college:
                list1 = Alumni.objects.filter(college_id=college)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif syear and college and eyear:
                list1 = Alumni.objects.filter(college_id=college, start_year=syear, end_year=eyear)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif course and syear and eyear:
                list1 = Alumni.objects.filter(start_year=syear, end_year=eyear, course_id=course)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif course and syear:
                list1 = Alumni.objects.filter(start_year=syear, end_year=eyear, course_id=course)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif course:
                list1 = Alumni.objects.filter(course_id=course)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif course and eyear:
                list1 = Alumni.objects.filter(end_year=eyear, course_id=course)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif syear and eyear:
                list1 = Alumni.objects.filter(start_year=syear, end_year=eyear)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif syear:
                list1 = Alumni.objects.filter(start_year=syear)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif eyear:
                list1 = Alumni.objects.filter(end_year=eyear)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            else:
                return render(request, 'AltHome.html', {'profile': alumni})
        else:
            course = request.POST.get('cmbcourse')
            syear = request.POST.get('syear')
            eyear = request.POST.get('eyear')
            if course and syear and eyear:
                list1 = Alumni.objects.filter(start_year=syear, end_year=eyear, course_id=course)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif course and syear:
                list1 = Alumni.objects.filter(start_year=syear, course_id=course)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif course:
                list1 = Alumni.objects.filter(course_id=course)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif course and eyear:
                list1 = Alumni.objects.filter(end_year=eyear, course_id=course)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif syear and eyear:
                list1 = Alumni.objects.filter(start_year=syear, end_year=eyear)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif syear:
                list1 = Alumni.objects.filter(start_year=syear)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            elif eyear:
                list1 = Alumni.objects.filter(end_year=eyear)
                return render(request, 'C-DLS.html', {'alumni': list1, 'profile': alumni})
            else:
                return render(request, 'AltHome.html', {'profile': alumni})


def send_data(request):
    name = request.GET.get('search')
    data = {
        'profile': Alumni.objects.filter(name_icontains=name)
    }
    return JsonResponse(data)


class UpdateProfile(View):
    template_name = 'profile.html'
    model = Alumni

    def post(self, request):
        alumni = Alumni.objects.get(user=request.user)
        name = request.POST.get('name')
        name = name.split(' ')
        alumni.f_name = name[0]
        alumni.l_name = name[1]
        alumni.birth_date = request.POST.get('birth')
        alumni.email = request.POST.get('email')
        alumni.ph_no = request.POST.get('countryCode') + request.POST.get('phno')
        alumni.dp = request.POST.get('dp')
        alumni.bio = request.POST.get('bio')
        alumni.save()
        return redirect(reverse('profile'))


def news(request):
    title = request.POST.get('title')
    des = request.POST.get('des')
    pic = request.POST.get('pic')
    list1 = []
    for i in Alumni.objects.all():
        list1.append(i.email)
    mail.send_mail('New Event', title, settings.EMAIL_HOST_USER, list1)
    notice = Notices(notice=title, description=des, pic=pic)
    notice.save()
    return redirect(reverse('home'))


def events(request):
    title = request.POST.get('title')
    datef = request.POST.get('usr_dates')
    datet = request.POST.get('usr_datee')
    t1 = request.POST.get('usr_times')
    t2 = request.POST.get('usr_timee')
    pic = request.POST.get('pic')
    list1 = []
    for i in Alumni.objects.all():
        list1.append(i.email)
    mail.send_mail('New Event', title, settings.EMAIL_HOST_USER, list1)
    event = Events(title=title, date_from=datef, date_to=datet, t1=t1, t2=t2, pic=pic)
    event.save()
    return redirect(reverse('home'))