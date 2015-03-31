from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from datetime import datetime, timedelta
from jumpstart.apps.home.models import Idea, sort_ideas, Category
from django.utils.timezone import get_current_timezone_name
import pytz
import json

JSON_DATE_FORMAT = "%d %b %Y"

def json_date(date_string):
    """
    Convert the string to a dat or None on error.
    """
    if date_string:
        try:
            unaware = datetime.strptime(date_string, JSON_DATE_FORMAT)
            return pytz.timezone(get_current_timezone_name()).localize(unaware)
        except ValueError:
            pass
    return None

def json_int(int_string):
    """
    Convert the string to an int or None on error.
    """
    if int_string:
        try:
            return int(int_string)
        except ValueError:
            pass
    return None

@require_GET
def ideas(request):
    """
    REST service for obtaining the best ideas ranked by net rating  with optional range of ranking range and date
    range. If start and end are not specified the top 5 ideas will be returned. If start_date and end_date are not
    specified then ideas will not be filtered by date at all.
    Can also be used to obtain a visual html representation of the ideas if render request param is set.
    """
    count = json_int(request.GET.get('count'))
    count = 5 if not count else count
    render_ideas = 'render' in request.GET
    idea_set = ideas_query(start_range=json_int(request.GET.get('start')),
                           end_range=json_int(request.GET.get('end')),
                           start_date=json_date(request.GET.get('start_date')),
                           end_date=json_date(request.GET.get('end_date')),
                           search_query=request.GET.get('query'),
                           category_filters=request.GET.getlist('category'),
                           count=count,)
    if render_ideas:
        return render(request, 'home/fragments/idea_cards.html', {
            'ideas': idea_set,
        })
    else:
        return JsonResponse({
            'ideas': [x.as_json() for x in idea_set],
        })


def ideas_query(search_query=None, category_filters=None,
                start_range=None, end_range=None,
                start_date=None, end_date=None,
                count=None, render=False):
    """
    Returns all ideas ordered by net rating that satisfy the specified query terms.
    """
    q = Q()
    # Add date filter to query
    if start_date:
        q &= Q(created_on__gte=start_date)
    if end_date:
        end_date += timedelta(days=1)
        q &= Q(created_on__lt=end_date)
    # Add search term to query
    if search_query:
        q &= Q(name__icontains=search_query) | Q(description__icontains=search_query) | Q(tags__icontains=search_query)
    # Add category filter to query
    if category_filters:
        q &= Q(category__pk__in=category_filters)

    # Query and sort all ideas
    idea_set = sort_ideas(Idea.objects.filter(q))

    # Correct indexes
    if not start_range or start_range < 0:
        start_range = 0
    if not end_range and count:
        end_range = start_range + count
    if not end_range or end_range > len(idea_set):
        end_range = len(idea_set)

    # Return the ideas in the specified index
    return idea_set[start_range:end_range]

@require_GET
def category_graph(request):
    return HttpResponse(category_graph_data_json(), content_type='application/json')

def category_graph_data_json():
    categories = Category.objects.annotate(idea_count=Count('ideas'))
    graph_data = []
    # Aggregate category data into a graph format
    for category in categories:
        if category.idea_count > 0:
            graph_data.append({
                'name': category.name,
                'y': category.idea_count,
            })
    return json.dumps({
        'graph_data': graph_data
    })