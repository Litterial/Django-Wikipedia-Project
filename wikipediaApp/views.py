from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .forms import Author,AuthorForm,Article,ArticleForm,Related,RelatedForm
from django.utils import timezone
from django.db.models import Q
import os
from django.conf import settings
from django.contrib.auth.models import User
# Create your views here.

def index(request):  #landing page
    allArticles=Article.objects.all() #ets all articles
    article_total=len(allArticles) #gets total number of articles
    allAuthors=Author.objects.all() #gets all authors

    author_total=len(allAuthors)  #total number of authors
    context={
        'allArticles':allArticles,
        'articletotal':article_total,
        'authortotal':author_total,
    }
    return render(request,'wikipediaApp/index.html',context)

def createAuthor(request): #create an author
    form=AuthorForm(request.POST or None) #submits blank form for get request, filled form for post request
    if request.method =='POST': #if post request
        if form.is_valid(): #if form is valid
            newuser=User.objects.create_user(username=request.POST['username'],password=request.POST['password']) #create user
            newform=form.save(commit=False)
            newform.make_user=newuser #gives article model foreign key to user
            login_created_author=newform.save()
            login_created_author=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password']) #checks to see if this is a valid user, if so return a user object
            login(request,login_created_author) #request that this user is logged in

            return redirect('index') #redirects user back to index
        else:
            form=AuthorForm(request.POST) #sends posted information back to form
            context={
                'form':form,
                'errors':form.errors
            }
            return render(request,'wikipediaApp/createAuthor.html',context) #renders content on template with errors

    return render(request,'wikipediaApp/createAuthor.html',{'form':form}) #renders form on createAuthor page



@login_required
def createArticle(request): #creates new page, will create an id once created
    form=ArticleForm(request.POST or None,request.FILES or None)  #get request to create an article
    key=Author.objects.get(username=request.user)   #grabs the author that is logged in
    if request.method =='POST': #if post request
        if form.is_valid(): #if form is valid
            newForm = form.save(commit=False) #does not commit the save
            newForm.key_to_User = key  #assigns the foreign key of the created article to the current author
            newForm.save() #saves the form
            return redirect('userArticles') #redirects user to userArticle  page

        else:
            form=ArticleForm(request.POST,request.FILES) #sends posted information back to form
            context={
                'form':form,
                'errors':form.errors
            }
            return render(request,'wikipediaApp/createArticle2.html',context) #renders content on template with errors

    return render(request,'wikipediaApp/createArticle2.html',{'form':form})

def readArticle(request,ID): #read individual articles
    if request.user.is_authenticated:
        oldArticle=get_object_or_404(Article,pk=ID) #grabs the instance of an article
        readArticle=Article.objects.filter(id=ID)  #legacy code
        trueAuthor=Author.objects.get(username=request.user) #i'm using to prevent users from accessing other user's information
        readRelated=Related.objects.filter(key_to_Article=oldArticle) #gets all related items with a foreign key attached to the article
        context={
            'readArticle':readArticle,
            'readRelated':readRelated,
            'oldArticle':oldArticle,
            'trueAuthor':trueAuthor,
        }
        return render(request,'wikipediaApp/readArticle2.html',context)
    else:
        oldArticle=get_object_or_404(Article,pk=ID) #grabs the instance of an article
        readArticle=Article.objects.filter(id=ID)  #legacy code
        readRelated=Related.objects.filter(key_to_Article=oldArticle) #gets all related items with a foreign key attached to the article
        context={
            'readArticle':readArticle,
            'readRelated':readRelated,
            'oldArticle':oldArticle,

        }
        return render(request,'wikipediaApp/readArticle2.html',context)

@login_required
def userArticles(request): #list all of  articles by the user
    key=Author.objects.get(username=request.user)
    user_article=Article.objects.filter(key_to_User=key)
    context={
        'userArticles':user_article
    }
    return render (request,'wikipediaApp/userArticles2.html',context)

@login_required
def editArticle(request,ID): #edits page,needs id of instance
    oldArticle=get_object_or_404(Article,pk=ID)  #grabs instance of the old article
    showArticle=Article.objects.filter(id=oldArticle.id)
    trueAuthor=Author.objects.get(username=request.user) #i'm using to prevent users from accessing other user's information
    newArticle=ArticleForm(instance=oldArticle) #fills form with the instance
    if request.method=="POST": #if post methdod
        newArticle=ArticleForm(request.POST,request.FILES,instance=oldArticle) #gets the post informations and use instance to reference the id so a new article isn't created
        if newArticle.is_valid(): #if the article is valid
            oldArticle.key_to_User=trueAuthor
            oldArticle.last_update=timezone.now()   #changes the time to the current time
            newArticle.save() #saves the current time
            return redirect('readArticle',oldArticle.id)  #redirects to the updated article
        else:
            newArticle=ArticleForm(request.POST,request.FILES,instance=oldArticle) #grabs the error-bound form
            context={
                'form':newArticle,
                'errors':newArticle.errors,
                'readArticle':showArticle,
             }
            return render(request,'wikipediaApp/editArticle2.html',context) #renders the form with errors

    context={
        'form':newArticle,
        'readArticle':showArticle,
        'trueAuthor':trueAuthor,
        'oldArticle':oldArticle,
    }
    return render(request,'wikipediaApp/editArticle2.html',context) #renders on the editarticle page

