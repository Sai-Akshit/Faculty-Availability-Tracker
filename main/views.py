from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

import os
import mimetypes

from .decorators import unauthenticated_user, allowed_users
from .algorithm import dataExtraction, defineTime, timeIndex, searchingFree, searchingBusy, download, course_and_champions_input
from .models import faculty_details, courseChampions, faculty_details_even, courseChampions_even

# creating a temporary dictionary named 'data' to store eligible employees, that can be used in download file function
tempDict = {}

# Create your views here.
@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Please check the entered username and password')
            return redirect('/')
        
    return render(request, 'main/login.html')

def password_reset(request):
    return HttpResponse('<h1 style="text-align: center">Currently under development</h1><h3 style="text-align: center"><a href="/login/">Click Here</a> to go back to login page.</h3>')

def logout(request):
    auth.logout(request)
    return redirect('/login')

@login_required(login_url='/login')
@allowed_users(allowed_roles=['Admin'])
def register_user(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email_id']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']
        group_type = request.POST['group_type']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                context['type'] = 'error'
                messages.info(request, 'User already exists with same username')
            elif User.objects.filter(email=email).exists():
                context['type'] = 'error'
                messages.info(request, 'Email already taken')
            else:
                context['type'] = None
                user = User.objects.create_user(username=username, password=password1, email=email)
                group = Group.objects.get(name=group_type)
                user.groups.add(group)
                user.save()
                messages.info(request, 'User created successfullly of user type ' + group_type)
        else:
            context['type'] = 'error'
            messages.info(request, "Password do not match")

    return render(request, 'main/register_user.html', context)
    # return render(request, 'main/register_user.html')

@login_required(login_url='/login')
def home(request):
    numbers = range(8, 17)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    dayIndex = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4}
    context = {'numbers': numbers, 'days': days}

    if request.method == 'POST':
        context['sem'] = request.POST['sem'].title() + " Sem" 
        try:
            reqDayIndex = dayIndex[request.POST['requested_day']]
        except:
            messages.info(request, 'Please select a day')
            return render(request, 'main/home.html', context)

        if 'day_sort' in request.POST.keys():
            if request.POST['day_sort'] == 'morning':
                reqTime = timeIndex([i for i in range(8, 14)])
                timeTemp = timeIndex([i for i in range(8, 14)])
            elif request.POST['day_sort'] == 'evening':
                reqTime = timeIndex([i for i in range(13, 17)])
                timeTemp = timeIndex([i for i in range(13, 17)])
            else:
                reqTime = timeIndex([i for i in range(8, 17)])
                timeTemp = timeIndex([i for i in range(8, 17)])
            try:
                context['time'] = f'{timeTemp[0]+8}:00 - {timeTemp[-1]+8}:50'
            except IndexError:
                messages.info(request, 'Select a time to search')
                return render(request, 'main/home.html', context)
        else:
            reqTime = timeIndex(defineTime(request.POST))
            timeTemp = defineTime(request.POST)
            try:
                context['time'] = f'{timeTemp[0]}:00 - {timeTemp[-1]}:50'
            except IndexError:
                messages.info(request, 'Select a time to search')
                return render(request, 'main/home.html', context)

        # add an if loop for odd and even sems
        if request.POST['sem'] == 'odd':
            querySet = faculty_details.objects.all()
        else:
            querySet = faculty_details_even.objects.all()
        """Need to verify above code"""
        context['day'] = request.POST['requested_day']

        try:
            if request.POST['use_case'] == 'free':
                context['eligibleEmps'] = searchingFree(querySet, reqDayIndex, reqTime)    
                global tempDict
                tempDict['data'] = context['eligibleEmps']
                context['status'] = 'Faculty who are free'
            else:
                context['eligibleEmps'] = searchingBusy(querySet, reqDayIndex, reqTime)
                tempDict
                tempDict['data'] = context['eligibleEmps']
                context['status'] = 'Faculty who are having class'
        except:
            messages.info(request, 'Please select a use case')
            return render(request, 'main/home.html', context)

    return render(request, 'main/home.html', context)

def course_champion(request):
    context = {'show': False}
    if request.method == 'POST':
        if request.POST['sem'] == 'odd':
            context['second_year'] = courseChampions.objects.filter(year=2)
            context['third_year'] = courseChampions.objects.filter(year=3)
            context['fourth_year'] = courseChampions.objects.filter(year=4)
            context['show'] = True
        else:
            context['second_year'] = courseChampions_even.objects.filter(year=2)
            context['third_year'] = courseChampions_even.objects.filter(year=3)
            context['fourth_year'] = courseChampions_even.objects.filter(year=4)
            context['show'] = True
    return render(request, 'main/course_champion.html', context)

@login_required(login_url='/login')
@allowed_users(allowed_roles=['Admin'])
def fileInput(request):
    sem = None
    if request.method == 'POST':
        if request.POST['sem'] == 'odd':
            sem = 'odd.xlsx'
        else:
            sem = 'even.xlsx'

        try:
            uploaded_file = request.FILES['document']
        except:
            messages.info(request, 'Please upload a file!')
            return render(request, 'main/fileInput.html', {})

        fs = FileSystemStorage()
        name = fs.save(sem, uploaded_file)
        path = "media/"+ str(sem)
        print(f'\n{path}\n')
        
        # 1.Updating the database
        dataExtraction(path, request.POST['sem'])    # extracting data to teacher table
        course_and_champions_input(path, request.POST['sem'])    # extracting data to course champion table

        # fs.delete(uploaded_file.name)
        # fs.delete(name)
        file_path = os.getcwd() + f'/media/{sem}'
        os.remove(file_path)
        
        return HttpResponseRedirect('/')

    return render(request, 'main/fileInput.html', {})

@login_required(login_url='/login')
def individual_tables(request):
    context = {}

    if request.method == 'POST':
        print(f'\n{request.POST}\n')
        if 'emp_id' in request.POST:
            print(request.POST['emp_id'], type(request.POST['emp_id']))

    return render(request, 'main/search.html', context)

def download_file(request):
    """Function that creates a csv file"""
    global tempDict
    try:
        download(tempDict['data'])
    except KeyError:
        messages.info(request, 'Retry searching for data')
    tempDict['data'] = None

    """Django handling"""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'data.csv'
    filepath = BASE_DIR + '/media/download/' + filename
    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
