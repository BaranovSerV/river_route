from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('report/', views.report, name='report'),
    path('favourites/', views.favourites, name='favourites'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('forum/', views.forum, name='forum'),
    path('forum/add/', views.add_topic, name='add_topic'),
    path('forum/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('add_topic/', views.add_topic, name='add_topic'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
