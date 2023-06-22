from django import forms
from .models import Note, Group, UserProfile

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'category']

class GroupForm(forms.ModelForm):
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))
    class Meta:
        model = Group
        fields = ['name', 'color']

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['employment_status', 'profile_photo']

class DeleteAccountForm(forms.Form):
    confirmation = forms.CharField(label='Confirmation', max_length=20)

class EmploymentStatusForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['employment_status']

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_photo',)

        