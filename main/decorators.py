from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            context = {}
            user = request.user
            group_name = Group.objects.get(user=user).name

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                context['message'] = 'This account does not have the permissions to access this page'
                return render(request, 'main/body.html', context)
        return wrapper_func
    return decorator