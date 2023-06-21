from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields

from app.models import Answer, Question

class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=4,
        max_length=80,
    )
    password = forms.CharField(
        min_length=8,
        max_length=80,
        widget=forms.PasswordInput,
    )

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'avatar',
        ]

    avatar = forms.FileField(
        required=False,
    )

    def save(self, commit=True):
        user = super().save(commit)
        
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            user.profile.avatar = avatar
            user.profile.save()
        
        return user


# TODO: убрать дублирование?
class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'avatar',
        ]

    avatar = forms.FileField(
        required=False,
    )

    def save(self, commit=True):
        user = super().save(commit)
        
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            user.profile.avatar = avatar
            user.profile.save()
        
        return user


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'title',
            'text',
        ]
        
    title = fields.CharField(
        min_length=4,
        max_length=160,
    )
    text = fields.CharField(
        min_length=4,
        max_length=8000,
        widget=forms.Textarea(
            attrs={
                'placeholder': "Enter the question text",
            },
        ),
    )
    

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            'text',
        ]
        
    text = fields.CharField(
        min_length=4,
        max_length=8000,
        widget=forms.Textarea(
            attrs={
                'placeholder': "Enter your answer to the question",
            },
        ),
    )
