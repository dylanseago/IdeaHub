

def glyphicon(icon_name):
    return '<span class="glyphicon glyphicon-{}" aria-hidden="true"></span>'.format(icon_name)


def field_max_len(model, field):
    return model._meta.get_field(field).max_length
