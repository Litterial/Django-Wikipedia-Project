from django.shortcuts import render,redirect,get_object_or_404
from .forms import Author,AuthorForm,Article,ArticleForm,Related,RelatedForm,editArticleForm,editRelatedForm
from django.utils import timezone

# Create your views here.
def index(request):  #landing page
    return render(request,'wikipediaApp/index.html')

def createAuthor(request): #create an author
    form=AuthorForm()
    return render(request,'wikipediaApp/createAuthor.html',{'form':form})

def readArticle(request,ID): #read individual articles
    return render(request,'wikipediaApp/readArticle.html')

def createArticle(request): #creates new page, will create an id once created
    return render(request,'wikipediaApp/createArticle.html')

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