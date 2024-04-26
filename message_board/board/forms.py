from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    text = forms.CharField(label='Введите текст сообщения: ', max_length=1000)

    class Meta:
        model = Post
        fields = ['text']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='Прокомментировать: ', max_length=1000)

    class Meta:
        model = Comment
        fields = ['comment']
