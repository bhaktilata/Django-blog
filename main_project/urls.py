"""main_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Представления функций
     1. Добавьте  import: from my_app import views
     2. Добавьте URL-адрес в URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Добавьте import:  from other_app.views import Home
    2. Добавьте a URL to urlpatterns:  path('', Home.as_view(), name='home')
В том числе другой URLconf
    1. Импортируйте функцию include(): from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from mysite.views import index

from django.conf import settings            # импортируем настройки
from django.conf.urls.static import static  # импортиурем модуль static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('mysite.urls')),
    #path('blog/', include('blog.urls')),
    #path('news/', include('news.urls')),
]


# для режима debug указываем где искать выгруженные файлы
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
         path('__debug__/', include(debug_toolbar.urls)),
     ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#handler404 = "mysite.views.page_not_found_view"