@login_required
def deleteArticle(request,ID): #deletes article
    oldArticle=get_object_or_404(Article,pk=ID) #gets instance of old article
    trueAuthor=Author.objects.get(username=request.user) #i'm using to prevent users from accessing other user's information
    showArticle=Article.objects.filter(id=oldArticle.id)

# newArticle=ArticleForm(instance=oldArticle)
    # myuser=Author.objects.get(article=oldArticle) #
    # print(myuser)
    if request.method=='POST': #if post request
        oldArticle.delete() #deletes article
        return redirect('userArticles') #sends user back to userArticles page
    context={
        "oldArticle":oldArticle,
        'trueAuthor':trueAuthor,
        'readArticle':showArticle,
    }
    return render(request,'wikipediaApp/deleteArticle2.html',context) #renders content on template

@login_required
def createRelated(request,ID): #creates related
    article_instance=get_object_or_404(Article,pk=ID) #gets instance of parent article
    trueAuthor=Author.objects.get(username=request.user) #i'm using to prevent users from accessing other user's information
    parent_article=Article.objects.get(id=article_instance.id)
    form=RelatedForm(request.POST or None, request.FILES or None) #get request
    if request.method =='POST': #if post request
        if form.is_valid(): #if form is valid
            print(form)
            newForm = form.save(commit=False) #cancels save
            newForm.key_to_Article= article_instance #attaches foregin key to
            print( newForm.key_to_Article)
            article_instance.last_update=timezone.now() #change update time on article page
            article_instance.save() #saves time on article
            newForm.save() #saves form

            return redirect('readArticle',article_instance.id) #redirects user to parent article
        else:
            form=RelatedForm(request.POST,request.FILES) #sends posted information back to form
            context={
                'form':form,
                'errors':form.errors
            }
            return render(request,'wikipediaApp/createRelated.html',context) #renders content on template with errors
    context={
        'form':form,
        'oldArticle':article_instance,
        'trueAuthor':trueAuthor,
    }
    return render(request,'wikipediaApp/createRelated.html',context)

@login_required
def editRelated(request,ID): #edits related
    oldRelated=get_object_or_404(Related,pk=ID) #grabs instance of related
    showRelated=Article.objects.filter(related=oldRelated) #legacy code
    test=Article.objects.get(related=oldRelated) #uses reverse foreign key to grab the parrent article
    newRelated=RelatedForm(instance=oldRelated)  #creates for with the instance of the old related item
    trueAuthor=Author.objects.get(username=request.user) #i'm using to prevent users from accessing other user's information
    if request.method=="POST": #if post methdod
        newRelated=RelatedForm(request.POST,request.FILES,instance=oldRelated) #gets the post informations and use instance to reference the id so a new related isn't created
        if newRelated.is_valid(): #if the form is valid
            newerRelated=newRelated.save(commit=False)
            oldRelated.last_update=timezone.now()  #changes the time to the current time
            newerRelated.key_to_Article=test
            test.last_update=timezone.now() #change time on article
            test.save() # saves time
            newerRelated.save() #saves the current time
            return redirect('readArticle',test.id)  #redirects to congrats
        else:
            newRelated=RelatedForm(request.POST,instance=oldRelated) #grabs the error-bound form
            context={
                'form':newRelated,
                'errors':newRelated.errors,
                'readArticle':showRelated,
            }
            return render(request,'wikipediaApp/editRelated2.html',context)#renders the form with errors
    context={
        'form':newRelated,
        'readArticle':showRelated,
        'trueAuthor':trueAuthor,
        'oldArticle':test,
    }
    return render(request,'wikipediaApp/editRelated2.html',context)

@login_required
def deleteRelated(request,ID): #deletes related
    oldRelated=get_object_or_404(Related,pk=ID) #grabs instance of old related
    parent_article=Article.objects.get(related=oldRelated) #reverse foreign key to get parent article
    readArticle=Article.objects.filter(related=oldRelated) #legacy code
    trueAuthor=Author.objects.get(username=request.user) #i'm using to prevent users from accessing other user's information
    if request.method=='POST': #if post
        oldRelated.delete() #deletes
        parent_article.last_update=timezone.now() #changes time on article
        parent_article.save() #saves time
        return redirect('readArticle',parent_article.id) #redirects to parent article
    context={
        'oldRelated':oldRelated,
        "parentArticle":parent_article,
        'readArticle':readArticle,
        'trueAuthor':trueAuthor,
        'oldArticle':parent_article,
    }
    return render(request,'wikipediaApp/deleteRelated2.html',context) #renders on template

def search(request):
    search=request.POST['find'] #grabs keyword user searched for
    newsearch='' + search + " "  #added space after each word to represent a single word
    articleSearch=Article.objects.filter(Q(title__icontains=newsearch) or Q(text__icontains=newsearch)) #filters keyword
    total_articles=len(articleSearch) #graps length of the array of article search

    context={
        'search':search,
        'articleSearch':articleSearch,
        'totalarticles':total_articles,



    }

    file_ = open(os.path.join(settings.BASE_DIR,  'common'))   #opens a file with a list of common words
    a=file_.read().split() #reads the file and turn the word list into an array of elements

    # clear

    for x in a:
        print(x)
        if x == search.lower():  #if the keyword matches on of the words on the common words list renders to broad search page
            return render(request,'wikipediaApp/broadsearch.html',context)


    if len(articleSearch)== 0: # if there is element in the array, renders to a broad search page
         return render(request,'wikipediaApp/broadsearch.html',context)


    return render(request,'wikipediaApp/search.html',context)



