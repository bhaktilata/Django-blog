# Класс ModelAdmin является представлением модели в интерфейсе администратора. Обычно они хранятся в файле с именем в приложении.
# ModelAdmin очень гибкий. Он содержит ряд параметров для настройки интерфейса администратора. Все настройки определяются в подклассе ModelAdmin:
# Объекты класса ModelAdmin:
from django.contrib import admin # предоставляет интерфейс администратора по умолчанию
from django import forms
#from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe
from .models import Post, Author, Category, Tag, Comment
#from .models import *  # импортирует все модели сразу

class PostAdminForm(forms.ModelForm):
    #intro_text = forms.CharField(widget=CKEditorUploadingWidget())
    #full_text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = PostAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'category', 'created_at', 'updated_at', 'get_photo', 'views', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'full_text',)
    list_editable = ('is_published',)
    list_filter = ('category', 'created_at', 'is_published')
    readonly_fields = ('created_at', 'updated_at', 'get_photo',)
    fields = ('title', 'slug', 'author', 'category', 'description', 'intro_text', 'full_text', 'photo', 'get_photo', 'created_at', 'updated_at', 'is_published', 'views')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')
        return '-'

    get_photo.short_description = 'Изображение'


class CategoryAdminForm(forms.ModelForm):
    #content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Category
        fields = '__all__'

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)} # параметр, который позволяет формировать slug из title автоматически
    form = CategoryAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'title_menu','slug', 'description', 'get_photo', 'visible')
    list_display_links = ('id', 'title')
    list_filter = ('title', 'visible',)
    search_fields = ('title', 'description',)
    readonly_fields = ('get_photo',)
    fields = (
    'title', 'title_menu', 'slug', 'description', 'content', 'photo', 'get_photo', 'visible')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')
        return '-'

class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm
    save_as = True
    list_display = ('id', 'name', 'surname', 'username', 'get_avatara', 'email_address')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name', 'username',)
    readonly_fields = ('get_avatara',)
    fields = ('name', 'surname', 'username', 'avatara', 'get_avatara', 'email_address')

    def get_avatara(self, obj):
        if obj.avatara:
            return mark_safe(f'<img src="{obj.avatara.url}" width="70">')
        return '-'

class TagAdminForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm
    save_as = True
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('title',)
    fields = ('title', 'slug')

class CommentAdminForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'body', 'name', 'email', 'post', 'created_at', 'active')
    list_display_links = ('id', 'body')
    list_filter = ('active', 'created_at', 'name',)
    search_fields = ('name', 'email', 'bogy',)
    readonly_fields = ('created_at', 'updated')
    fields = ('post', 'name', 'email', 'body', 'created_at', 'updated', 'active')
    actions = ['approve_comments']
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')
        return '-'

# Регистрация моделей
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
