from django.shortcuts import redirect

def unauthenticated_user(view_func):
    """
    Блокирует доступ к странице логина/регистрации,
    если пользователь уже авторизован.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('job_list')  # куда отправлять авторизованного
        else:
            return view_func(request, *args, **kwargs)
    return wrapper