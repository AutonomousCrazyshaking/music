from django.shortcuts import render, redirect
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import reverse
from django.db.models import Q, F
from index.models import *

_ = settings.SEARCH_VIEW

def searchView(request, page):
    """path '<int:page>.html' handler """
    if request.method == 'GET':
        # 热搜歌曲
        searchs = Dynamic.objects.select_related('song').order_by('-search').all()[:_['SEARCHS']]
        kword = request.session.get('kword', '')
        if kword:
            songs = Song.objects.filter(Q(name__icontains=kword) | Q(singer=kword)).order_by('-release').all()
        else:
            songs = Song.objects.order_by('-release').all()[:_['DEFAULT_SONGS']]
        paginator = Paginator(songs, _['PER_AGE'])
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        # 添加歌曲搜索次数
        if kword:
            idList = Song.objects.filter(name__icontains=kword)
            for i in idList:
                # 判断歌曲动态信息是否存在
                dynamics = Dynamic.objects.filter(song_id=i.id)
                if dynamics:
                    dynamics.update(search=F('search') + 1)
                else:
                    dynamics = Dynamic(plays=0, search=1, download=0, song_id=i.id)
                    dynamics.save()
        return render(request, 'search.html', locals())
    else:
        # post
        request.session['kword'] = request.POST.get('kword', '')
        return redirect(reverse('search',kwargs={'page': 1}))
