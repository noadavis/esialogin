from django.shortcuts import render
from user.models import checkRights


@checkRights
def dashboard(request, obj_id, obj_adds):
    page_info = {
        'name': 'Главная',
        'icon': 'home',
        'br': 'Главная',
        'bp': '/about/dashboard/',
        'userinfo': obj_id
    }

    data = {
        'description': {
            'additional': 'Добро пожаловать',
            'text': 'Нет описания.',
        },
        'news': {}
    }

    return render(request, 'dashboard.html', { 'page_info': page_info, 'user_adds': obj_adds, 'data': data })

