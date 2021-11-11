from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from .models import Post, Comment
from .serializers import PostSerializer

class PostListView(ListAPIView):
    queryset = Post.objects.filter(status='published')
    serializer_class = PostSerializer