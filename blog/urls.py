from blog.api_views import PostListView
from django.urls import path
from .views import post_list,post_detail, post_share
app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', post_list,name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',post_detail,name='post_detail'),
    path('<int:id>/share/', post_share, name="post_share"),
    path('api/v1/', PostListView.as_view())
]