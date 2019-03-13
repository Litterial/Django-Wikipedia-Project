from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('createAuthor/',views.createAuthor,name='createAuthor'),
    path('congrats/',views.congrats,name='congrats'),
    path('createArticle/',views.createArticle,name='createArticle'),
    path('userArticles/',views.userArticles,name='userArticles'),
    path('editArticle/<int:ID>/',views.editArticle,name='editArticle'),


    path('readArticle/<int:ID>/',views.readArticle,name='readArticle'),


    path('deleteArticle/<int:ID>/',views.deleteArticle,name='deleteArticle'),
    path('createRelated/<int:ID>/',views.createRelated,name='createRelated'),
    path('readRelated/<int:ID>/',views.readRelated,name='readRelated'),
    path('editRelated/<int:ID>/',views.editRelated,name='editRelated'),
    path('deleteRelated/<int:ID>/',views.deleteRelated,name='deleteRelated'),


]