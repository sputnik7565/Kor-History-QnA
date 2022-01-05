from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # 소켓 구동 경로를 consumers 에 전달
    re_path(r'ws/qna/(?P<room_name>\w+)/$', consumers.AnswerConsumer.as_asgi()),
]
