from django import forms
from .models import Note, Group

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'category']

class GroupForm(forms.ModelForm):
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))
    class Meta:
        model = Group
        fields = ['name', 'color']
