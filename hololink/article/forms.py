from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['name', 'content', 'from_url', ]


class ArticleChangeForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['name']
