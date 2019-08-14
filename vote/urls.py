from django.urls import path
from vote.views import admin, auth, general

urlpatterns = [
    # Index
    path('', general.index, name='index'),

    # Login + Logout
    path('login', auth.login_user, name='login'),
    path('logout', auth.logout_user, name='logout'),

    # Voting
    path('vote/<int:headline_id>', general.vote, name='vote'),

    # Admin
    path('import_export_headlines', admin.import_export_headlines, name='import_export_headlines'),
    path('__export_headlines_func', admin.export_headlines, name='export_headlines'),
    path('check_votes', admin.check_votes, name='check_votes'),
    path('purge_user', admin.purge_user_page, name='purge_user_page'),
    path('__purge_user/<int:user_id>', admin.purge_user, name='purge_user'),
]
