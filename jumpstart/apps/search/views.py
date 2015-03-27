from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from jumpstart.apps.home.models import Idea
from django.db.models import Q


@require_http_methods(['GET'])
def results(request):
    query = request.GET.get('q', '')
    ideas = Idea.objects.all().filter(
        Q(name__icontains=query) | Q(summary__icontains=query) | Q(about__icontains=query) | Q(tags__icontains=query))
    return render(request, 'search/results.html', {
        'ideas': ideas,
        'search_query': query
    })

