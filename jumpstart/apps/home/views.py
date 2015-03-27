from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from jumpstart.apps.home.models import Idea
from django.http import HttpResponseRedirect


def index(request):
    return render(request, 'home/index.html', {
        'ideas': Idea.objects.all(),
    })


def about(request):
    return render(request, 'home/about.html')


def user(request, user_id):
    return render(request, 'home/user.html', {
        'user_profile': get_object_or_404(User, pk=user_id),
    })


@login_required
def post_idea(request):
    #TODO
    return HttpResponseRedirect('/')


def ideas(request):
    return render(request, 'home/ideas.html', {
        'ideas': Idea.objects.all()
    })


def idea(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    """
    user_contribution = None
    if request.method == 'POST':
        form = FundingForm(request.user, project, request.POST)
        if form.is_valid():
            funding = form.save()
            user_contribution = funding.amount
    else:
        form = FundingForm(request.user, project)
        fundings = project.fundings.filter(user__id=request.user.id)
        if len(fundings) != 0:
            user_contribution = fundings[0].amount
            """
    return render(request, 'home/idea.html', {
        'idea': idea,
    })