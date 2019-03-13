from django import forms
from .models import Author,Article,Related

class AuthorForm(forms.ModelForm):
    class Meta:
        model=Author
        exclude=['make_user']
class ArticleForm(forms.ModelForm):
    class Meta:
        model=Article
        fields=['title','text','image','last_update']
        widgets={
            'last_update':forms.HiddenInput(),
        }
class RelatedForm(forms.ModelForm):
    class Meta:
        model=Related
        exclude=['date_created','last_updated']
