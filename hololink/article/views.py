from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
import hashlib
from .models import Article
from .forms import ArticleForm, ArticleChangeForm


def now():
    return timezone.localtime(timezone.now())


def sha256_hash(content):
    sha = hashlib.sha256()
    sha.update(content.encode())
    return sha.hexdigest()


def change_list(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    articles = Article.objects.filter(created_by=request.user)
    for article in articles:
        if len(article.hash) > 8:
            article.hash = f'{article.hash[:8]}...'
        if len(article.content) > 32:
            article.content = f'{article.content[:32]}...'
        if len(article.from_url) > 64:
            article.from_url = f'{article.from_url[:64]}...'
    context = {
        'articles': articles,
    }
    return render(request, 'article/change_list.html', context)


@csrf_exempt
def add(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'form': None,
        'instant_messages': {}
    }
    if not request.POST:
        form = ArticleForm()
        context['form'] = form
        context['instant_messages']['help_text'] = _('Fill in the following form to create a new article.')
    else:
        form = ArticleForm(request.POST)
        context['form'] = form
        if form.is_valid():
            Article.objects.create(
                hash=sha256_hash(form.cleaned_data.get('content')),
                name=form.cleaned_data.get('name'),
                content=form.cleaned_data.get('content'),
                from_url=form.cleaned_data.get('from_url'),
                created_by=request.user,
                created_at=now(),
            )
            messages.success(request, _('Added successfully.'))
            return change_list(request)
    return render(request, 'article/add.html', context)


def change(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'form': None,
        'instant_messages': {},
    }
    instance = get_object_or_404(Article, id=id, created_by=request.user)
    if not request.POST:
        form = ArticleChangeForm(instance=instance)
        context['form'] = form
        context['instant_messages']['help_text'] = _(
            'The following is the current setting. Please fill in the part you want to modify and then submit.')
    else:
        form = ArticleChangeForm(request.POST, instance=instance)
        context['form'] = form
        if form.is_valid():
            form.save()
            messages.success(request, _('Changed successfully.'))
            return change_list(request)
    return render(request, 'article/change.html', context)


def delete(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    instance = get_object_or_404(Article, id=id, created_by=request.user)
    if not request.POST:
        pass
    else:
        instance.delete()
        messages.success(request, _('Deleted successfully.'))
        return change_list(request)
    return render(request, 'article/delete.html')
