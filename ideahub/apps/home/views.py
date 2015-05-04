from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db.models import ForeignKey, Q
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from ideahub.apps.api.views import ideas_query, category_graph_data_json
from ideahub.apps.home.models import Idea, Category, Rating, sort_ideas
from ideahub.apps.home.forms import IdeaForm


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())


class ModelOwnershipMixin(SingleObjectMixin):
    model_owner_field = None

    def dispatch(self, request, *args, **kwargs):
        # Staff can access everything
        if not request.user.is_staff:
            # Determine the models owner field name by picking the first foreign key that references the User model
            if not self.model_owner_field:
                for f in self.model._meta.get_fields_with_model():
                    if isinstance(f[0], ForeignKey) and f[0].rel.to == User:
                        self.model_owner_field = f[0].name

            # Redirect if the user doesn't own this
            obj = self.get_object()
            if getattr(obj, self.model_owner_field) != request.user:
                return redirect(obj)
        return super(ModelOwnershipMixin, self).dispatch(request, *args, **kwargs)


def index(request):
    return render(request, 'home/index.html', {
        'ideas': Idea.objects.all(),
        'graph_data': category_graph_data_json(),
    })


class IdeaDetail(DetailView):
    queryset = Idea.objects.all()
    template_name = 'home/idea.html'


class IdeaCreate(LoginRequiredMixin, CreateView):
    model = Idea
    form_class = IdeaForm
    template_name = 'home/idea_create.html'

    def form_valid(self, form):
        # Set the poster before the form is saved
        form.instance.creator = self.request.user
        return super(IdeaCreate, self).form_valid(form)


class IdeaUpdate(LoginRequiredMixin, ModelOwnershipMixin, UpdateView):
    model = Idea
    form_class = IdeaForm
    template_name = 'home/idea_update.html'
    model_owner_field = 'creator'


class IdeaDelete(LoginRequiredMixin, ModelOwnershipMixin, DeleteView):
    model = Idea
    success_url = reverse_lazy('profile')
    model_owner_field = 'creator'


@login_required(login_url='get_started')
@require_POST
def idea_rate(request, pk):
    rating = request.POST.get('rating')
    if not (rating and rating in ['-1', '0', '1']):
        return HttpResponseBadRequest('rating parameter is required and must be -1, 0, or 1')
    # Remove any previous ratings
    Rating.objects.filter(idea__pk=pk, rater=request.user).delete()
    if rating != '0':
        # Add new rating if the user isn't trying to remove their current rating
        Rating(idea=get_object_or_404(Idea, pk=pk), rater=request.user, positive=(rating == '1')).save()
    return HttpResponse('')


def ideas(request):
    query = request.GET.get('query')
    selected_categories = request.GET.getlist('category', [])
    filtered_ideas = ideas_query(search_query=query, category_filters=selected_categories)
    categories = Category.objects.order_by('name')
    for category in categories:
        category.selected = str(category.id) in selected_categories
    return render(request, 'home/ideas.html', {
        'ideas': sort_ideas(filtered_ideas),
        'categories': categories,
        'query': query,
    })


def idea_cards(request):
    ideas = ideas_query()