from rest_framework import fields, serializers
from rest_framework.utils.field_mapping import ClassLookupDict
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title','slug','body','status']