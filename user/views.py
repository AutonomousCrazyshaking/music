from django.shortcuts import render, redirect, reverse
from .form import MyUserCreationForm
from .models import MyUser
from index.models import *
from django.db.models import Q, F
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from common.paginator import cPaginator as Paginator


def loginView(request):
    """path 'login.html' handler """
    user = MyUserCreationForm()
    if request.method == 'POST':
        if request.POST.get('loginUser', ''):
            u = request.POST.get('loginUser', '')
            p = request.POST.get('password', '')
            if MyUser.objects.filter(Q(mobile=u) | Q(username=u)):
                u1 = MyUser.objects.filter(Q(mobile=u) | Q(username=u)).first()
                if check_password(p, u1.password):
                    login(request, u1)
                    return redirect(reverse('home', kwargs={'page': 1}))
                else:
                    tips = '密码错误'
            else:
                tips = '用户不存在'
        else:
            # 注册
            u = MyUserCreationForm(request.POST)
            print(u.errors)
            if u.is_valid():
                u.save()
                tips = '注册成功'
            else:
                if u.errors.get('username', ''):
                    tips = u.errors.get('username', '注册失败')
                else:
                    tips = u.errors.get('mobile', '注册失败')
    return render(request, 'user.html', locals())


@login_required(login_url='/user/login.html')
def homeView(request, page):
    """path 'home/<int:page>.html' handler """
    searchs = Dynamic.objects.select_related('song').order_by('-search').all()[:4]
    songs = request.session.get('play_list', [])
    paginator = Paginator(songs, 3)
    pages = paginator.page(page)
    return render(request, 'home.html', locals())


def logoutView(request):
    """path 'logout.html' handler """
    logout(request)
    return redirect('/')