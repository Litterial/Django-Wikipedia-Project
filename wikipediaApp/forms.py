from django import forms
from .models import Author,Article,Related

class AuthorForm(forms.ModelForm):
    class Meta:
        model=Author
        exclude=['make_user']
class ArticleForm(forms.ModelForm):
    class Meta:
        model=Article
        fields=['title','text','image',]



class RelatedForm(forms.ModelForm):
    class Meta:
        model=Related
        fields=['title','text','image',]

class SearchForm (forms.Form):
    search=forms.CharField(max_length=255)
