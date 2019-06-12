from django import forms
from .models import Author,Article,Related

class AuthorForm(forms.ModelForm):
    class Meta:
        model=Author
        exclude=['make_user']
        widgets={
            'password':forms.PasswordInput(),
        }

    def clean_username(self):
        userData=self.cleaned_data['username']
        print(userData)
        if Author.objects.filter(username=userData).exists():
            print("error")
            raise forms.ValidationError("This user already exist")
        return userData



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
        fields=['title','text','image','key_to_Article']

        widgets={
            'title':forms.TextInput(attrs={'class':'titleBar'}),
            'text':forms.Textarea(attrs={'class':'wideTextarea'}),
            'key_to_Article':forms.HiddenInput,
        }

