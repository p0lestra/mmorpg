from django.urls import path

from board.views import PostsList, PostDetail, PostCreate, ReplyAdd

urlpatterns = [
   path('', PostsList.as_view(), name='posts'),
   path('<int:pk>', PostDetail.as_view(), name='post'),
   path('create/', PostCreate.as_view(), name='postcreate'),
   path('<int:pk>/reply/add', ReplyAdd.as_view(), name='reply_add'),
]
