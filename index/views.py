from django.shortcuts import render
from django.conf import settings
from .models import *

_ = settings.INDEX_VIEW
def indexView(request):
    """path '' handler """
    songDynamic = Dynamic.objects.select_related('song')
    # 热搜歌曲
    searchs = songDynamic.order_by('-search').all()[:_['SEARCHS']]
    labels = Label.objects.all()
    # 热门歌曲
    popular = songDynamic.order_by('-plays').all()[:_['POPULAR']]
    # 新歌推荐
    recommend = Song.objects.order_by('-release').all()[:_['RECOMMEND']]
    # 热门下载
    downloads = songDynamic.order_by('-download').all()[:_['DOWNLOADS']]
    tabs = [searchs[:_['TABS']], downloads[:_['TABS']]]
    return render(request, 'index.html', locals())

def page_not_found(request, exception):
    """404 page"""
    return render(request, '404.html', status=404)

def page_error(request):
    """500 page"""
    return render(request, '404.html', status=500)