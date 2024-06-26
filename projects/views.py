from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import search_projects, paginate

def projects(request):
    projects, search_query = search_projects(request)
    projects, custom_pagination = paginate(request, projects, 6)
    context = {"projects": projects, "search_query": search_query, "custom_pagination": custom_pagination}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()

        project_obj.get_vote_count

        messages.success(request, "Your review was successfully submitted!")
        return redirect("project", pk= project_obj.id)

    context = {'project': project_obj, "form": form}
    return render(request, 'projects/single-project.html', context)

@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == "POST":
        newtags = request.POST.get('new_tags').replace(',', ' ').split()          
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)        
            return redirect('account')
    context = {'form': form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        newtags = request.POST.get('new_tags').replace(',', ' ').split()    
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context = {'form': form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("account")
    context = {'object': project}
    return render(request, 'delete_template.html', context)