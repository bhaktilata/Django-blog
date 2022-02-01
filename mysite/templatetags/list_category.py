from django import template
from mysite.models import Category
from django.db.models import Count, F

register = template.Library()

@register.simple_tag(name='list-categories')
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('mysite/list_categories.html')
def show_categories():
    #categories = Category.objects.all()
    categories = Category.objects.annotate(cnt=Count('post', filter=F('post__is_published'))).filter(cnt__gt=0)
    return {"categories": categories}

