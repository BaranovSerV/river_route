from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login  # Убедитесь, что этот импорт существует
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserProfileForm, TopicForm
from .models import UserProfile, Topic
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')  # Убедитесь, что используете правильный URL
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Передаем два аргумента: request и user
            return redirect('index')  # Перенаправляем на главную страницу
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})



def index(request):
    return render(request, 'index.html')

def report(request):
    return render(request, 'report.html')

def favourites(request):
    return render(request, 'favourites.html')

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile.html', {'form': form})

@login_required
def add_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)  # Создаем объект, но не сохраняем его в базе данных
            topic.author = request.user  # Устанавливаем текущего пользователя как автора
            topic.save()  # Сохраняем объект с автором
            return redirect('forum')  # Перенаправление на страницу форума после добавления темы
    else:
        form = TopicForm()
    return render(request, 'add_topic.html', {'form': form})


def forum(request):
    topics = Topic.objects.all().order_by('-created_at')  # Получаем все темы отсортированные по дате
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect('forum')
    else:
        form = TopicForm()
    return render(request, 'forum.html', {'form': form, 'topics': topics})

def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    return render(request, 'topic_detail.html', {'topic': topic})