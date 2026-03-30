from django.urls import path
from .views import PostListView, PostDetailView, CreateView, PostCreateView, PostUpdateView, PostDeleteView
from . import views

urlpatterns = [
    # Service worker (JavaScript)
    path('sw.js', views.service_worker, name='service-worker'),
    # Offline page
    path('offline/', views.offline, name='offline'),
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
]


