from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = (
            'Введите какой нибудь текст'
        )
        self.fields['group'].empty_label = (
            'Выберите группу 🙂'
        )

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': "Текст поста",
            'group': "Группа",
        }
        help_texts = {
            'text': "Текст нового поста",
            'group': "Выбрать группу",
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Текст',
        }
        help_texts = {
            'text': 'Текст нового комментария',
        }
