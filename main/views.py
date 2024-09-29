from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login as auth_login, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserProfileForm, TopicForm, GPXTrackForm
from .models import UserProfile, Topic, GPXTrack
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
import gpxpy

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index', username=user.username)  # Перенаправляем на профиль
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

def routes(request):
    return render(request, 'poster/routes.html')

def report(request):
    return render(request, 'report.html')

def favourites(request):
    return render(request, 'favourites.html')


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile.html', {'form': form, 'user_profile': user_profile})

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
    
    # Увеличиваем счетчик просмотров
    topic.views += 1
    topic.save(update_fields=['views'])
    
    return render(request, 'topic_detail.html', {'topic': topic})

def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'user_profile.html', {'user': user})

@user_passes_test(lambda u: u.is_superuser)  # Проверка, что пользователь - администратор
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    topic.delete()
    return redirect('forum')  # Перенаправление на страницу форума после удаления





def routes_view(request):
    if request.method == 'POST':
        form = GPXTrackForm(request.POST, request.FILES)
        if form.is_valid():
            gpx_file = request.FILES['file']
            track = form.save(commit=False)

            # Чтение и парсинг GPX файла
            gpx = gpxpy.parse(gpx_file.read().decode('utf-8'))

            distance = 0
            elevation_gain = 0
            previous_elevation = None

            # Перебираем все треки и их сегменты
            for gpx_track in gpx.tracks:
                for segment in gpx_track.segments:
                    # Вычисляем длину сегмента
                    distance += segment.length_2d() / 1000  # длина в км

                    # Проходим по точкам и вычисляем набор высоты
                    for point in segment.points:
                        if point.elevation is not None:  # Проверяем, есть ли у точки высота
                            if previous_elevation is not None:
                                elevation_difference = point.elevation - previous_elevation
                                if elevation_difference > 0:
                                    elevation_gain += elevation_difference
                            previous_elevation = point.elevation  # Обновляем предыдущую высоту
                        else:
                            previous_elevation = None  # Если высота отсутствует, сбрасываем previous_elevation

            # Сохраняем вычисленные значения в объекте трека
            track.distance = distance
            track.elevation_gain = elevation_gain
            track.save()

            return redirect('routes')
    else:
        form = GPXTrackForm()

    tracks = GPXTrack.objects.all()
    return render(request, 'poster/routes.html', {'form': form, 'tracks': tracks})

def delete_route(request, track_id):
    track = get_object_or_404(GPXTrack, id=track_id)
    
    # Удаляем файл и сам объект
    track.file.delete()  # Удаляем файл с диска
    track.delete()       # Удаляем запись из базы данных
    
    messages.success(request, f'Маршрут "{track.name}" был успешно удалён.')
    return redirect('routes')

def routes_view(request):
    if request.method == 'POST':
        form = GPXTrackForm(request.POST, request.FILES)
        if form.is_valid():
            gpx_file = request.FILES['file']
            track = form.save(commit=False)

            # Чтение и парсинг GPX файла
            gpx = gpxpy.parse(gpx_file.read().decode('utf-8'))

            distance = 0
            elevation_gain = 0
            previous_elevation = None

            # Перебираем все треки и их сегменты
            for gpx_track in gpx.tracks:
                for segment in gpx_track.segments:
                    # Вычисляем длину сегмента
                    distance += segment.length_2d() / 1000  # длина в км

                    # Проходим по точкам и вычисляем набор высоты
                    for point in segment.points:
                        if point.elevation is not None:  # Проверяем, есть ли у точки высота
                            if previous_elevation is not None:
                                elevation_difference = point.elevation - previous_elevation
                                if elevation_difference > 0:
                                    elevation_gain += elevation_difference
                            previous_elevation = point.elevation  # Обновляем предыдущую высоту
                        else:
                            previous_elevation = None  # Если высота отсутствует, сбрасываем previous_elevation

            # Сохраняем вычисленные значения в объекте трека
            track.distance = distance
            track.elevation_gain = elevation_gain
            track.save()

            return redirect('routes')
    else:
        form = GPXTrackForm()

    tracks = GPXTrack.objects.all()
    return render(request, 'poster/routes.html', {'form': form, 'tracks': tracks})


def add_routes(request):
    return render(request, 'poster/add_routes.html')
