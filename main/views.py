from django.http.response import FileResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import *

from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth.forms import AuthenticationForm

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound


from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def render_pdf(request, name):
    project = Project.objects.get(project_title=name)
    return render(request, "main/render_pdf.html", context={"project":project})


# Create your views here.
context = {'home':['Home', 'homepage'], 'login':['Login', 'login'], 'signup':['Sign Up', 'signup']}

def context_generator(*args, context):
    result = [context[each] for each in args]
    return result

def homepage(request):
    cont={'name':context_generator('home', 'login', 'signup', context=context), 'title': ''}
    return render(request=request, template_name='main/homepage.html', 
    context=cont)

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect ('homepage')

    form = AuthenticationForm()
    cont = {'form':form, 'name':context_generator('login', 'home', 'signup', context=context), 'title': ''}
    return render(request=request, template_name='main/login.html', context=cont)

@login_required
def forms(request):
    try:
        StudentProfile.objects.get(user = request.user)
        return redirect('homepage')
    except:
        
        if request.method == "POST":
            form = StudentForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                if (form.instance.year.year == 4) and (form.instance.department == "Electrical Engineering"):
                    return redirect("stream_form")
                return redirect('homepage')
        else:
            form = StudentForm()

        cont={'form':form, 'name':context_generator('login', 'home', 'signup', context=context), 'title': ''}
        return render(request=request, template_name='user/forms.html', context=cont)

def stream_form(request):
    if request.method == "POST":
        form = StudentForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')

    cont={'form':StreamForm()}
    return render(request=request, template_name='user/stream_form.html', context=cont)
    


        

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        cont={'form':form, 'title': '',  'name':context_generator('signup', 'home', 'login', context=context)}
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created {username}")
            login(request, user)
            return redirect('forms')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form = SignUpForm()
        cont = {'form':form, 'title': '', 'name':context_generator('signup', 'home', 'login', context=context)}
    return render(request=request, template_name='main/signup.html',context=cont)



def signout(request):
    logout(request)
    return redirect ('homepage')

@login_required
def account(request, name):
    user = StudentProfile.objects.get(user=request.user)
    cont = {'title': 'department', 'student':user, 'name':context_generator('home', 'login', 'signup', context=context),'department':False}
    return render(request=request, template_name='user/account.html', context=cont)


def department(request):
    faculty = Department.objects.all()
    cont = {'title': 'department', 'name':context_generator('home', 'login', 'signup', context=context), 'faculties':faculty}
    return render(request=request, template_name='main/department.html', context=cont)
    

def dep_display(request, name):
    year = SchoolYear.objects.all()
    cont = { 'title': 'department', 'dep_name':name,
        'name':context_generator('home', 'login', 'signup', context=context), 
        'school_year':year,  'department':False }
    return render(request=request, template_name='main/year.html', context=cont)
  


def school_year(request, name, number):
    projects = Project.objects.all()
    project = []
    for each in projects:
        if (each.author.year.name == number and each.author.department.name == name):
            project.append(each) 
    cont = {'title': 'department','dep_name':name, 'year':number,
    'name':context_generator('home', 'login', 'signup', context=context), 
    "projects":project,  'department':False}
    return render(request=request, template_name='main/projects.html', context=cont)
    



@login_required
def add_project(request, name):
    
    if request.method == "POST":
        form = ProjectForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.author = StudentProfile.objects.get(user=request.user)
            form.save()
            return redirect('homepage')
    else:
        form = ProjectForm()

    cont={'form':form, 'name':context_generator('login', 'home', 'signup', context=context), 'title': ''}
    return render(request=request, template_name='user/forms.html', context=cont)
    

def profile_settings(request):
    form = ProfileForm(instance=request.user)
    context = {'form':form}
    return render(request, 'profile.html', context)