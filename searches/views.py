from django.shortcuts import render, redirect
from application.models import Expert
from .models import SearchQuery
from application.filters import ExpertFilter

def search_view(request):
    query = request.GET.get('q', None)
    place = request.GET.get('p', None)

    if query is None and place is None:
        return redirect('home')

    user = None

    context = {"query": query, "place": place}

    if request.user.is_authenticated:
        user = request.user
    
    #save search for analytics purpose
    SearchQuery.objects.create(user=user, query=query, place=place) 
    # experts
    experts = Expert.objects.search(query=query, place=place)
    # custom_filter
    custom_filter = ExpertFilter(request.GET, queryset=experts)
    # experts filtered
    experts = custom_filter.qs

    context['experts'] = experts
    context['total_experts'] = experts.count()
    context['custom_filter'] = custom_filter

    return render(request, 'search.html', context)