from django.urls import path
from vote.views import admin, auth, general

urlpatterns = [
    # Index
    path('', general.index, name='index'),

    # Login + Logout
    path('login', auth.LoginFormView.as_view(), name='login'),
    path('__logout', auth.logout_user, name='logout'),

    # Voting
    path('detail/<int:headline_id>', general.detail, name='detail'),
    path('vote/<int:headline_id>', general.vote, name='vote'),

    # Admin
    path('admin_controls', admin.admin_controls, name='admin_controls'),
    path('check_votes', admin.check_votes, name='check_votes'),
    path('purge_user', admin.purge_user_page, name='purge_user_page'),
    path('__purge_user/<int:user_id>', admin.purge_user, name='purge_user'),
    path('__import_headlines', admin.import_headlines, name='import_headlines')
]
