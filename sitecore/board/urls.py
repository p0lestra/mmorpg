from django.urls import path

from board.views import PostsList, PostDetail, PostCreate, ReplyAdd, PostEdit, Replies

urlpatterns = [
   path('', PostsList.as_view(), name='posts'),
   path('<int:pk>', PostDetail.as_view(), name='post'),
   path('create/', PostCreate.as_view(), name='postcreate'),
   path('<int:pk>/reply/add', ReplyAdd.as_view(), name='reply_add'),
   path('<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
   path('replies/', Replies.as_view(), name='replies')
]
