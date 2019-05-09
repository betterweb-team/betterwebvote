from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:headline_id>', views.detail, name='detail'),
    path('vote/<int:headline_id>', views.vote, name='vote'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout')
]
