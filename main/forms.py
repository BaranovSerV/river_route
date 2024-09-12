from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Topic

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 10,  # Количество строк по умолчанию
                'cols': 80,  # Ширина текстового поля
                'placeholder': 'Введите содержание темы',
                'style': 'resize: none; width: 100%;',  # Отключить изменение размеров
            })
        }