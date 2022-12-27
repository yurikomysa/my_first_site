from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect



# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from visioners.forms import *
from visioners.models import *
from visioners.utils import *


class VisHome(DataMixin, ListView):
    model = Visioners
    template_name = 'visioners/index.html'
    context_object_name = 'posts'
    # extra_context = {'title': 'Главная страница'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

class VisCategory(DataMixin, ListView):
    model = Visioners
    template_name = 'visioners/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat_id),
                                      cat_selected=context['posts'][0].cat_id)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Visioners.objects.filter(cat__id=self.kwargs['cat_id'], is_published=True)

class ShowPost(DataMixin, DetailView):
    model = Visioners
    template_name = 'visioners/post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'visioners/addpage.html'
    success_url = reverse_lazy('home')
    # login_url = '/admin/'
    login_url = reverse_lazy('login')
    # raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить статью')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'visioners/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'visioners/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'visioners/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')




def logout_user(request):
    logout(request)
    return redirect('login')

# def index(request): #HttpRequest
#     posts = Visioners.objects.all()
#     cats = Category.objects.all()
#     return render(request, 'visioners/index.html',
#                   {'menu': menu,
#                    'title': 'Главная страница',
#                    'posts': posts,
#                    'cats': cats,
#                    'cat_selected': 0,
#                    })

def about(request):
    contact_list = Visioners.objects.all()
    paginator = Paginator(contact_list, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'visioners/about.html',
                  {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})

def categories(request, catid):
    if (request.GET):
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")

def archive(request, year):
    if int(year) > 2022:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             try:
#                 form.save()
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Ошибка добавления поста')
#     else:
#         form = AddPostForm()
#     return render(request, 'visioners/addpage.html',
#                   {'menu': menu,
#                    'title': 'Добавление статьи',
#                    'form': form,
#                    })


def contact(request):
    return HttpResponse("Обратная связь")


# def login(request):
#     return HttpResponse("Авторизация")

# def show_post(request, post_id):
#     return HttpResponse(f"Отображение статьи с id = {post_id}")
#
# def show_category(request, cat_id):
#     posts = Visioners.objects.filter(cat_id=cat_id)
#     cats = Category.objects.all()
#     if len(posts) == 0:
#         raise Http404()
#
#     return render(request, 'visioners/index.html',
#                   {'menu': menu,
#                    'title': 'Отображение по рубрикам',
#                    'posts': posts,
#                    'cats': cats,
#                    'cat_selected': cat_id,
#                    })

