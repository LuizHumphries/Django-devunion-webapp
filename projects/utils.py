from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project, Tag

def search_projects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    tags = Tag.objects.filter(name__icontains=search_query)    
    
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) | 
        Q(owner__name__icontains=search_query) | 
        Q(tags__in=tags)
        )
    
    return projects, search_query

def paginate(request, projects, results):
    page = request.GET.get("page", 1)    
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    left_index = (int(page) - 4)
    if left_index <= 0:
        left_index = 1
    right_index = (int(page) + 5)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1


    custom_pagination = range(left_index, right_index)
    
    return projects, custom_pagination