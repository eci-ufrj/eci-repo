from django.template import Library


register = Library()


@register.filter
def truncate(value, arg):
    if len(value) < arg:
        return value
    else:
        return value[:arg] + '..'

@register.filter(name='kbyte')
def kbyte(value):
    bytes = int(value)*1.0
    kbytes = bytes/1000.0
    return str(kbytes)+' KB'

@register.filter(name='none_value')
def none_value(value):
    if value == None:
        return 'Sem Nota'
    return value