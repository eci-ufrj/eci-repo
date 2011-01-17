from django import template
from eci.resources.models import *
import urllib
register = template.Library()

@register.inclusion_tag("tags/last_resources.html")
def last_resources():
    resources = Resource.objects.all().order_by('-created')
    if len(resources) > 3:
        resources = resources[:3]
    return {'last_resources' : resources }

@register.inclusion_tag("tags/top_resources.html")
def top_resources():
    resources = Resource.objects.filter(deleted=False)
    dict = {}
    top = []
    top_resources =[]
    for r in resources:
        dict[r.id] = r.month_hits()
    i= 0
    for key, value in sorted(dict.iteritems(), key=lambda (k,v): (v,k),reverse=True):
        top.append(key)
        i+=1
        if i == 5:
            break
    for i in top:
        r = Resource.objects.get(id=i)
        top_resources.append(r)

    return {'top_resources' : top_resources }

@register.inclusion_tag("tags/top_collaborators.html")
def top_collaborators():
    collaborators = User.objects.filter(is_active=True)
    dict = {}
    top = []
    top_collaborators =[]
    for c in collaborators:
        dict[c.id] = c.resource_collaborator.all().count()
    i= 0
    for key, value in sorted(dict.iteritems(), key=lambda (k,v): (v,k),reverse=True):
        top.append(key)
        i+=1
        if i == 5:
            break
    for i in top:
        c = User.objects.get(id=i)
        top_collaborators.append(c)

    return {'top_collaborators' : top_collaborators }

@register.inclusion_tag('tags/pagination_links.html')
def pagination_links(request,paginator):
    raw_params = request.GET.copy()
    page = raw_params.get('page',1)
    p = paginator.page(page)
    try:
        del raw_params['page']
    except KeyError:
        pass
    params = urllib.urlencode(raw_params)
    return {'request':request,
            'paginator':paginator,
            'p':p,
            'params':params
            }