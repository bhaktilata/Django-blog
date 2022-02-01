from django.urls import path  # функция path связывает контроллер views и template (странитцами) - это функция для обработки пути
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(6)(Home.as_view()), name='home'),
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostByCategory.as_view(), name='category'), # список статей выбранной категории
    path('post/add-post/', CreatePost.as_view(), name='add_post'), # добавление статьи
    path('post/<str:slug>/', post_comment, name='post'),
    #path('post/<str:slug>/', GetPost.as_view(), name='post'), # показ полной статьи

    #path('category/list', GetCategory.as_view(), name='categories'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('feedback/', contact, name='contact'),

   #path('404/', get_error, name='error'),

]



