from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Answer, Question, Comment

class CustomUserCreationForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'gender', 'password1', 'password2']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']