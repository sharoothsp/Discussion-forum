from django import forms
from django.forms import ModelForm, TextInput, Textarea
from .models import Subthread, Comment

class PostForm(ModelForm):
    class Meta:
        model = Subthread
        fields = ['name','topic']
        widgets = {
            'name' : TextInput(attrs={'cols':30, 'rows':30}),
            'topic': Textarea(attrs={'cols':80, 'rows':10})
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['reply']
        widgets={
            'reply': Textarea(attrs={'cols':80, 'rows':10})

        }
