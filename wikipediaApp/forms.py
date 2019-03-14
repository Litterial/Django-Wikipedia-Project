from django import forms
from .models import Author,Article,Related

class AuthorForm(forms.ModelForm):
    class Meta:
        model=Author
        exclude=['make_user']
class ArticleForm(forms.ModelForm):
    class Meta:
        model=Article
        fields=['title','text','image','key_to_User']

        widgets={
            'title':forms.TextInput(attrs={'class':'titleBar'}),
            'text':forms.Textarea(attrs={'class':'wideTextarea'}),
           'key_to_User':forms.HiddenInput,
        }



class RelatedForm(forms.ModelForm):
    class Meta:
        model=Related
        fields=['title','text','image',]

