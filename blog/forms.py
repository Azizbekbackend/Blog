from django import forms
from django.forms import fields
from .models import Comment
class EmailForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','body']

class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, label= '')