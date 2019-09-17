from django import forms

from .models import (
    BoastPost,
    Comment
)


class CreatePost(forms.ModelForm):
    class Meta:
        model = BoastPost
        fields = ('header',
                  'content',
                  'author')
        widgets = {'author': forms.HiddenInput()}


class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message',
                  'owner',
                  'post')
        widgets = {'owner': forms.HiddenInput(),
                   'post': forms.HiddenInput()}
