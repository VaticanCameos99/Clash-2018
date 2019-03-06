from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, render_to_response
# built in django registration form
from accounts.forms import RegistrationFrom
from django.views.generic import DetailView, TemplateView
from accounts.models import MCQ, UserProfile, Question_list
import random
import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.template import RequestContext


@login_required()
def home(request):  # for logging in
    if request.method == "GET":
        return HttpResponseRedirect("/accounts/rules")
    else:
        return render(request, 'accounts/home.html')


@login_required()
def timer(request):
    if request.method == 'POST':
        currentuser = request.user.id
        data = UserProfile.objects.get(user_id=currentuser)
        login_time = datetime.datetime.now()
        login_time_sec = ((login_time.hour) * 60 * 60) + ((login_time.minute) * 60) + (login_time.second)
        data.timer = login_time_sec
        data.save()
        return display(request)
    else:
        return loggedout(request)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email_1 = request.POST['email_1']
        email_2 = request.POST['email_2']
        name_1 = request.POST['name_1']
        name_2 = request.POST['name_2']
        number_1 = request.POST['num_1']
        number_2 = request.POST['num_2']

        # for validation of the user

        def validate():
            if username and password and email_1 and name_1 and number_1:
                pass
            else:
                return 1

            if User.objects.filter(username=username).exists():
                return 2

        if validate() == 1:
            return render_to_response('reg_form.html', {"error": "Some fields are empty !!!"})
        if validate() == 2:
            return render_to_response('reg_form.html', {"error": "Username already exists !!!"})

	#creating new user using inbuilt Functions
        user = User.objects.create(username=username, password=password)
        user.set_password(password)
        user.save()	#User is added -> instance is created -> go to kwargs
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                datas = UserProfile.objects.filter(user_id=request.user.id)
                for data in datas:
                    year = request.POST['level']
                    data.year = year
                    data.save()
                    if int(data.year) == 1:
                        data.level = 0
                        data.save()
                    else:
                        data.level = 1
                        data.save()
                    data.email_1 = request.POST['email_1']
                    if request.POST['email_2']:
                        data.email_2 = request.POST['email_2']
                    data.name_1 = request.POST['name_1']
                    if request.POST['name_2']:
                        data.name_2 = request.POST['name_2']
                    data.number_1 = request.POST['num_1']
                    if request.POST['num_2']:
                        data.number_2 = request.POST['num_2']
                    data.save()
                    return rules(request)
            else:
                return render(request, 'reg_form.html')
        else:
            return render(request, 'reg_form.html')
    else:
        return render(request, 'reg_form.html')


# for accessing rules page
@login_required()
def rules(request):
    return render(request, 'rules.html')


def addq(request):
    if request.method == "POST": #POST has to be capitalized

        user = MCQ.objects.create(
        question = str(request.POST.get('Que')),
        answer =  int(request.POST.get('Ans')),
        A = str(request.POST.get('opt1')),
        B = str(request.POST.get('opt2')),
        C = str(request.POST.get('opt3')),
        D = str(request.POST.get('opt4')),
        level =  int(request.POST.get('level')),
        )   
        user.save()
        choice = str(request.POST.get('choice')),
        print(choice[0])
        if choice[0] == "Yes":
            return render(request, 'addq.html')
        else:
            return HttpResponse('Questions Saved!')
    else:
        return render(request, 'addq.html')


# for displaying questions on the page
@login_required()
def display(request):
    if request.method == 'POST':
        print("in display")
        currentuser = request.user.id
        data = UserProfile.objects.get(user_id=currentuser)
        m = random.randint(1, 916)
        check = Question_list.objects.filter(user_id=currentuser)
        check = check.filter(question_list=m)
        if check:
            return display(request)

        else:
            login_time_sec = data.timer
            time_kill = login_time_sec + 1680 + data.add_time
            now = datetime.datetime.now()
            now_sec = ((now.hour) * 60 * 60) + ((now.minute) * 60) + (now.second)
            time = time_kill - now_sec
            if time <= 0:
                return loggedout(request)

            if data.perception_active == 1 and data.perception_question_count == 3:
                ques = Question_list.objects.filter(user_id=currentuser).last()
                show = MCQ.objects.get(id=ques.question_list)
                value = {'v': show, 'u': data, 't': time}
                return render(request, 'display.html', value)

            else:
                show = MCQ.objects.get(id = m)
                print(show.level)
                print(data.level)
                if show.level == data.level:
                    ques = Question_list.objects.create(user_id=currentuser, question_list=m, )
                    value = {'v': show, 'u': data, 't': time}
                    return render(request, 'display.html', value)
                else:
                    return display(request)
    else:
        return context(request)


