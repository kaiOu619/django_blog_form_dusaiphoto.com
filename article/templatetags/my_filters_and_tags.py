from django import template
from django.utils import timezone
import math
register = template.Library()

@register.filter(name='transfer')
def transfer(value, arg):
    return arg

@register.filter()
def lower(value):
    return value.lower()

@register.filter()
def time_since_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        return '刚刚'
    if diff.days == 0 and diff.seconds >= 60 and diff.seconds <3600:
        return str(math.floor(diff.seconds /60)) + '分钟前'
    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        return str(math.floor(diff.seconds / 3600)) + "小时前"

    if diff.days >= 1 and diff.days < 30:
        return str(diff.days) + "天前"

    if diff.days >= 30 and diff.days < 365:
        return str(math.floor(diff.days / 30)) + "个月前"

    if diff.days >= 365:
        return str(math.floor(diff.days / 365)) + "年前"

@register.inclusion_tag('article/tag_list.html')
def show_comments_pub_time(article):
    """显示文章评论的发布时间"""
    comments = article.comments.all()
    return {'comments': comments}