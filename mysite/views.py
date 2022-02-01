from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, UserRegisterForm, UserLoginForm, ContactForm, CommentForm
from .models import Post, Category, Comment, Tag, Author
from django.db.models import F # F() ORM позволит вам использовать поля текущей модели в ваших запросах
from .utils import MyMixin
from django.core.paginator import Paginator
from django.shortcuts import render
#from django.contrib.auth.forms import UserCreationForm # форма создания пользователя
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

class Home(ListView):
    model = Post
    template_name = 'mysite/index.html'
    context_object_name = 'news'
    #queryset = Post.objects.select_related('category')
    #extra_context = {'title': 'Главная'} # только для статичных данных
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related('category') # управляет выводом опубликованных материалов
    #  в случае ленивой загрузки  return Post.objects.filter(is_published=True) получается слишком много запросов для главной чстраницы
    #  при выводе 15 аннотаций статей. Использование .select_related('category') [подходит при работе со связью models.ForeignKey]
    #  позволяет загрузить связанные данные не отложенно. а жадно, т.е. сразу же при выборке и получении новостей, это делать можно
    #  кргда эти данные точно будут использованы, Это позволяет уменьшить число запросов  в 2 раза/
    #  Метод prefetch_related() используется для свяязи ManyToMany

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Институт сознания INICONS'
        return context

# django.views.generic.list.ListView предоставляет встроенный способ разбить отображаемый список на страницы.
# Это ограничивает количество объектов на странице и добавляет в context paginator и page_obj,
# что позволяет меньше писать кода, чем в классе-функции listing(request)
class PostByCategory(ListView):    # выводит список статей выбранной категории
    template_name = 'mysite/category.html'
    context_object_name = 'posts_list'
    paginate_by = 2
    allow_empty = False # ошибка 404 при несуществующей категории

    def get_queryset(self):
        #return Post.objects.filter(visible=True) # управляет выводом опубликованных всех материалов всех категорий
        return Post.objects.filter(category__slug=self.kwargs['slug'], is_published=True).select_related('author') # обращается к полю 'slug' связанной модели category, который получается в маршруте
                                                                       # поэтому здесь выводятся статьи только выбранной категории

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug']) # извлекаем title, название текущей категории по слагу благодаря связанным моделям
        return context

class GetPost(DetailView):               # выводит полную статью
    model = Post
    template_name = 'mysite/post_single.html'
    context_object_name = 'post_item'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context

# создание поста с фронтента
class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostForm                   # связываем класс с формой
    template_name = 'mysite/add_post.html'
    # login_url = '/admin/'
    #raise_exception = True
    # success_url = reverse_lazy('home')


def page_not_found_view(request, exception):
    return render(request, 'mysite/404.html', status=404)

def get_error(request):
    return render(request, 'mysite/404.html')

# методы разбиения на страницы используют класс Paginator. Он делает всю работу по фактическому разбиению
# QuerySet на объекты Page.
'''
def listing(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 2) #создаем объект класса Paginator, в качестве параметра
    # передаются все объекты (список post_list статей) и количчество элементов,
    # котоые мы хотим иметь на каждой странице. В итоге получаем это методы доступа к элементам для каждой страницы
    page_number = request.GET.get('page', 1) # запрос на получения номера страницы
    page_obj = paginator.get_page(page_number)
    return render(request, 'mysite/category.html', {'page_obj': page_obj})
'''
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) # создаем экземпляр формы и передаем в контекст
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'mysite/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'mysite/login.html', {"form": form})

def user_logout(request):
    logout(request)
    return redirect('login')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail('subject', 'content', 'admin@inicons.ru', ['bvlata@mail.ru'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = ContactForm()
    return render(request, 'mysite/feedbsck.html', {"form": form})

# функция для создания комментарий
def post_comment(request, slug):
    #form_class =  CommentForm
    template_name = 'mysite/post_single.html'
    post = get_object_or_404(Post, slug=slug) # назначаем переменной 'post' все данные объекта Post, выбираемого по слагу
    comments = post.comments.filter(active=True) # извлекает из базы данных все одобренные комментарии
    # Поскольку это та же самая страница, на которой пользователи будут создавать новые комментарии, мы инициализировали
    # переменную new_comment, установив для нее значение none.
    new_comment = None
    # Comment posted

    if request.method == 'POST': # переменная comment_form будет содержать данные пользовательского ввода
        comment_form = CommentForm(data=request.POST) # создаем экземпляр класса формы комметнраия
        if comment_form.is_valid():
            # Создаем новый объект комментария Comment, вызывая метод формы save(), присваимваем его переменной new_comment,
            # но пока не сохранять в базе данных, потому что нам все еще нужно связать его с объектом сообщения (статьей)
            new_comment = comment_form.save(commit=False)
            # привязываем объект комментария к текущему посту
            new_comment.post = post
            # Сохраните объект (комментарий) в базе данных
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, template_name, {'post': post,
                                           'comments': comments,  # выводит список комментарий
                                           'new_comment': new_comment, # выводит новый комментарий
                                           'comment_form': comment_form} # выводит форму омментарий
    )