# for checking the answer
@login_required()
def anscheck(request):
    if request.method == 'POST':
        currentuser = request.user.id
        data = UserProfile.objects.get(user_id=currentuser)
        check = Question_list.objects.filter(user_id=currentuser).last()
        show = MCQ.objects.get(id=check.question_list)
        n =0
        if request.POST.get('select'):
            n = request.POST.get('select')
        check.answer = n
        check.save()
        data.number_of_questions += 1
        data.save()

        if data.perception_active == 1:
            data.perception_question_count -= 1
            data.save()

        if show.answer == int(n):
            data.score += data.incr
            data.question_skip_count += 1

            data.correct_answer += 1
            n = 0
            data.save()

            if data.question_skip_count == 3:
                data.skip_count += 1
                data.question_skip_count = 0
                data.save()

            if data.perception_question_count == 0:
                data.incr = 4
                data.decr = 2
                data.perception_active = 0
                data.save()

            if data.number_of_questions == 391:
                return loggedout(request)
            else:
                return display(request)

        else:
            n = 0
            data.score -= data.decr

            data.question_skip_count = 0
            data.save()
            if data.perception_question_count == 0:
                data.incr = 4
                data.decr = 2
                data.perception_active = 0
                data.save()
            if data.number_of_questions == 391:
                return loggedout(request)
                return HttpResponse('Questions complete!!')
            else:
                return display(request)
    else:
        return loggedout(request)


def skip(request):
    if request.method == 'POST':
        print('in skip post')
        data = UserProfile.objects.get(user_id=request.user.id)
        if data.perception_active == 0 and data.skip_count >= 1:
            print(data.skip_count)
            data.skip_count -= 1
            data.number_of_questions += 1
            if data.number_of_questions == 391:
                return loggedout(request)
            data.save()
            return display(request)  # try with dislay(request)
        else:
            return context(request)
    else:
        return loggedout(request)


# logic for perception lifeline
@login_required()
def perception(request):
    if request.method == 'POST':
        print('perc post')
        data = UserProfile.objects.get(user_id=request.user.id)
        if (data.perception_present == 2 or data.perception_present == 1) and data.perception_active == 0:
            print('perc present')
            return render(request, 'accounts/perception.html')
        else:
            return context(request)
    else:
        return loggedout(request)


def context(request):
    ques = Question_list.objects.filter(user_id=request.user.id).last()
    m = ques.question_list
    show = MCQ.objects.get(id=m)
    data = UserProfile.objects.get(user_id=request.user.id)

    login_time_sec = data.timer
    #login_time_sec = ((login_time.hour) * 60 * 60) + ((login_time.minute) * 60) + (login_time.second)
    time_kill = login_time_sec + 1680 + data.add_time
    now = datetime.datetime.now()
    now_sec = ((now.hour) * 60 * 60) + ((now.minute) * 60) + (now.second)
    time = time_kill - now_sec

    value = {'v': show, 'u': data, 't': time}
    return render(request, 'display.html', value)


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)


def perception_check(request):
    if request.method == 'POST':
        data = UserProfile.objects.get(user_id=request.user.id)
        if (data.perception_present == 2 or data.perception_present == 1) and data.perception_active == 0:
            print('enter answer chek')

            data.incr = request.POST.get('select2')
            data.decr = request.POST.get('select2')
            print(data.incr)
            data.perception_active = 1
            data.perception_present -= 1
            data.perception_question_count = 3
            data.save()
            return display(request)
        else:
            return context(request)
    else:
        return loggedout(request)


#@login_required()
def loggedout(request):
    if request.user.id:
        print('logout entered')
        data = UserProfile.objects.get(user_id=request.user.id)
        score = data.score
        corrans = data.correct_answer
        numques = data.number_of_questions
        final = {'final_score': score, 'final_corr_ans': corrans, 'final_number_ques': numques}
        logout(request)
        print(score)
        return render (request, 'result.html', final)
    else:
        return render(request, 'reg_form.html')

@csrf_exempt
def logged(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        ad_pass = request.POST['ad_pass']
        if not ad_pass == "NORSians":
            return render_to_response('login.html', {"error": "Admin password required or incorrect !"})

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                data = UserProfile.objects.get(user_id=request.user.id)
                data.add_time = request.POST.get('add_time')
                data.save()
                return context(request)
            return render(request, 'login.html')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
