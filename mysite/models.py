from django.db import models
from django.urls import reverse

class Category(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    title_menu = models.CharField(max_length=255, verbose_name='Название в меню')
    slug = models.SlugField(max_length=255, verbose_name='Псевдоним', unique=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    content = models.TextField(blank=True, verbose_name='Контент')
    parent_id = models.IntegerField(default=0, verbose_name='Родительская категория')
    published = models.IntegerField(default=1, verbose_name='Опубликован')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Изображение!!')
    visible = models.IntegerField(default=1, verbose_name='Видимость')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})  # маршрут/словарь - функция reverse работает в пайтон файлах
                                                                # тогда как функция url {% url 'category' item.slug %} в шаблонах

    class Meta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'
        ordering = ['title']

class Author(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    surname = models.CharField(max_length=150, verbose_name='Фамилия')
    username = models.SlugField(max_length=255, verbose_name='Псевдоним', unique=True)
    avatara = models.ImageField(upload_to='avataras/%Y/%m/%d/', blank=True, verbose_name='Аватара')
    email_address = models.EmailField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author', kwargs={"username": self.username})  # маршрут/словарь

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['username']

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='Псевдоним', unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='posts', blank=True, verbose_name='Автор')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')
    intro_text = models.TextField(blank=True, verbose_name='Аннотация')
    full_text = models.TextField(blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован?')
    views = models.IntegerField(default=0, verbose_name='Хиты')
    visible = models.BooleanField(default=True, verbose_name='Видимость')


    def __str__(self): # магический метод, возвращает строкоеое представление объекькта object
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.slug})  # маршрут/словарь

    class Meta:
        verbose_name = 'Статья(ю)'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, verbose_name='Псевдоним', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})  # маршрут/словарь

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['title']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья')
    name = models.CharField(max_length=100, verbose_name='Пользователь')
    email = models.EmailField(verbose_name='Адрес')
    body = models.TextField(max_length=400, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name='Опубликовано?')

    def get_absolute_url(self):
        return reverse('comment', kwargs={"slug": self.slug})  # маршрут/словарь

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at',]

    def __str__(self):
        return f'Комментарий {self.name} на {self.post}'