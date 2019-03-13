from django.shortcuts import render,redirect,get_object_or_404
from .forms import Author,AuthorForm,Article,ArticleForm,Related,RelatedForm
from django.utils import timezone
from django.contrib.auth.models import User
# Create your views here.
def index(request):  #landing page
    allArticles=Article.objects.all()
    return render(request,'wikipediaApp/index.html',{'allArticles':allArticles})

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

def readArticle(request,ID): #read individual articles
    oldArticle=get_object_or_404(Article,pk=ID) #grabs id of the article
    read=Article.objects.filter(id=ID)  #grabs instance of the old article
    return render(request,'wikipediaApp/readArticle.html',{'Read':read})

def userArticles(request): #list all of the user
    key=Author.objects.get(username=request.user)
    print(key)
    user_article=Article.objects.filter(key_to_User=key)
    context={
        'userArticles':user_article
    }
    return render (request,'wikipediaApp/userArticles.html',context)
def editArticle(request,ID): #edits page,needs id of instance
    oldArticle=get_object_or_404(Article,pk=ID) #grabs id of the article
    newArticle=ArticleForm(instance=oldArticle)  #grabs instance of the old article
    if request.method=="POST": #if post methdod
        newArticle=ArticleForm(request.POST,instance=oldArticle) #gets the post informations and use instance to reference the id so a new article isn't created
        if newArticle.is_valid(): #if the article is valid
            oldArticle.last_update=timezone.now()   #changes the time to the current time
            newArticle.save() #saves the current time
            return redirect('congrats')  #redirects to congrats
        else:
            newArticle=ArticleForm(request.POST,instance=oldArticle) #grabs the error-bound form
            context={
                'form':newArticle,
                'errors':newArticle.errors,
             }
            return render(request,'wikipediaApp/editArticle.html',context) #renders the form with errors

    return render(request,'wikipediaApp/editArticle.html',{'form':newArticle}) #renders on the editarticle page

def deleteArticle(request,ID): #deletes needs id of instace
    oldArticle=get_object_or_404(Article,pk=ID)
    newArticle=ArticleForm(instance=oldArticle)
    if request.method=='POST':
        oldArticle.delete()
        return redirect('congrats')
    return render(request,'wikipediaApp/deleteArticle.html',{'form':newArticle})

def readRelated(request,ID): #reads related needs id of parent

    return render(request,'wikipediaApp/readRelated.html',{'ID':ID})

def createRelated(request,ID): #creates related needs id of parent
    articleID=get_object_or_404(Article,pk=ID)
    form=RelatedForm(request.POST or None)
    if request.method =='POST': #if post request
        if form.is_valid(): #if form is valid
            print(form)
            #The image is not a post, its a file. use request.FILES['name of varible in image']
            Related.objects.create(title=request.POST['title'],text=request.POST['text'],image=request.FILES['image'],date_created=timezone.now(),last_update=timezone.now(),key_to_article=articleID)

            return redirect('congrats') #redirects user to a confirmation page
        else:
            form=RelatedForm(request.POST) #sends posted information back to form
            context={
                'form':form,
                'errors':form.errors
            }
            return render(request,'wikipediaApp/createRelated.html',context) #renders content on template with errors
    return render(request,'wikipediaApp/createRelated.html',{'form':form})

def editRelated(request,ID): #edits related needs id of parent
    oldRelated=get_object_or_404(Related,pk=ID) #grabs id of the article
    newRelated=RelatedForm(instance=Related)  #grabs instance of the old article
    if request.method=="POST": #if post methdod
        newRelated=RelatedForm(request.POST,instance=Related) #gets the post informations and use instance to reference the id so a new article isn't created
        if newRelated.is_valid(): #if the article is valid
            oldRelated.last_update=timezone.now()   #changes the time to the current time
            newRelated.save() #saves the current time
            return redirect('congrats')  #redirects to congrats
        else:
            newRelated=RelatedForm(request.POST,instance=Related) #grabs the error-bound form
            context={
                'form':newRelated,
                'errors':newRelated.errors,
            }
            return render(request,'wikipediaApp/editRelated.html',context) #renders the form with errors    return render(request,'wikipediaApp/editRelated.html',{'ID':ID})
    return render(request,'wikipediaApp/editRelated.html',{'form':newRelated})

def deleteRelated(request,ID): #deletes related neeeds id of parent
    oldRelated=get_object_or_404(Related,pk=ID)
    newRelated=RelatedForm(instance=Related)
    if request.method=='POST':
        oldRelated.delete()
        return redirect('congrats')
    return render(request,'wikipediaApp/deleteRelated.html',{'form':newRelated})
