from crispy_forms.bootstrap import AppendedText, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from ideahub import settings
from ideahub.utils import glyphicon, field_max_len


class LoginForm(AuthenticationForm):
    """
    A form that logs a user in
    """
    remember_me = forms.BooleanField(
        label = 'Remember Me',
        required = False,
        widget = forms.CheckboxInput
    )

    def remember_user(self):
        try:
            if self.cleaned_data.get('remember_me'):
                return True
        except AttributeError:
            pass
        return False

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'login'
        self.helper.label_class = 'sr-only'
        self.helper.layout = Layout(
            PrependedText('username', glyphicon('user'), placeholder='Username'),
            PrependedText('password', glyphicon('lock'), placeholder='Password'),
            Field('remember_me', css_class='checkbox-inline'),
            Submit('submit', 'Login'),
        )


class SignupForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username, email,
    password, first name and last name.
    """
    first_name = forms.CharField(
        label = 'First Name',
        max_length = field_max_len(User, 'first_name'),
        required = True,
        widget = forms.TextInput,
    )

    last_name = forms.CharField(
        label = 'Last Name',
        max_length = field_max_len(User, 'last_name'),
        required = True,
        widget = forms.TextInput,
    )

    email = forms.EmailField(
        label = 'Email',
        max_length = field_max_len(User, 'email'),
        required = True,
        widget = forms.EmailInput,
    )

    username = forms.RegexField(
        label = "Username",
        max_length = field_max_len(User, 'username'),
        required = True,
        regex = r'^[\w.@+-]+$',
        help_text = "{} characters or fewer. Letters, digits and @/./+/-/_ only.".format(field_max_len(User, 'username')),
        error_messages = {
            'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters.",
        },
    )

    password1 = forms.CharField(
        label = "Password",
        min_length = 8,
        required = True,
        widget = forms.PasswordInput,
        help_text = "8 characters minimum.",
    )

    password2 = forms.CharField(
        label = "Repeat Password",
        required = True,
        widget = forms.PasswordInput,
        help_text = "Enter the same password as above, for verification.",
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def save(self, commit=True, auth_after_save=True):
        user = super(SignupForm, self).save(commit)
        if commit and auth_after_save:
            user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password1'])
        return user

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = 'signup'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.layout = Layout(
            Field('first_name', placeholder='First Name'),
            Field('last_name', placeholder='Last Name'),
            Field('email', placeholder='Email'),
            Field('username', placeholder='Username'),
            Field('password1', placeholder='Password'),
            Field('password2', placeholder='Repeat Password'),
            Submit('submit', 'Sign Up'),
        )