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

def congrats(request): #confirmation page
    return render(request,'wikipediaApp/congrats.html')


def readArticle(request,ID): #read individual articles
    return render(request,'wikipediaApp/readArticle.html')

def createArticle(request): #creates new page, will create an id once created
    form=ArticleForm(request.POST or None)
    key=Author.objects.get(username=request.user)
    if request.method =='POST': #if post request
        if form.is_valid(): #if form is valid
            print(form)
            #The image is not a post, its a file. use request.FILES['name of varible in image']
            Article.objects.create(title=request.POST['title'],text=request.POST['text'],image=request.FILES['image'],date_created=timezone.now(),last_update=timezone.now(),key_to_User=key)

            return redirect('congrats') #redirects user to a confirmation page
        else:
            form=ArticleForm(request.POST) #sends posted information back to form
            context={
                'form':form,
                'errors':form.errors
            }
            return render(request,'wikipediaApp/createAuthor.html',context) #renders content on template with errors

    return render(request,'wikipediaApp/createArticle.html',{'form':form})


def userArticles(request):
    key=Author.objects.get(username=request.user)
    print(key)
    user_article=Article.objects.filter(key_to_User=key)
    context={
        'userArticles':user_article
    }
    return render (request,'wikipediaApp/userArticles.html',context)
def editArticle(request,ID): #edits page,needs id of instance
    oldArticle=get_object_or_404(Article,pk=ID)
    newArticle=ArticleForm(instance=oldArticle)
    print(oldArticle.last_update)
    if request.method=="POST":
        newArticle=ArticleForm(request.POST,instance=oldArticle)
        if newArticle.is_valid():
            print(newArticle.last_update)

            newArticle.save()
            return redirect('congrats')
        else:
            newArticle=ArticleForm(request.POST,instance=oldArticle)
            context={
                'form':newArticle,
                'errors':newArticle.errors,
             }
            return render(request,'wikipedia/editArticle.html',context)

    return render(request,'wikipediaApp/editArticle.html',{'form':newArticle})

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