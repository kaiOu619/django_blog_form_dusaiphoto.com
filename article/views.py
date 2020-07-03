from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from django.views import View

from .models import ArticlePost, ArticleColumn
from .forms import ArticlePostFrom
import markdown

from comment.models import Comment

from comment.forms import CommentForm


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    article_list = ArticlePost.objects.all()
    if search:
        if order == 'total_views':
            articles_list = ArticlePost.obhects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            articles_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ''
        if request.GET.get('order') == 'total_views':
            articles_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            articles_list = ArticlePost.objects.all()
    if column is not None and column.isdigit():
        articles_list = articles_list.filter(column=column)
    if tag and tag != 'None':
        articles_list = articles_list.filter(tags__name__in=[tag])
    if order == 'total_views':
        articles_list = articles_list.order_by('-total_views')

    paginator = Paginator(articles_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    }
    return render(request, 'article/list.html', context)

def article_detail(request, id):
    # article = ArticlePost.objects.get(id=id)
    article = get_object_or_404(ArticlePost, id=id)
    comments = Comment.objects.filter(article=id)
    article.total_views += 1
    article.save(update_fields=['total_views'])
    md = markdown.Markdown(
                    extensions=[
                        'markdown.extensions.extra',
                        'markdown.extensions.codehilite',
                        'markdown.extensions.toc',
                    ])
    article.body = md.convert(article.body)
    comment_form = CommentForm()
    context = {'article': article, 'toc': md.toc, 'comments':comments, 'comment_form': comment_form}
    return render(request, 'article/detail.html', context)
@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostFrom(request.POST, request.FILES)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()
            article_post_form.save_m2m()
            return redirect('article:article_list')
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    else:
        article_post_form = ArticlePostFrom
        columns = ArticleColumn.objects.all()
        context = {'article_post_form': article_post_form, 'columns': columns}
        return render(request, 'article/create.html', context)
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('仅允许post请求。')

@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉呢，您无权修改这篇文章！")
    if request.method == 'POST':
        article_post_form = ArticlePostFrom(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse('表单内容有误，请重新填写！')
    else:
        article_post_form = ArticlePostFrom()
        context = {'article': article,
                   'article_post_form': article_post_form,
                   'tags': ','.join([x for x in article.tags.names()]),
                   }
        return render(request, 'article/update.html', context)
# 点赞数 +1
class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')