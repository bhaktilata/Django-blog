# Generated by Django 4.0 on 2022-01-30 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('surname', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('username', models.SlugField(max_length=255, unique=True, verbose_name='Псевдоним')),
                ('avatara', models.ImageField(blank=True, upload_to='avataras/%Y/%m/%d/', verbose_name='Аватара')),
                ('email_address', models.EmailField(max_length=100)),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
                'ordering': ['username'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name='Название')),
                ('title_menu', models.CharField(max_length=255, verbose_name='Название в меню')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Псевдоним')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('content', models.TextField(blank=True, verbose_name='Контент')),
                ('parent_id', models.IntegerField(default=0, verbose_name='Родительская категория')),
                ('published', models.IntegerField(default=1, verbose_name='Опубликован')),
                ('photo', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Изображение!!')),
                ('visible', models.IntegerField(default=1, verbose_name='Видимость')),
            ],
            options={
                'verbose_name': 'Категория(ю)',
                'verbose_name_plural': 'Категории',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True, verbose_name='Псевдоним')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Псевдоним')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Описание')),
                ('intro_text', models.TextField(blank=True, verbose_name='Аннотация')),
                ('full_text', models.TextField(blank=True, verbose_name='Контент')),
                ('photo', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Изображение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликован?')),
                ('views', models.IntegerField(default=0, verbose_name='Хиты')),
                ('visible', models.BooleanField(default=True, verbose_name='Видимость')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='mysite.author', verbose_name='Автор')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mysite.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Статья(ю)',
                'verbose_name_plural': 'Статьи',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Пользователь')),
                ('email', models.EmailField(max_length=254, verbose_name='Адрес')),
                ('body', models.TextField(max_length=400, verbose_name='Комметнарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Опубликовано?')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='mysite.post', verbose_name='Статья')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['created_at'],
            },
        ),
    ]
