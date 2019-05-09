from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def admin_page(func):
    @login_required(login_url='login_page')
    def render(req, *args, **kwargs):
        if not req.user.is_superuser:
            return redirect('index', 'noperm')
        return func(req, *args, **kwargs)
    return render