from django import forms
from .models import Author,Article,Related

class AuthorForm(forms.ModelForm):
    class Meta:
        model=Author
        exclude=['make_user']
class ArticleForm(forms.ModelForm):
    class Meta:
        models=Article
        exclude=['last_updated']
class RelatedForm(forms.ModelForm):
    class Meta:
        models=Related
        exclude=['last_updated']
class editArticleForm(forms.ModelForm):
    class Meta:
        model=Article
        exclude=['date_created','last_updated']

class editRelatedForm(forms.ModelForm):
    class Meta:
        models=Related
        exclude=['date_created','last_updated']