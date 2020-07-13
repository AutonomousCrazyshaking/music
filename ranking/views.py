from django.shortcuts import render
from index.models import *
from django.views.generic import ListView
from django.conf import settings

_ = settings.RANKING_VIEW


def rankingView(request):
    """path '' handler """
    # 热搜歌曲
    searchs = Dynamic.objects.select_related('song').order_by('-search').all()[:_['SEARCHS']]
    labels = Label.objects.all()
    # 歌曲列表信息
    t = request.GET.get('type', '')
    if t:
        dynamics = \
            Dynamic.objects.select_related('song').filter(song__label=t).order_by('-plays').all()[:_['TOP']]
    else:
        dynamics = Dynamic.objects.select_related('song').order_by('-plays').all()[:_['TOP']]
    return render(request, 'ranking.html', locals())
