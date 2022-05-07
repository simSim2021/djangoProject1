from django.shortcuts import render

from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime

from .models import Capital, Option
# Базовый класс для обработки страниц с формами.
from django.views.generic.edit import FormView
# Спасибо django за готовую форму регистрации.
from django.contrib.auth.forms import UserCreationForm
# Спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm
# Функция для установки сессионного ключа.
# По нему django будет определять,
# выполнил ли вход пользователь.
from django.contrib.auth import login
# Для Log out с перенаправлением на главную
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
# Для смены пароля - форма
from django.contrib.auth.forms import PasswordChangeForm
# оценки
from .models import Mark
# вычисление среднего,
# например, средней оценки
from django.db.models import Avg
# для ответа на асинхронный запрос в формате JSON
from django.http import JsonResponse
import json


# базовый URL приложения, главной страницы -
# часто нужен при указании путей переадресации
app_url = "/geography/"


# главная страница со списком столиц
def index(request):
    message = None
    if "message" in request.GET:
        message = request.GET["message"]
    # создание HTML-страницы по шаблону index.html
    # с заданными параметрами latest_geography и message
    return render(
        request,
        "index.html",
        {
            "latest_geography":
                Capital.objects.order_by('-pub_date')[:100],
            "message": message
        }
    )


# страница столицы со списком ответов
def detail(request, capital_id):
    error_message = None
    if "error_message" in request.GET:
        error_message = request.GET["error_message"]
    return render(
        request,
        "answer.html",
        {
            "capital": get_object_or_404(Capital, pk=capital_id),
            "error_message": error_message,
            # кол-во оценок, выставленных пользователем
            "already_rated_by_user":
                Mark.objects
                    .filter(author_id=request.user.id)
                    .filter(capital_id=capital_id)
                    .count(),
            # оценка текущего пользователя
            "user_rating":
                Mark.objects
                    .filter(author_id=request.user.id)
                    .filter(capital_id=capital_id)
                    .aggregate(Avg('mark'))
                ["mark__avg"],
            # средняя по всем пользователям оценка
            "avg_mark":
                Mark.objects
                    .filter(capital_id=capital_id)
                    .aggregate(Avg('mark'))
                ["mark__avg"]

        }
    )
# обработчик выбранного варианта ответа -
# сам не отдает страниц, а только перенаправляет (redirect)
# на другие страницы с передачей в GET-параметре
# сообщения для отображения на этих страницах


def answer(request, capital_id):
    capital = get_object_or_404(Capital, pk=capital_id)
    try:
        option = capital.option_set.get(pk=request.POST['option'])
    except (KeyError, Option.DoesNotExist):
        return redirect(
            '/geography/' + str(capital_id) +
            '?error_message=Такой вариант ответа не существует',
        )
    else:
        if option.correct:
            return redirect(
                "/geography/?message=Отлично! Проверим дальше!")
        else:
            return redirect(
                '/geography/' + str(capital_id) +
                '?error_message=Неправильный ответ!',
            )

# наше представление для регистрации


class RegisterFormView(FormView):
    # будем строить на основе
    # встроенной в django формы регистрации
    form_class = UserCreationForm
    # Ссылка, на которую будет перенаправляться пользователь
    # в случае успешной регистрации.
    # В данном случае указана ссылка на
    # страницу входа для зарегистрированных пользователей.
    success_url = app_url + "login/"
    # Шаблон, который будет использоваться
    # при отображении представления.
    template_name = "reg/register.html"

    def form_valid(self, form):
        # Создаём пользователя,
        # если данные в форму были введены корректно.
        form.save()
        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


# наше представление для входа
class LoginFormView(FormView):
    # будем строить на основе
    # встроенной в django формы входа
    form_class = AuthenticationForm
    # Аналогично регистрации,
    # только используем шаблон аутентификации.
    template_name = "reg/login.html"
    # В случае успеха перенаправим на главную.
    success_url = app_url

    def form_valid(self, form):
        # Получаем объект пользователя
        # на основе введённых в форму данных.
        self.user = form.get_user()
        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

# для выхода - миниатюрное представление без шаблона -
# после выхода перенаправим на главную


class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя,
        # запросившего данное представление.
        logout(request)
        # После чего перенаправляем пользователя на
        # главную страницу.
        return HttpResponseRedirect(app_url)


# наше представление для смены пароля
class PasswordChangeView(FormView):
    # будем строить на основе
    # встроенной в django формы смены пароля
    form_class = PasswordChangeForm
    template_name = 'reg/password_change_form.html'
    # после смены пароля нужно снова входить
    success_url = app_url + 'login/'

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(PasswordChangeView, self).form_valid(form)


def post_mark(request, capital_id):
    msg = Mark()
    msg.author = request.user
    msg.capital = get_object_or_404(Capital, pk=capital_id)
    msg.mark = request.POST['mark']
    msg.pub_date = datetime.now()
    msg.save()
    return HttpResponseRedirect(app_url+str(capital_id))


def get_mark(request, capital_id):
    res = Mark.objects\
            .filter(capital_id=capital_id)\
            .aggregate(Avg('mark'))

    return JsonResponse(json.dumps(res), safe=False)
