from crispy_forms.bootstrap import FormActions
from django import forms
from jumpstart.apps.home.models import Idea, Rating
from crispy_forms.helper import FormHelper
from django.core.urlresolvers import reverse
from crispy_forms.layout import Submit, Layout, Field, Div, Button, HTML
from jumpstart.utils import field_max_len


class IdeaForm(forms.ModelForm):
    """
    A form that creates a new idea.
    """
    name = forms.CharField(
        label = 'Name',
        max_length = field_max_len(Idea, 'name'),
        required = True,
        widget = forms.TextInput(),
    )

    tags = forms.CharField(
        label = 'Tags',
        max_length = field_max_len(Idea, 'tags'),
        required = False,
        widget = forms.TextInput(),
    )

    description = forms.CharField(
        label = 'Description',
        max_length = field_max_len(Idea, 'description'),
        required = True,
        widget = forms.Textarea(attrs = {
            'rows': 5,
        }),
    )

    class Meta:
        model = Idea
        fields = ['category', 'name', 'description', 'tags']

    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.layout = Layout(
            Field('name', placeholder='Name'),
            Field('category'),
            Field('tags', placeholder='Comma or space separated list of tags'),
            Field('description',
                  placeholder='Description of your idea (max {} characters)'.format(field_max_len(Idea, 'description')))
        )