from django import forms

from board.models import Post, Reply


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
