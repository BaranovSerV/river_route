from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Topic, GPXTrack
from ckeditor.widgets import CKEditorWidget

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль', 
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label='Повторите пароль', 
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Пароли не совпадают.')
        if len(cd.get('username')) > 15:
            raise forms.ValidationError('Имя пользователя не должно превышать 15 символов')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Хеширование пароля
        if commit:
            user.save()
        return user
    
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
                'rows': 40,
                'cols': 80,
            })  # Используйте CKEditorWidget для редактирования текста
        }

class GPXTrackForm(forms.ModelForm):
    class Meta:
        model = GPXTrack
        fields = ['name', 'file']
        labels = {
            'name': 'Маршрут'
        }
        widgets = {
            'name': forms.Textarea(attrs={
                'rows': 1,  # Количество строк по умолчанию
                'cols': 80,  # Ширина текстового поля
                'placeholder': 'Введите название маршрута',
                'style': 'resize: none; width: 100%;',  # Отключить изменение размеров
            })
        }
