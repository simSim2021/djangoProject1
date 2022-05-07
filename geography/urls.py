from django.urls import path, re_path

from . import views

app_name = 'geography'
urlpatterns = [
    path(r'', views.index, name='index'),
    re_path(r'^([0-9]+)/$', views.detail, name='detail'),
    re_path(r'^([0-9]+)/answer/$', views.answer, name='answer'),
    re_path(r'^register/$', views.RegisterFormView.as_view()),
    re_path(r'^login/$', views.LoginFormView.as_view()),
    re_path(r'^logout/$', views.LogoutView.as_view()),
    re_path(r'^password-change/', views.PasswordChangeView.as_view()),
    # отправка оценки
    re_path(r'^([0-9]+)/post_mark/$', views.post_mark, name='post_mark'),
    # средняя оценка
    re_path(r'^([0-9]+)/get_mark/$', views.get_mark, name='get_mark'),

]
