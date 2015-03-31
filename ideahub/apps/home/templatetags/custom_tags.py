from django.template import Library
import locale
from django.core.urlresolvers import reverse
from django.utils.timesince import timeuntil
from django.template.defaultfilters import title as format_title, capfirst
from ideahub.apps.home.models import Rating

locale.setlocale(locale.LC_ALL, '')
register = Library()


def get_next_param(context):
    request = context['request']
    if 'next' in request.GET:
        next_param = request.GET['next']
    else:
        next_param = request.path
    if next == reverse('login') or next == reverse('signup'):
        next_param = ''
    else:
        next_param = '?next=' + next_param
    return next_param


@register.inclusion_tag("fragments/link.html", name="link", takes_context=True)
def link_tag(context, named_url, title=None, nav=False, next='', classes='', wrapper_classes=''):
    request = context['request']
    if next == '' and named_url in ['login', 'signup']:
        if 'next' in request.GET:
            next = request.GET['next']
        else:
            next = request.path
        if next == reverse('login') or next == reverse('signup'):
            next = ''
        else:
            next = '?next=' + next

    if not title:
        title = named_url.replace('_', ' ')
        title = format_title(title) if nav else capfirst(title)

    url = reverse(named_url)
    wrapper_classes += ' active' if nav and request.path == url else ''
    return {
        'nav': nav,
        'href': url + next,
        'title': title,
        'classes': classes,
        'wrapper_classes': wrapper_classes,
    }


@register.filter("timeleft", is_safe=False)
def timeleft_filter(value, arg=None):
    """ Formats a date as the time until that date (i.e. "4 days, 6 hours left")."""
    if not value:
        return ''
    try:
        return timeuntil(value, arg) + ' left'
    except (ValueError, TypeError):
        return ''


@register.filter(name='currency', is_safe=False)
def currency_filter(value):
    """
    Filter - returns the currency format of the input number
    """
    if value is None:
        return ''
    try:
        return locale.currency(value, grouping=True)
    except ValueError:
        try:
            return "${:,.2f}".format(value)
        except ValueError:
            return ''


@register.filter(name='range')
def range_filter(value):
    """
    Filter - returns a sequence containing range made from given value

    Example:
    {% for i in 3|range %}
        {{ i }}
    {% endfor %}

    Result:
    0
    1
    2

    Example:
    {% for i in (0,10,2)|range %}
        {{ i }}
    {% endfor %}

    Result:
    0
    2
    4
    6
    8
    """
    return range(*value) if isinstance(value, tuple) else range(value)

@register.filter(name='sentences')
def sentences(value, nsentences):
    """
    Filter - returns everything in value up to the first period or line break.
    """
    if len(value) == 0:
        return value
    sentence_count = 0
    for i in range(len(value)):
        if sentence_count == nsentences:
            return value[:i]
        if value[i] in '.\n':
            sentence_count += 1
    return value


@register.inclusion_tag("home/fragments/idea_vote_button.html", name="idea_vote_button", takes_context=True)
def user_liked(context, idea, vote_type):
    request = context['request']
    rating = Rating.objects.filter(rater__id=request.user.id, idea=idea).first()
    voted = rating and ((rating.positive and vote_type == 'like') or (not rating.positive and vote_type == 'dislike'))
    return {
        'vote_type': vote_type,
        'voted': voted,
        'glyphicon_type': 'thumbs-up' if vote_type == 'like' else 'thumbs-down',
    }
