from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import search_projects

# Create your views here.

def profiles(request):
    profiles, search_query = search_projects(request)
    context = {"profiles": profiles, "search_query": search_query}
    return render(request, "users/profiles.html", context)

def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")
    context = {"profile": profile, "top_skills": top_skills, "other_skills": other_skills}
    return render(request, "users/user_profile.html", context)

@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile': profile, "skills": skills, "projects":projects}
    return render(request, "users/account.html", context)

@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, "users/profile_form.html", context)

def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successifully")
            return redirect(request.GET["next"] if "next" in request.GET else "account")
        messages.error(request, "Username or password is incorrect")
    return render(request, "users/login_register.html")

def logout_user(request):
    logout(request)
    messages.info(request, "User was logged out")
    return redirect('login')

def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created!")
            login(request, user)
            return redirect('edit_account')
        messages.error(request, "An error has occurred during registration!")


    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)

@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False) 
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill created correcty!")           
            return redirect('account')
    context = {'form': form}
    return render(request, "users/skill_form.html", context)

@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)    
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated correcty!")
            return redirect('account')
    context = {'form': form}
    return render(request, "users/skill_form.html", context)

@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill deleted correcty!")
        return redirect('account')
    context = {'object': skill}
    return render(request, "delete_template.html", context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    message_requests = profile.messages.all()
    unread_count = message_requests.filter(is_read=False).count()
    context = {"message_requests": message_requests, "unread_count": unread_count}
    return render(request, "users/inbox.html", context)

@login_required(login_url='login')
def view_message(request, pk):
    profile = request.user.profile
    message_data = profile.messages.get(id=pk)
    if not message_data.is_read:
        message_data.is_read = True
        message_data.save()
    context = {"message_data": message_data}
    return render(request, "users/message.html", context)

def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    
    try:
        sender = request.user.profile
    except:
        sender = None
    
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient     
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, "Message sent successfully!")
            return redirect("user_profile", pk=recipient.id)

    context = {"recipient": recipient, "form": form}
    return render(request, "users/message_form.html", context)