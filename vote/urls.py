from django.urls import path
from . import views, auth_views, admin_views

urlpatterns = [
    # Index
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('index/<str:message>', views.index, name='index'),

    # Login
    path('login', auth_views.login_page, name='login_page'),
    path('login/<str:message>', auth_views.login_page, name='login_page'),

    # Voting
    path('detail/<int:headline_id>', views.detail, name='detail'),
    path('vote/<int:headline_id>', views.vote, name='vote'),

    # Admin
    path('admin_controls', admin_views.admin_controls, name='admin_controls'),
    path('check_votes', admin_views.check_votes, name='check_votes'),
    path('purge_user', admin_views.purge_user, name='purge_user'),
    path('purge_user_process/<int:user_id>', admin_views.purge_user_process, name='purge_user_process'),

    # Login Redirect URLS
    path('login_user', auth_views.login_user, name='login'),
    path('logout_user', auth_views.logout_user, name='logout')
]
