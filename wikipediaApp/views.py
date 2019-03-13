from django.shortcuts import render,redirect,get_object_or_404
from .forms import Author,AuthorForm,Article,ArticleForm,Related,RelatedForm
from django.utils import timezone
from django.contrib.auth.models import User
# Create your views here.
def index(request):  #landing page
    return render(request,'wikipediaApp/index.html')

def createAuthor(request): #create an author
    form=AuthorForm(request.POST or None) #submits blank form for get request, filled form for post request
    if request.method =='POST': #if post request
        if form.is_valid(): #if form is valid
            User.objects.create_user(username=request.POST['username'],password=request.POST['password']) #create user
            form.save()#saves info in models
            return redirect('congrats') #redirects user to a confirmation page
        else:
            form=AuthorForm(request.POST) #sends posted information back to form
            context={
                'form':form,
                'errors':form.errors
            }
            return render(request,'wikipediaApp/createAuthor.html',context) #renders content on template with errors

    return render(request,'wikipediaApp/createAuthor.html',{'form':form})

def congrats(request):
    return render(request,'wikipediaApp/congrats.html')


def readArticle(request,ID): #read individual articles
    return render(request,'wikipediaApp/readArticle.html')

def createArticle(request): #creates new page, will create an id once created
    allArticles=Article.objects.all()
    print(allArticles)
    return render(request,'wikipediaApp/createArticle.html',{'allArticles':allArticles})

def editArticle(request,ID): #edits page,needs id of instance
    ID=1
    return render(request,'wikipediaApp/editArticle.html',{'ID':ID})

def deleteArticle(request,ID): #deletes needs id of instace
    ID=1
    return render(request,'wikipediaApp/deleteArticle.html',{'ID':ID})

def readRelated(request,ID): #reads related needs id of parent
    ID=1
    return render(request,'wikipediaApp/readRelated.html',{'ID':ID})

def createRelated(request,ID): #creates related needs id of parent
    ID=1
    return render(request,'wikipediaApp/createRelated.html',{'ID':ID})

def editRelated(request,ID): #edits related needs id of parent
    ID=1
    return render(request,'wikipediaApp/editRelated.html',{'ID':ID})

def deleteRelated(request,ID): #deletes related neeeds id of parent
    ID=1
    return render(request,'wikipediaApp/deleteRelated.html',{'ID':ID})