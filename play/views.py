from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.conf import settings
from index.models import *

_ = settings.PLAY_VIEW

def playView(request, id):
    """path '<int:id>.html' handler """
    # 热搜歌曲
    searchs = Dynamic.objects.select_related('song').order_by('-search').all()[:_['SEARCHS']]
    # 相关歌曲推荐
    type = Song.objects.values('type').get(id=id)['type']
    relevant = Dynamic.objects.select_related('song').filter(song__type=type).order_by('-plays').all()[:_['RELEVANT']]
    # 歌曲信息
    songs = Song.objects.get(id=int(id))
    play_list = request.session.get('play_list', [])
    exist = False
    if play_list:
        for i in play_list:
            if int(id) == i['id']:
                exist = True
    if exist is False:
        play_list.append({'id': int(id), 'singer': songs.singer, 'name': songs.name, 'time': songs.time})
    request.session['play_list'] = play_list
    # 歌词
    if songs.lyrics != '暂无歌词':
        lyrics = str(songs.lyrics.url)[1::]
        with open(lyrics, 'r', encoding='utf-8') as f:
            lyrics = f.read()
    # 添加播放次数
    p = Dynamic.objects.filter(song_id=int(id)).first()
    plays = p.plays + 1 if p else 1
    Dynamic.objects.update_or_create(song_id=id, defaults={'plays': plays})
    return render(request, 'play.html', locals())


def downloadView(request, id):
    """path 'download/<int:id>.html' handler """
    # 添加下载次数
    p = Dynamic.objects.filter(song_id=int(id)).first()
    download = p.download + 1 if p else 1
    Dynamic.objects.update_or_create(song_id=id, defaults={'download': download})
    # 读取文件内容
    songs = Song.objects.get(id=int(id))
    file = songs.file.url[1::]
    def file_iterator(file, chunk_size=512):
        with open(file, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    f = songs.name + '.m4a'
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachement;filename="%s"' % f
    return response