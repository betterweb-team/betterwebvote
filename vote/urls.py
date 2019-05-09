from django.urls import path
from . import views
from vote.views import admin, auth

urlpatterns = [
    # Index
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('index/<str:message>', views.index, name='index'),

    # Login
    path('login', auth.login_page, name='login_page'),
    path('login/<str:message>', auth.login_page, name='login_page'),

    # Voting
    path('detail/<int:headline_id>', views.detail, name='detail'),
    path('vote/<int:headline_id>', views.vote, name='vote'),

    # Admin
    path('admin_controls', admin.admin_controls, name='admin_controls'),
    path('check_votes', admin.check_votes, name='check_votes'),
    path('purge_user', admin.purge_user, name='purge_user'),
    path('purge_user_process/<int:user_id>', admin.purge_user_process, name='purge_user_process'),

    # Login Redirect URLS
    path('login_user', auth.login_user, name='login'),
    path('logout_user', auth.logout_user, name='logout')
]
