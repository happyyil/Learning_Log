from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text', 'private']
        labels = {'text': '主题', 'private': '设为私有'}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text', 'private']
        labels = {'text': '内容', 'private': '设为私有'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
